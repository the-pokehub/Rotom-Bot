import discord
from discord.ext import commands
import random
import asyncio

winningConditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],
                     [2, 5, 8], [0, 4, 8], [2, 4, 6]]

pos_dict = {
    "a1": 1,
    "a2": 2,
    "a3": 3,
    "b1": 4,
    "b2": 5,
    "b3": 6,
    "c1": 7,
    "c2": 8,
    "c3": 9
}

over = False


class Game(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["guessing-game", "guessing_game"])
    async def gg(self, ctx):

        def check(ms):
            return ms.author == ctx.author and ms.channel == ctx.channel

        em = discord.Embed(
            title="Choose your level of difficulty:",
            description="The bot will randomly select any number between the highest and the lowest value. You have to guess it. Guessing wrong will provide you a hint weather to guess higher or lower than you guessed.",
            colour=discord.Colour.green())

        em.set_thumbnail(url=ctx.author.avatar_url)

        em.add_field(name="0 | QUIT", value="Quit this game.", inline=False)
        em.add_field(name="1 | EASY",
                     value="Guess between 1 and 10.",
                     inline=False)
        em.add_field(name="2 | MEDIUM",
                     value="Guess between 1 and 100.",
                     inline=False)
        em.add_field(name="3 | HARD",
                     value="Guess between 1 and 500.",
                     inline=False)
        em.add_field(name="4 | BRUTAL",
                     value="Guess between 1 and 1000.",
                     inline=False)

        em.set_footer(text="This session will end in 30 Seconds.",
                      icon_url=self.client.user.avatar_url)

        await ctx.send(embed=em)

        highest = int()
        guess = int()

        while True:
            try:
                level = await self.client.wait_for("message",
                                                   check=check,
                                                   timeout=30.0)

                chosen_level = level.content.casefold()

                if chosen_level == "1" or chosen_level == "easy" or chosen_level == "e":
                    highest = 10
                    break

                elif chosen_level == "2" or chosen_level == "medium" or chosen_level == "m":
                    highest = 100
                    break

                elif chosen_level == "3" or chosen_level == "hard" or chosen_level == "h":
                    highest = 500
                    break

                elif chosen_level == "4" or chosen_level == "brutal" or chosen_level == "b":
                    highest = 1000
                    break

                elif chosen_level == "0" or chosen_level == "quit" or chosen_level == "q":
                    await ctx.send("You opted to QUIT!")
                    return

                else:
                    continue
            except asyncio.TimeoutError:
                await ctx.send("Response Timeout")
                return

        answer = random.randint(1, highest)
        guesses = 1
        print(answer)

        await ctx.send(
            "Guess a number between 1 and {} or 0 to quit: ".format(highest))

        while guess != answer:

            try:
                msg = await self.client.wait_for("message",
                                                 check=check,
                                                 timeout=30.0)
                guess = int(msg.content)

                if guess == 0:
                    await ctx.send("You opted to QUIT!")
                    return

                elif 1 <= guess < highest + 1:
                    if guess == answer:

                        if guesses == 1:
                            await ctx.send(
                                "WOW! You have guessed it the first time.")
                            break
                        else:
                            await ctx.send(
                                "Well done! You guessed it right.\nYou guessed it correct in {} times...".format(guesses))

                    else:
                        if guess < answer:
                            await ctx.send("Guess something higher...")
                        else:
                            await ctx.send("Guess something lower...")

                    guesses += 1

                else:
                    await ctx.send(
                        "Oops! that number is out of your range...\nIt must be between 1 and {}:".format(highest))
                    continue

            except ValueError:
                continue

            except asyncio.TimeoutError:
                await ctx.send("Response Timeout.")
                return

    @commands.command(aliases=["tictactoe", "tic-tac-toe", "tic_tac_toe"])
    async def ttt(self, ctx, player2: discord.Member):
        
        p2 = player2

        if p2.bot:
            await ctx.send("You cannot play with a Bot.")
            return

        p1 = ctx.author
        global over

        if p2 == ctx.author:
            await ctx.send("You cannot play with yourself.")
            return

        embed = discord.Embed(title=f"Tic-Tac-Toe between {p1} and {p2}", description="Type out `a` , `b` or `c` for the row, then `1` , `2` or `3` for the column. (eg. `a1` for top-left or `b2` for middle or `c3` for the bottom-right).\nYou can also type from `1` to `9`. (eg. `1` for top-left or `5` for middle or `9` for the bottom-right).\nYou can also type `quit` to quit the game.\nEach turn is of 60 seconds.", colour=discord.Colour.green())

        await ctx.send(embed=embed)

        def check_winner(w_conditions, point):
            global over
            for condition in w_conditions:
                if board[condition[0]] == point and board[condition[1]] == point and board[condition[2]] == point:
                    over = True

        board = [
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:"
        ]

        count = 0

        line = ""
        # for x in range(len(board)):
        #     if x == 2 or x == 5 or x == 8:
        #         line += " " + board[x]
        #         await ctx.send(line)
        #         line = ""

        #     else:
        #         line += " " + board[x]

        num = random.randint(1, 2)
        turn: discord.Member = ctx.author
        mark = ""
        position = 0

        if num == 1:
            turn = p1
        else:
            turn = p2

        while not over:

            if turn == p1:
                mark = ":regional_indicator_x:"
            elif turn == p2:
                mark = ":regional_indicator_o:"

            await ctx.send(f"{turn.mention}'s Turn.")

            def check(ms):
                return ms.author == turn and ms.channel == ctx.channel

            while True:
                try:

                    place = await self.client.wait_for("message",
                                                        check=check,
                                                        timeout=60.0)
                    pos = place.content

                    if pos.casefold() == "quit" or pos == "0" or pos.casefold() == "fortify":
                        await ctx.send(f"{turn.mention} fortified.")
                        if turn == p1:
                            await ctx.send(f"{p2.mention} wins...")
                        else:
                            await ctx.send(f"{p1.mention} wins...")

                    elif pos.isnumeric():
                        position = int(pos)
                        break

                    elif pos.casefold() in pos_dict:
                        position = pos_dict[pos.lower()]
                        break

                    else:
                        continue

                except asyncio.TimeoutError:
                    await ctx.send("Response Timeout...")
                    if turn == p1:
                        await ctx.send(f"{p2.mention} wins...")
                    else:
                        await ctx.send(f"{p1.mention} wins...")
                    return

            if 0 < position < 10 and board[position -
                                            1] == ":white_large_square:":
                board[position - 1] = mark
                count += 1
            else:
                await ctx.send(
                    "Be sure to choose a number between 1 and 9 and an unmarked tile."
                )

            board_list = []
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += board[x]
                    board_list.append(line)
                    # await ctx.send(line)
                    line = ""

                else:
                    line += board[x]

            new_board = "\n".join(board_list)
            await ctx.send(new_board)

            check_winner(winningConditions, mark)

            if over:
                await ctx.send(f"{turn.mention} wins...")
                return

            if count >= 9:
                await ctx.send("It's a tie...")
                return

            if turn == p1:
                turn = p2
            elif turn == p2:
                turn = p1


def setup(client):
    client.add_cog(Game(client))
