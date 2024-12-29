import discord
from discord.ext import commands
import re
import requests
from bs4 import BeautifulSoup
import string
from replit import db


def evalu(url):

    r = requests.get(f"{url}.json")

    soup = BeautifulSoup(r.content, features="html5lib")

    a = soup.find("body")

    js = eval(a.get_text().replace("null", "None"))
    got = js["log"]

    p1 = js["p1id"].translate(str.maketrans('', '', string.punctuation)).replace(" ", "")
    p2 = js["p2id"].translate(str.maketrans('', '', string.punctuation)).replace(" ", "")

    got = got.split("|win|")
    got = got[1].split("\n")
    winner = got[0].translate(str.maketrans('', '', string.punctuation)).lower().replace(" ", "")

    p1m, p2m = get_rmon(js["log"])

    if winner == p1:
        return p1, p2, p1m, p2m
    elif winner == p2:
        return p2, p1, p2m, p1m
    else:
        return


async def won(replay, self):

    if "replay.pokemonshowdown.com" not in replay:
        return

    url = re.search(r"(?P<url>https?://[^\s]+)", replay).group("url")

    p1, p2, p1m, p2m = evalu(url)

    members = db["registered"]

    with open("SpookyMons.txt", "r") as bd:
        valid = bd.read()

    valid = valid.split("\n")

    if p1 in members:
        won = await self.client.fetch_user(int(members[p1]))
    else:
        return "error", f"{p1} is not registered."

    if p2 in members:
        lost = await self.client.fetch_user(int(members[p2]))
    else:
        return "error", f"{p2} is not registered."

    p1in = []
    p2in = []

    for i in p1m:
        if i not in valid:
            p1in.append(i)

    if p1in:
        return "error", f"{p1} team is not valid consisting of {p1in}"

    for i in p2m:
        if i not in valid:
            p2in.append(i)

    if p2in:
        return "error", f"{p2} team is not valid consisting of {p2in}"

    if not p1:
        return None
    else:
        return "log", f"{won.mention} won against {lost.mention}."


def validate(user):
    try:
        r = requests.get(f"https://pokemonshowdown.com/users/{user}")

    except Exception:
        return False

    soup = BeautifulSoup(r.content, features="html5lib")

    try:
        a = soup.find_all("div")[4]
    except Exception:
        return False

    b = a.find("p").get_text()

    if "(Unregistered)" in b:
        return False
    else:
        return True


def get_rmon(js):

    mons = js.split("\n|poke|")
    lastm = mons[-1].split("|\n|teampre")[0]
    mons = mons[1:-1]

    p1m = []
    p2m = []

    rm = ["|", "p1", "p2", ", M", ", F", ", L50", "-*"]
    for i in mons:
        if "p1" in i:
            for r in rm:
                i = i.replace(r, "")
                # print(i)
            p1m.append(i)

        elif "p2" in i:
            for r in rm:
                i = i.replace(r, "")
            p2m.append(i)

    for r in rm:
        lastm = lastm.replace(r, "")

    p2m.append(lastm)

    return p1m, p2m

    # print(lastm[0])
    # print(mons)

    # mons = mons.append(lastm[0])
    # print(mons)


class Tour(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.channel.id in [991682121791983676, 847509607185383494, 992846848282857615]:

            logCh = await self.client.fetch_channel(898820997501820958)

            got = await won(message.content, self)
            if got and len(got) > 1:
                log, msg = got
            else:
                return

            if log == "error":
                await message.channel.send(msg)
            elif log == "log":
                await logCh.send(msg)
            else:
                pass

    @commands.hybrid_command(name="register", description="Register yourself for the Spooky Cup")
    async def register(self, ctx, showdown_id: str):

        if ctx.channel.id not in [861952254072586240, 847509607185383494]:
            return await ctx.send("Use it in <#861952254072586240>.", ephemeral=True)

        sdid = showdown_id.lower()

        members = db["registered"]

        if str(ctx.author.id) in members.values():
            return await ctx.reply("You have already registered, contact a mod if you want to change your Showdown ID.")
        if sdid in members:
            return await ctx.reply("There is already a registered user with this ID.")

        val = validate(sdid)

        if not val:
            return await ctx.reply("You need a registered PSD ID to register.")

        members[sdid] = str(ctx.author.id)

        await ctx.reply("You are successfully registered for the Spooky Cup.")
        role = ctx.guild.get_role(856351985519165450)
        await ctx.author.add_roles(role)

    @commands.hybrid_command(name="participants", description="See the participants of Spooky Cup")
    async def participants(self, ctx):

        members = db["registered"]

        des = ""

        tot = 0

        for i in members.values():
            mem = await ctx.guild.fetch_member(i)
            des += f"{mem.mention}\n"
            tot += 1

        em = discord.Embed(title="Spooky Cup Participants", description=des, color=discord.Color.orange())

        em.set_footer(text=f"Total Participants: {tot}")

        await ctx.reply(embed=em)


async def setup(client):
    await client.add_cog(Tour(client), guilds=[discord.Object(id=676777139776913408)])
