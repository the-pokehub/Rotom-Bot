import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
import datetime


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def roll(self, ctx, num: int = None):

        if num is None:
            num = 1

        rolled = ""

        for i in range(num):
            rol = random.randint(1, 6)
            if rolled == "":
                rolled += str(rol)
            else:
                new = ", " + str(rol)
                rolled += new

        await ctx.send(f"You rolled: {rolled}")

    @commands.command(aliases=["flip", "coinflip"])
    async def toss(self, ctx):

        coin = random.randint(1, 2)

        if coin == 1:
            tossed = "Heads"
        else:
            tossed = "Tails"

        await ctx.send(tossed)

    @commands.command()
    async def urban(self, ctx, *, word):

        r = requests.get("http://www.urbandictionary.com/define.php?term={}".format(word))

        if r:
            em = discord.Embed(title=f"Urban {word}", colour=discord.Colour.green())

            soup = BeautifulSoup(r.content, features="html5lib")

            a = soup.find("div", attrs={"class": "meaning"}).text
            b = soup.find("div", attrs={"class": "example"}).text
            c = soup.find("div", attrs={"class": "contributor"}).text

            up = soup.find(attrs={"class": "up"})
            d = up.find("span", attrs={"class": "count"}).text

            down = soup.find(attrs={"class": "down"})
            e = down.find("span", attrs={"class": "count"}).text

            if a:
                em.add_field(name="Definition", value=a, inline=False)
            if b:
                em.add_field(name="Example", value=b, inline=False)
            if d:
                em.add_field(name="👍", value=d)
            if e:
                em.add_field(name="👎", value=e)
            if c:
                em.add_field(name="\u200b", value=c, inline=False)

        else:
            em = discord.Embed(title="❌Error Nothing Found!", colour=discord.Colour.green())

        await ctx.send(embed=em)

    @commands.command()
    async def poll(self, ctx, *, txt):
        if "//" not in txt:
            await ctx.send("Please provide valid Options.")
            return

        txt = txt.split("//")

        ask = txt[0]
        options = txt[1]
        options = options.split(",")

        if ask == "":
            await ctx.send("Enter a Question for the Poll.")
            return

        if len(options) < 2:
            await ctx.send("Please provide at least 2 Options for a Poll.")
            return

        if len(options) > 20:
            await ctx.send("You cannot make Poll with more than 20 Options")
            return

        emo = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬",
               "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺", "🇻", "🇼", "🇽",
               "🇾", "🇿"]

        text = ""
        used_emo = []

        for i in range(len(options)):
            op = options[i]
            op = op.strip()
            emoj = emo[i]

            text += emoj + " " + op + "\n\n"
            used_emo.append(emoj)

        em = discord.Embed(title=f"{ask}", description=f"{text}", colour=discord.Colour.green())

        em.set_footer(text=f"Poll by {ctx.author}")
        em.timestamp = datetime.datetime.utcnow()

        msg = await ctx.send(embed=em)
        for i in used_emo:
            try:
                await msg.add_reaction(i)
            except discord.errors.NotFound:
                pass

    @commands.command(aliases=["pollshow", "showpoll", "sp"])
    async def show_poll(self, ctx, message:discord.Message):

        poll = False
        emo = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬",
               "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺", "🇻", "🇼", "🇽",
               "🇾", "🇿"]
        title = ""
        des = ""
        for embed in message.embeds:
            title = embed.title
            des = embed.description

        des = des.split("\n\n")

        rea = []

        for reaction1 in message.reactions:
            if reaction1.emoji == "1️⃣":
                for reaction2 in message.reactions:
                    if reaction2.emoji == "2️⃣":
                        poll = True
                        break
            elif reaction1.emoji == "🇦":
                for reaction2 in message.reactions:
                    if reaction2.emoji == "🇧":
                        poll = True
                        break

        if not poll:
            await ctx.send("Please provide the message ID/link for a valid poll.")
            return

        for reaction in message.reactions:
            for em in emo:
                if reaction.emoji == em:
                    count = reaction.count
                    async for user in reaction.users():
                        if user.bot:
                            count -= 1
                    r = reaction.emoji + ", " + str(count)
                    rea.append(r)

        tot_r = 0
        for i in rea:
            c = i.split(", ")
            tot_r += int(c[1])

        if tot_r == 0:
            tot_r = 1
        
        opt = []
        for i in des:
            for j in emo:
                if j in i:
                    ele = i.replace(j, "»")
                    opt.append(ele)

        empty = "░"
        fill = "█"
        total = ""
        for i in range(len(rea)):
            c = rea[i].split(", ")
            per = int(c[1])/tot_r*float(20)
            filled = fill*int(per)
            subs = 20 - int(per)
            non_filled = empty*subs
            percentage = int(c[1])/tot_r*float(100)

            if "." in str(percentage):
                per = str(percentage).split(".")
                if len(per[1]) > 2:
                    per[1] = per[1][:2]
                perce = per[0] + "." + per[1]
            else:
                perce = str(percentage)

            total += f"{opt[i]}\n{filled}{non_filled} {perce}% ({c[1]} votes)\n\n"

        em = discord.Embed(title=title, description=f"{total} \nTotal Votes: {tot_r} \n[__Poll Jump Url__]({message.jump_url})", colour=discord.Colour.green())
        em.timestamp = message.created_at
        em.set_footer(text="Poll Results • Poll Created")
        await ctx.send(embed=em)

    @commands.command(aliases=["8pool", "8p"])
    async def _8pool(self, ctx, *, question):
        answers = [
            'It is certain',
            'It is decidedly so',
            'Without a doubt',
            'Yes – definitely',
            'You may rely on it',
            'As I see it, yes',
            'Most likely',
            'Outlook good',
            'Yes',
            'Signs point to yes',
            'Reply hazy, try again',
            'Ask again later', 
            'Better not tell you now', 
            'Cannot predict now',
            'Concentrate and ask again',
            'Dont count on it',
            'My reply is no',
            'My sources say no',
            'Outlook not so good',
            'Very doubtful']

        answer = random.choice(answers)
        em = discord.Embed(description=f"Question: {question}\nMy Answer: {answer}.") 

        await ctx.reply(embed=em)

    def get(self, replay):

        rat = None

        try:
            r = requests.get(f"{replay}.json")

            soup = BeautifulSoup(r.content, features="html5lib")

            a = soup.find("body")

            rm = ["<body>", "</body>", "</strong>", "</strong>"]
            for i in rm:
                a = str(a).replace(i, "")
            a = a.replace("null", "None")

            js = eval(a)
            got = js["log"]

            got = got.split("|win|")
            got = got[1].split("\n")
            winner = got[0]

            if js["rating"]:
                rat = ""
                for i in got:
                    if "|raw|" in i:
                        add = i.replace("|raw|", "")
                        r = ["&lt;\/strong&gt;<br \=/>", "<strong>"]
                        for j in r:
                            add = add.replace(j, "")

                        rat += add + "\n"

            return winner, js, rat

        except:
            return "Looks like you have put an invalid Battle Replay Link."


    @commands.command(aliases=["evaluate", "winner"])
    async def eval(self, ctx, *, Replay):

        win, got, rat = self.get(Replay)

        if got:
            send = f"**Format:** {got['format']}\n**Players:** {got['p1']} vs {got['p2']}\n**Winner:** {win}"
            
            if rat:
                send += f"\n**Ladder Update:**\n{rat}"

            await ctx.send(send)

        else:
            await ctx.send("Looks like you have put an invalid Battle Replay Link.")


def setup(client):
    client.add_cog(Fun(client))
