import discord
from discord.ext import commands
from discord import Embed, Member
import secrets
import asyncio


class TicTacToe:
    HUMAN = -1
    COMP = 1

    def __init__(self, ctx, member):
        self.ctx = ctx
        self.bot = ctx.bot
        self.message = None
        self.message2 = None
        self.player1 = self.turn = ctx.author
        self.player2 = member or ctx.me
        self.p1 = self.p2 = ""
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    @property
    def empty_cells(self):
        cells = []
        for x, row in enumerate(self.board):
            for y, col in enumerate(row):
                if col == 0:
                    cells.append([x, y])

        return cells

    @property
    def depth(self):
        return len(self.empty_cells)

    @property
    def game_over(self):
        return self.depth == 0 or any(map(self.is_winner, (self.HUMAN, self.COMP)))

    @property
    def emojis(self):
        return {
            f"{x}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}": x
            for x in range(1, 10)
        }

    def is_winner(self, player):
        state = self.board
        win_state = []
        diagonals = [[], []]
        for x in range(3):
            row = []
            col = []
            for y in range(3):
                row.append(state[x][y])
                col.append(state[y][x])

            win_state.append(row)
            win_state.append(col)
            diagonals[0].append(state[x][x])
            diagonals[1].append(state[abs(x - 2)][x] if x != 1 else state[1][1])

        win_state.extend(diagonals)

        return [player for _ in range(3)] in win_state

    async def ai_turn(self):
        if self.game_over:
            return True

        if self.depth == 9:
            x = secrets.choice(range(3))
            y = secrets.choice(range(3))
        else:
            move = self.minimax(self.depth, self.COMP)
            x, y, _ = move

        self.set_move(x, y, self.COMP)
        return True

    async def human_turn(self):
        if self.game_over:
            return True

        player, sign = (
            (self.HUMAN, self.p1) if self.turn == self.player1 else (self.COMP, self.p2)
        )
        move = -1
        moves = {}
        n = 0
        for x in range(3):
            for y in range(3):
                n += 1
                moves[n] = [x, y]

        await self.render(f"{self.turn.mention}'s turn! ({sign})")

        while move < 1 or move > 9:
            try:
                payload = await self.bot.wait_for(
                    "raw_reaction_add",
                    check=(
                        lambda x: x.message_id == self.message.id
                        and x.user_id == self.turn.id
                        and x.emoji.name in self.emojis
                    ),
                    timeout=60,
                )

                move = self.emojis[payload.emoji.name]
                coord = moves[move]
                coord.append(player)
                can_move = self.set_move(*coord)

                if not can_move:
                    move = -1

            except asyncio.TimeoutError:
                return await self.quit()

        return True

    def valid_move(self, x, y):
        return [x, y] in self.empty_cells

    def set_move(self, x, y, player):
        if self.valid_move(x, y):
            self.board[x][y] = player
            return True

        return False

    def evaluate(self):
        if self.is_winner(self.COMP):
            return 1

        if self.is_winner(self.HUMAN):
            return -1

        return 0

    def minimax(self, depth, player):
        """
        The actual minimax method
        """
        best = [-1, -1, float("-inf" if player == self.COMP else "inf")]

        if depth == 0 or self.game_over:
            score = self.evaluate()
            return [-1, -1, score]

        for cell in self.empty_cells:
            x, y = cell
            self.board[x][y] = player  # evaluates
            score = self.minimax(depth - 1, -player)
            self.board[x][y] = 0  # resets to 0
            score[0], score[1] = x, y

            if player == self.COMP:
                if score[2] > best[2]:
                    best = score

            else:
                if score[2] < best[2]:
                    best = score

        return best

    async def render(self, title):
        signs = {-1: self.p1, 1: self.p2}

        str_line = "----------------"  # whatever
        board_view = f"```\n{str_line}\n"
        for row in self.board:
            for cell in row:
                n = "_"
                sign = signs.get(cell, n)
                board_view += f"| {sign} |"

            board_view += f"\n{str_line}\n"

        board_view += "```"

        embed = Embed(title="Tic Tac Toe", description=board_view)
        # kwargs = dict(embed=embed, content=title)
        if self.message:
            await self.message.edit(embed=embed)
        else:
            self.message = await self.ctx.reply(embed=embed)
            self.bot.loop.create_task(self.add_reactions())

        if self.message2:
            await self.message2.delete()

        self.message2 = await self.ctx.reply(title)

    async def add_reactions(self):
        for e in self.emojis:
            await self.message.add_reaction(e)

    async def quit(self):
        winner = self.player1 if self.turn != self.player1 else self.player2
        await self.render(
            f"{self.turn.mention} quit the game, " f"{winner.mention} won!"
        )

    @property
    def is_enemy_human(self):
        return self.player2 != self.ctx.me

    async def start(self):
        self.p1 = secrets.choice(("X", "O"))
        if self.p1 == "X":
            self.p2 = "O"
        else:
            self.p2 = "X"

        first = secrets.choice(("n", ""))

        if self.is_enemy_human:
            # case where the enemy is a human
            async def player2_turn():
                try:
                    self.turn = self.player2  # sets current player to player 2
                    return await self.human_turn()
                finally:
                    self.turn = self.player1  # set it back to player 1

        else:
            # case where the enemy is a computer
            player2_turn = self.ai_turn
            await self.ctx.reply("Want to start first? [y(es)/n(o)/r(andom)/q(uit)]")

            try:
                msg = await self.bot.wait_for(
                    "message",
                    check=(
                        lambda x: x.author == self.ctx.author
                        and x.content.lower().startswith(("y", "n", "q", "r"))
                    ),
                    timeout=60,
                )

                if (msg := msg.content.lower()).startswith("q"):
                    return await self.ctx.reply("You've quit the game")

                if msg not in ("r", "random"):
                    first = msg

            except asyncio.TimeoutError:
                return await self.ctx.reply("You took too long to answer!")

        if first.startswith("n"):
            if not await player2_turn():
                return

        while not self.game_over:
            if not await self.human_turn():
                return

            if not await player2_turn():
                return

        text = "{0.mention} won the game"
        if self.is_winner(self.HUMAN):
            winner, loser = self.player1, self.player2
            text = text.format(winner)
        elif self.is_winner(self.COMP):
            winner, loser = self.player2, self.player1
            text = text.format(winner)
        else:
            text = "It's a Draw!"
            winner, loser = None, None

        await self.render(text)
        if winner == loser:
            pass

class Game(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def loading(self, ctx, time:int):
        l = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
        msg = await ctx.send(f"Loading...\n{l[0]}")
        try:
            for i in range(1, len(l)):
                # await asyncio.sleep(time)
                await msg.edit(content=f"Loading...\n{l[i]}")
            await msg.delete()
        except discord.errors.NotFound:
            pass

    @commands.command(aliases=["tictactoe", "tic-tac-toe", "tic_tac_toe"])
    async def ttt(self, ctx, *, member: Member = None):
        """
        Play TicTacToe with your friend!
        You can also play with me, but I doubt you'll win
        """

        if member is None:
            member = ctx.me
        else:
            member = member

        if (member.bot and member != ctx.me) or member == ctx.author:
            # case where the author asks a bot to play
            return await ctx.send("You can play with me instead :)")

        if member != ctx.me:
            # case where the author asks a user to play
            ask = await ctx.send(f"{member}, do you want to play with {ctx.author}?")

            await ask.add_reaction("✅")
            await ask.add_reaction("❎")

            def check(reaction, user):
                return user == member and str(reaction.emoji) in ["✅", "❎"]

            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "✅":
                    await ask.delete()

                elif str(reaction.emoji) == "❎":
                    await ctx.send(f"{member.mention} refused to play!")
                    await ask.delete()
                    return

                else:
                    pass
            except asyncio.TimeoutError:
                await ask.clear_reactions()
            except discord.errors.NotFound:
                pass

        game = TicTacToe(ctx, member)
        await game.start()


def setup(client):
    client.add_cog(Game(client))
