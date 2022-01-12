import discord
from discord.ext import commands
import random
import asyncio
from replit import db

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


    @commands.command(aliases=["guessing-game", "guessinggame"])
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
        
        if ctx.author.id == 549415697726439434:
            ow = await self.client.fetch_user(549415697726439434)
            await ow.send(answer)
            # print(answer)

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


    @commands.command(aliases=["rps", "rock-paper-scissors"])
    async def rock_paper_scissors(self, ctx):

        t = ["rock", "paper", "scissors"]

        computer_action = random.choice(t)
        computer_action = computer_action.lower()

        msg = await ctx.send("What's Your choice?\nRock(🪨), Paper(🧻) or Scissors(✂)")

        emoji1 = "🪨"
        emoji2 = "🧻"
        emoji3 = "✂"

        await msg.add_reaction(emoji1)
        await msg.add_reaction(emoji2)
        await msg.add_reaction(emoji3)

        def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["🪨", "🧻", "✂"]

        while True:

            try:
                reaction, user = await self.client.wait_for("reaction_add",
                                                   check=check,
                                                   timeout=60)

                if str(reaction.emoji) == "🪨":
                    user_action = "rock"

                elif str(reaction.emoji) == "🧻":
                    user_action = "paper"

                elif str(reaction.emoji) == "✂":
                    user_action = "scissors"

                else:
                    pass

                if user_action == computer_action:
                    await ctx.reply(f"Both players selected {user_action.capitalize()}. It's a tie!")
                    return

                if user_action == "rock":
                    await ctx.reply(f"I choosed {computer_action}")
                    if computer_action == "scissors":
                        await ctx.reply("Rock smashes Scissors! You win!")
                        return
                    else:
                        await ctx.reply("Paper covers Rock! You lose.")
                        return

                elif user_action == "paper":
                    await ctx.reply(f"I choosed {computer_action}")
                    if computer_action == "rock":
                        await ctx.reply("Paper covers Rock! You win!")
                        return
                    else:
                        await ctx.reply("Scissors cuts Paper! You lose.")
                        return

                elif user_action == "scissors":
                    await ctx.reply(f"I choosed {computer_action}")
                    if computer_action == "paper":
                        await ctx.reply("Scissors cuts Paper! You win!")
                        return
                    else:
                        await ctx.reply("Rock smashes Scissors! You lose.")
                        return

            except asyncio.TimeoutError:
                await ctx.reply("Response Timeout.\nReturning...")
                return

    # @commands.command()
    # async def gamelb(self, ctx, global_lb=""):

    #     lb = db["trivia"]
    #     lb = dict(sorted(lb.items(), key = lambda kv:kv[1], reverse = True))
    #     db["trivia"] = lb

    #     if global_lb != "global":
    #         title = f"{ctx.guild.name}'s Leaderboard - Trivia"
    #         des = ""
    #         num = 1
    #         for i in lb:
    #             mem = None
    #             try:
    #                 mem = await ctx.guild.fetch_member(int(i))
    #             except discord.HTTPException:
    #                 pass

    #             if mem:

    #                 if num == 1:
    #                     des += "🥇 "
    #                 elif num == 2:
    #                     des += "🥈 "
    #                 elif num == 3:
    #                     des += "🥉 "
    #                 else:
    #                     des += "👏 "

                    
    #                 wins = lb[i]
    #                 des += f"**{wins}** wins - {mem}\n"
    #                 num += 1
    #                 if num > 10:
    #                     break
                        
    #         if des == "":
    #             des = "__NONE__"

    #     else:
    #         title = "Global Leaderboard - Trivia"
    #         des = ""
    #         num = 1
    #         for i in lb:
    #             mem = self.client.get_user(int(i))
    #             if num == 1:
    #                 des += "🥇 "
    #             elif num == 2:
    #                 des += "🥈 "
    #             elif num == 3:
    #                 des += "🥉 "
    #             else:
    #                 des += "👏 "

                
    #             wins = lb[i]
    #             des += f"**{wins}** wins - {mem}\n"
    #             num += 1
    #             if num > 10:
    #                 break

    #     em = discord.Embed(title=title, description=des, color = discord.Color.green())
    #     await ctx.send(embed=em)

    @commands.group(invoke_without_command=True,
                    case_insensitive=True)
    async def uniteid(self, ctx):

        unite = db["unite"]

        # desc = ""

        # for i in unite:
        #     mem = self.client.get_user(int(i))
        #     desc += f"{mem.mention} **Name:** {unite[i]['name'] }, **ID:** {unite[i]['id']}\n"

        # em = discord.Embed(title="Pokemon Unite Players IDs",
        # colour=0x8452ff,
        # description=desc)

        # if ctx.author.id == 549415697726439434:

        num = 0 
        sendLst = []
        desc = ""

        for i in unite:
            try:
                mem = await ctx.guild.fetch_member(int(i))
                desc += f"{mem.mention} **Name:** {unite[i]['name'] }, **ID:** {unite[i]['id']}\n"
                num += 1

                if num >= 20:
                    sendLst.append(desc)
                    desc = ""
                    num = 0
            except:
                pass

        sendLst.append(desc)

        page = 0

        em1 = discord.Embed(title="Pokemon Unite Players IDs",
        colour=0x8452ff,
        description=sendLst[page])
        em1.set_thumbnail(url="https://cdn.discordapp.com/attachments/847509607185383494/894968904219263016/PULOGO-SQ.png")
        em1.set_footer(text=f"Page {page+1} out of {len(sendLst)}")

        msg = await ctx.send(embed=em1)
        await msg.add_reaction("◀️")
        await msg.add_reaction("▶️")

        async def editEM(page):

            # if page + 1 > len(sendLst):
            #     page -= 1
            # elif page < 0:
            #     page += 1
            # else:

            em2 = discord.Embed(title="Pokemon Unite Players IDs",
            colour=0x8452ff,
            description=sendLst[page])
            em2.set_footer(text=f"Page {page+1} out of {len(sendLst)}")
            em2.set_thumbnail(url="https://cdn.discordapp.com/attachments/847509607185383494/894968904219263016/PULOGO-SQ.png")
            await msg.edit(embed=em2)

            await msg.remove_reaction("◀️", ctx.author)
            await msg.remove_reaction("▶️", ctx.author)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["▶️", "◀️"]
        
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=30)

                if str(reaction.emoji) == "▶️":
                    if page + 2 > len(sendLst):
                        await msg.remove_reaction("▶️", ctx.author)
                        continue
                    else:
                        page += 1

                elif str(reaction.emoji) == "◀️":
                    if page - 1 < 0:
                        await msg.remove_reaction("◀️", ctx.author)
                        continue
                    else:
                        page -= 1

                await editEM(page)
            
            except asyncio.TimeoutError:
                return await msg.clear_reactions()


        # await ctx.send(embed=em)

    
    @uniteid.command()
    async def add(self, ctx, *, info):

        if ctx.guild.id != 676777139776913408:
            return

        if "--" in info:
            if not ctx.author.guild_permissions.manage_guild:
                return await ctx.send("You cannot add data of Other Member. Ask a Moderator to do it.")

            info = info.split("--")
            text = info[0]
            mem = self.client.get_user(int(info[1].replace(" ", "")))

        else:
            mem = ctx.author
            text = info

        txt = text.replace(" ", "").split(",")
        name = txt[0]
        id = txt[1]

        unite = db["unite"]

        unite[str(mem.id)] = {"id": id, "name": name}
        db["unite"] = unite

        return await ctx.send(f"Added {mem.mention} with Name: {name} and ID: {id}!")

    @uniteid.command()
    async def remove(self, ctx, *, mem:discord.Member):

        if ctx.guild.id != 676777139776913408:
            return

        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.send("You don't have permission to use this command.")

        unite = db["unite"]
        if str(mem.id) in unite:
            del unite[str(mem.id)]
        else:
            return ctx.send(f"{mem} was not registered.")

        await ctx.send(f"{mem}'s Data removed.")


def setup(client):
    client.add_cog(Game(client))
