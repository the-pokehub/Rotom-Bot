import discord
from math import inf
from discord.ext import commands
import random
import asyncio
from replit import db
import json
import datetime

file = ""

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

winningConditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],
                     [2, 5, 8], [0, 4, 8], [2, 4, 6]]


class Try(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command()
    # @commands.is_owner()
    # async def test(self, ctx):

    #     with open("hof.json", "r") as bot_data:
    #         data = json.load(bot_data)

    #     em = discord.Embed(title="Sample HOF", description="It is only for Pokéhub League 2020 for now")

    #     gls = data["Pok\u00e9hub League 2020"]["gen6"]["gl"]

    #     em.add_field(name="Gen VI", value="\u200b", inline=False)

    #     em.add_field(name="Gym Leaders:", value=f"Total: {len(gls)}", inline=False)

    #     for gl in gls:
    #         g = gl.split(",")
    #         member_id = ''.join(filter(lambda i: i.isdigit(), g[0]))
    #         if member_id:
    #             mem = await ctx.guild.fetch_member(int(member_id))
    #             leader = mem
    #         else:
    #             leader = g[0]
    #         em.add_field(name=leader, value=f"{g[1]} {g[2]}")

    #     e4s = data["Pok\u00e9hub League 2020"]["gen6"]["e4"]
    #     em.add_field(name="Elites:", value=f"Total: {len(e4s)}", inline=False)
    #     for e4 in e4s:
    #         g = e4.split(",")
    #         member_id = ''.join(filter(lambda i: i.isdigit(), g[0]))
    #         if member_id:
    #             mem = await ctx.guild.fetch_member(int(member_id))
    #             leader = mem
    #         else:
    #             leader = g[0]
    #         em.add_field(name=leader, value=g[1])

    #     chs = data["Pok\u00e9hub League 2020"]["gen6"]["champ"]
    #     em.add_field(name="Champions:", value=f"Total: {len(chs)}", inline=False)
    #     for ch in chs:
    #         g = ch.split(",")
    #         member_id = ''.join(filter(lambda i: i.isdigit(), ch))
    #         if member_id:
    #             mem = await ctx.guild.fetch_member(int(member_id))
    #             leader = mem
    #         else:
    #             leader = ch
    #         em.add_field(name=leader, value="\u200b")

    #     # em.add_field(name="\u200b", value="\u200b", inline=False)

    #     gls = data["Pok\u00e9hub League 2020"]["gen7"]["gl"]

    #     em.add_field(name="Gen VII", value="\u200b", inline=False)

    #     em.add_field(name="Gym Leaders:", value=f"Total: {len(gls)}", inline=False)

    #     for gl in gls:
    #         g = gl.split(",")
    #         member_id = ''.join(filter(lambda i: i.isdigit(), g[0]))
    #         if member_id:
    #             mem = await ctx.guild.fetch_member(int(member_id))
    #             leader = mem
    #         else:
    #             leader = g[0]
    #         em.add_field(name=leader, value=f"{g[1]} {g[2]}")

    #     e4s = data["Pok\u00e9hub League 2020"]["gen7"]["e4"]
    #     em.add_field(name="Elites:", value=f"Total: {len(e4s)}", inline=False)
    #     for e4 in e4s:
    #         g = e4.split(",")
    #         member_id = ''.join(filter(lambda i: i.isdigit(), g[0]))
    #         if member_id:
    #             mem = await ctx.guild.fetch_member(int(member_id))
    #             leader = mem
    #         else:
    #             leader = g[0]
    #         em.add_field(name=leader, value=g[1])

    #     chs = data["Pok\u00e9hub League 2020"]["gen7"]["champ"]
    #     em.add_field(name="Champions:", value=f"Total: {len(chs)}", inline=False)
    #     for ch in chs:
    #         member_id = ''.join(filter(lambda i: i.isdigit(), ch))
    #         if member_id:
    #             mem = await ctx.guild.fetch_member(int(member_id))
    #             leader = mem
    #         else:
    #             leader = ch
    #         em.add_field(name=leader, value="\u200b") 

    #     await ctx.send(embed=em)

    # async def strrrr(self, txt):

    #     ret = []

    #     spc = txt.split(" ")
    #     cnt = txt.split(":")

    #     if len(cnt) > 1:
    #         for item in spc:
    #             if item.count(":") > 1:
    #                 wr = ""
    #                 if item.startswith("<") and item.endswith(">"):
    #                     ret.append(item)



    # @commands.command()
    # @commands.is_owner()
    # async def getem(self, ctx, member:discord.Member=None):

    #     XPLAYER = ":regional_indicator_x:"
    #     OPLAYER = ":regional_indicator_o:"
    #     EMPTY = ":white_large_square:"
    #     count = 1

    #     board = [
    #         [EMPTY, EMPTY, EMPTY],
    #         [EMPTY, EMPTY, EMPTY],
    #         [EMPTY, EMPTY, EMPTY]
    #     ]

    #     async def printBoard(self, brd):
    #         chars = {XPLAYER: ':regional_indicator_x:', OPLAYER: ':regional_indicator_o:', EMPTY: ':white_large_square:'}
    #         e_b = []
    #         for x in brd:
    #             for y in x:
    #                 ch = chars[y]
    #                 e_b.append(ch)
    #                 p_b = " ".join(e_b)
    #                 await ctx.send(p_b)

    #     # def clearBoard(brd):
    #     #     for x, row in enumerate(brd):
    #     #         for y, col in enumerate(row):
    #     #             brd[x][y] = ":white_large_square:"
        
    #     async def winningPlayer(brd, point):
    #         winningStates = [[brd[0][0], brd[0][1], brd[0][2]],
    #                         [brd[1][0], brd[1][1], brd[1][2]],
    #                         [brd[2][0], brd[2][1], brd[2][2]],
    #                         [brd[0][0], brd[1][0], brd[2][0]],
    #                         [brd[0][1], brd[1][1], brd[2][1]],
    #                         [brd[0][2], brd[1][2], brd[2][2]],
    #                         [brd[0][0], brd[1][1], brd[2][2]],
    #                         [brd[0][2], brd[1][1], brd[2][0]]]

    #         if [point, point, point] in winningStates:
    #             return True

    #         return False


    #     def gameWon(brd):
    #         return winningPlayer(brd, XPLAYER) or winningPlayer(brd, OPLAYER)


    #     def printResult(brd):
    #         if winningPlayer(brd, XPLAYER):
    #             print('X has won! ' + '\n')

    #         elif winningPlayer(brd, OPLAYER):
    #             print('O\'s have won! ' + '\n')

    #         else:
    #             print('Draw' + '\n')


    #     def emptyCells(brd):
    #         emptyC = []
    #         for x, row in enumerate(brd):
    #             for y, col in enumerate(row):
    #                 if brd[x][y] == EMPTY:
    #                     emptyC.append([x, y])

    #         return emptyC


    #     def boardFull(brd):
    #         if len(emptyCells(brd)) == 0:
    #             return True
    #         return False


    #     def setMove(brd, x, y, player):
    #         brd[x][y] = player


    #     async def playerMove(brd):
    #         e = True
    #         moves = {1: [0, 0], 2: [0, 1], 3: [0, 2],
    #                 4: [1, 0], 5: [1, 1], 6: [1, 2],
    #                 7: [2, 0], 8: [2, 1], 9: [2, 2]}
    #         while e:
    #             try:
    #                 move = int(input('Pick a position(1-9)'))
    #                 if move < 1 or move > 9:
    #                     await ctx.send('Invalid location! ')
    #                 elif not (moves[move] in emptyCells(brd)):
    #                     await ctx.send('Location filled')
    #                 else:
    #                     setMove(brd, moves[move][0], moves[move][1], XPLAYER)
    #                     await printBoard(self, brd)
    #                     e = False
    #             except(KeyError, ValueError):
    #                 await ctx.send('Please pick a number!')


    #     def getScore(brd):
    #         if winningPlayer(brd, XPLAYER):
    #             return 10

    #         elif winningPlayer(brd, OPLAYER):
    #             return -10

    #         else:
    #             return 0


    #     def MiniMaxAB(brd, depth, alpha, beta, player):
    #         row = -1
    #         col = -1
    #         if depth == 0 or gameWon(brd):
    #             return [row, col, getScore(brd)]

    #         else:
    #             for cell in emptyCells(brd):
    #                 setMove(brd, cell[0], cell[1], player)
    #                 score = MiniMaxAB(brd, depth - 1, alpha, beta, -player)
    #                 if player == XPLAYER:
    #                     # X is always the max player
    #                     if score[2] > alpha:
    #                         alpha = score[2]
    #                         row = cell[0]
    #                         col = cell[1]

    #                 else:
    #                     if score[2] < beta:
    #                         beta = score[2]
    #                         row = cell[0]
    #                         col = cell[1]

    #                 setMove(brd, cell[0], cell[1], EMPTY)

    #                 if alpha >= beta:
    #                     break

    #             if player == XPLAYER:
    #                 return [row, col, alpha]

    #             else:
    #                 return [row, col, beta]


    #     def AIMove(brd):
    #         if len(emptyCells(brd)) == 9:
    #             x = random.choice([0, 1, 2])
    #             y = random.choice([0, 1, 2])
    #             setMove(brd, x, y, OPLAYER)
    #             await printBoard(self, brd)

    #         else:
    #             result = MiniMaxAB(brd, len(emptyCells(brd)), -inf, inf, OPLAYER)
    #             setMove(brd, result[0], result[1], OPLAYER)
    #             await printBoard(self, brd)


    #     def AI2Move(brd):
    #         if len(emptyCells(brd)) == 9:
    #             x = random.choice([0, 1, 2])
    #             y = random.choice([0, 1, 2])
    #             setMove(brd, x, y, XPLAYER)
    #             await printBoard(self, brd)

    #         else:
    #             result = MiniMaxAB(brd, len(emptyCells(brd)), -inf, inf, XPLAYER)
    #             setMove(brd, result[0], result[1], XPLAYER)
    #             await printBoard(self, brd)


    #     def makeMove(brd, player, mode):
    #         if mode == 1:
    #             if player == XPLAYER:
    #                 playerMove(brd)

    #             else:
    #                 AIMove(brd)
    #         else:
    #             if player == XPLAYER:
    #                 AIMove(brd)
    #             else:
    #                 AI2Move(brd)


    #     def playerVSai():
    #         order = 2

    #         # clearBoard(board)
    #         if order == 2:
    #             currentPlayer = OPLAYER
    #         else:
    #             currentPlayer = XPLAYER

    #         while not (boardFull(board) or gameWon(board)):
    #             makeMove(board, currentPlayer, 1)
    #             currentPlayer *= -1

    #         printResult(board)

    #     async def playerVSplayer(self, ctx, member):
    #         p2 = member

    #         if p2.bot:
    #             await ctx.send("You cannot play with a Bot.")
    #             return

    #         p1 = ctx.author
    #         global over

    #         if p2 == ctx.author:
    #             await ctx.send("You cannot play with yourself.")
    #             return

    #         ask = await ctx.send(f"{p2.mention}, {p1.name} has invited you for a tic-tac-toe match. Do you want to play with him?")
    #         await ask.add_reaction("✅")
    #         await ask.add_reaction("❎")

    #         def check(reaction, user):
    #             return user == p2 and str(reaction.emoji) in ["✅", "❎"]

        
    #         try:
    #             reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)

    #             if str(reaction.emoji) == "✅":
    #                 # cur_page += 1
    #                 # await msg.edit(embed=help_embed2)
    #                 await ask.delete()
                    

    #             elif str(reaction.emoji) == "❎":
    #                 # cur_page -= 1
    #                 # await msg.edit(embed=help_embed1)\
    #                 await ctx.send(f"{p2.mention} Declined!")
    #                 await ask.delete()
    #                 return

    #             else:
    #                 pass
    #         except asyncio.TimeoutError:
    #             await ask.clear_reactions()
    #         except discord.errors.NotFound:
    #             pass

    #         # await self.loading(ctx, 0.1)

    #         embed = discord.Embed(title=f"Tic-Tac-Toe between {p1} and {p2}", description="Type out `a` , `b` or `c` for the row, then `1` , `2` or `3` for the column. (eg. `a1` for top-left or `b2` for middle or `c3` for the bottom-right).\nYou can also type from `1` to `9`. (eg. `1` for top-left or `5` for middle or `9` for the bottom-right).\nYou can also type `quit` to quit the game.\nEach turn is of 60 seconds.", colour=discord.Colour.green())

    #         await ctx.send(embed=embed)

    #         def check_winner(w_conditions, point):
    #             global over
    #             for condition in w_conditions:
    #                 if board[condition[0]] == point and board[condition[1]] == point and board[condition[2]] == point:
    #                     over = True

    #         board = [
    #             ":white_large_square:", ":white_large_square:",
    #             ":white_large_square:", ":white_large_square:",
    #             ":white_large_square:", ":white_large_square:",
    #             ":white_large_square:", ":white_large_square:",
    #             ":white_large_square:"
    #         ]

    #         count = 0

    #         line = ""

    #         num = random.randint(1, 2)
    #         turn: discord.Member = ctx.author
    #         mark = ""
    #         position = 0

    #         if num == 1:
    #             turn = p1
    #         else:
    #             turn = p2

    #         while not over:

    #             if turn == p1:
    #                 mark = ":regional_indicator_x:"
    #             elif turn == p2:
    #                 mark = ":regional_indicator_o:"

    #             msg2 = await ctx.send(f"{turn.mention}'s Turn.")

    #             def check(ms):
    #                 return ms.author == turn and ms.channel == ctx.channel

    #             while True:
    #                 try:

    #                     place = await self.client.wait_for("message",
    #                                                         check=check,
    #                                                         timeout=60.0)
    #                     pos = place.content

    #                     if pos.casefold() == "quit" or pos == "0" or pos.casefold() == "forfied":
    #                         await ctx.send(f"{turn.mention} fortified.")
    #                         if turn == p1:
    #                             await ctx.send(f"{p2.mention} wins...")
    #                             return
    #                         else:
    #                             await ctx.send(f"{p1.mention} wins...")
    #                             return

    #                     elif pos.isnumeric():
    #                         position = int(pos)

    #                     elif pos.casefold() in pos_dict:
    #                         position = pos_dict[pos.lower()]

    #                     else:
    #                         continue

    #                     if 0 < position < 10 and board[position -
    #                                             1] == ":white_large_square:":
    #                         board[position - 1] = mark
    #                         count += 1
        #                     await place.delete()
        #                     await msg2.delete()
        #                     break

        #                 else:
        #                     try:
        #                         await msg3.delete()
        #                     except discord.errors.NotFound:
        #                         pass
        #                     except UnboundLocalError:
        #                         pass

        #                     msg3 = await ctx.send(
        #                         "Be sure to choose a number between 1 and 9 and an unmarked tile."
        #                     )

        #                     continue

        #             except asyncio.TimeoutError:
        #                 await ctx.send("Response Timeout...")
        #                 if turn == p1:
        #                     await ctx.send(f"{p2.mention} wins...")
        #                 else:
        #                     await ctx.send(f"{p1.mention} wins...")
        #                 return

                
        #         try:
        #             await msg3.delete()
        #         except discord.errors.NotFound:
        #             pass
        #         except UnboundLocalError:
        #             pass
                    

        #         board_list = []
        #         for x in range(len(board)):
        #             if x == 2 or x == 5 or x == 8:
        #                 line += board[x]
        #                 board_list.append(line)
        #                 # await ctx.send(line)
        #                 line = ""

        #             else:
        #                 line += board[x]

        #         new_board = "\n".join(board_list)

        #         if count == 1:
        #             msg = await ctx.send(new_board)
        #         else:
        #             await msg.edit(content=new_board)

        #         check_winner(winningConditions, mark)

        #         if over:
        #             await ctx.send(f"{turn.mention} wins...")
        #             return

        #         if count >= 9:
        #             await ctx.send("It's a tie...")
        #             return

        #         if turn == p1:
        #             turn = p2
        #         elif turn == p2:
        #             turn = p1

        # if member is None:
        #     playerVSai()
        # else:
        #     pass


def setup(client):
    client.add_cog(Try(client))
