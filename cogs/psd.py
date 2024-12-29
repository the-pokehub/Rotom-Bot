from discord.ext import commands
import discord
from bs4 import BeautifulSoup
import requests
from tabulate import tabulate


def get_rank(user):

    try:
        r = requests.get(f"https://pokemonshowdown.com/users/{user}")

    except Exception:
        return "NF"

    soup = BeautifulSoup(r.content, features="html5lib")

    tit = soup.find("title")

    tit = str(tit.get_text()).split("-")
    tit = tit[0]

    try:
        a = soup.find_all("div")[5]
    except Exception:
        return "NF"

    b = a.find_all("tr")

    tab = [["Format", "Elo", "GXE", "Glicko"]]

    for i in range(1, len(b)):
        c = b[i].find_all("td")
        if not c:
            continue
        elif len(c) == 3:
            row = [c[0].get_text(), c[1].get_text(), '-', '-']
        else:
            row = [
                c[0].get_text(), c[1].get_text(), c[2].get_text(),
                c[3].get_text()
            ]

        tab.append(row)
        if len(str(tab)) > 2500:
            break

    return tit, tab


class PSD(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in [
                1187602804441890866, 856187354536214578
        ] and message.content == "@Alpha Swarms" and message.author.bot:
            role = discord.utils.get(message.guild.roles, name="PokeMMO")
            await message.channel.send(f"{role.mention} Alpha Swarm Alert!")

    @commands.hybrid_command(name="ladder", aliases=["rankings"])
    async def _ladder(self, ctx, *, user: str):
        "Get the Ladder of the showdown user."

        if ctx.channel.id == 761502109459677185:
            return await ctx.send("Fuck Off and go to <#761527008311377930>")

        ret = get_rank(user)

        if ret == "NF":
            return await ctx.send(
                "Either the user is Not Available or the user has not played any ladder match yet."
            )

        send = tabulate(ret[1],
                        headers='firstrow',
                        tablefmt='pipe',
                        stralign='center')

        cnt = send.split("\n")
        screen = len(cnt[0])
        add = "-" * (screen - 2)

        em = discord.Embed(
            title=f"**__{ret[0]}'s Rankings__**",
            description=f"`{add} \n{send}\n{add}-`",
            colour=0x4289C1,
            url=f"https://pokemonshowdown.com/users/{user.replace(' ', '')}")
        em.set_footer(
            text="Due to discord's limit of 4000 characters, list might be incomplete press the title to view full list."
        )

        await ctx.send(embed=em)

    def get(self, replay):

        rat = None

        # try:
        r = requests.get(f"{replay}.json")
        js = r.json()

        # soup = BeautifulSoup(r.content, features="html5lib")

        # a = soup.find("body")

        # rm = ["<body>", "</body>", "</strong>", "</strong>", "</div>"]
        # for i in rm:
        #     a = str(a).replace(i, "")
        # a = a.replace("null", "None")

        # js = eval(a)
        got = js["log"]

        got = got.split("|win|")
        got = got[1].split("\n")
        winner = got[0]

        if js["rating"]:
            rat = ""
            for i in got:
                if "|raw|" in i:
                    add = i.replace("|raw|", "")
                    r = ["&lt;/strong&gt;<br />", "<strong>"]  # Fixed the invalid escape sequence
                    for j in r:
                        add = add.replace(j, "")

                    rat += add + "\n"

        return winner, js, rat

    @commands.hybrid_command(name="check-replay")
    async def evalu(self, ctx, *, replay):
        "Check showdown replay."

        win, got, rat = self.get(replay)

        if got:

            em = discord.Embed(title=f"**__{got['p1']} vs {got['p2']}__**",
                               colour=0x4289C1,
                               url=replay)

            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/890936011591401522/897515553466486845/icon.png"
            )
            em.add_field(name="Format:", value=got['format'])
            em.add_field(name="Winner:", value=win)
            if rat:
                em.add_field(name="Ladder Update:", value=rat, inline=False)

            await ctx.send(embed=em)

        else:
            await ctx.send(
                "Looks like you have put an invalid Battle Replay Link.")

    @commands.command()
    async def dance(self, ctx):
        await ctx.send(
            "<a:dance1:807167808164331531>\n<a:dance2:807167807757746177>\n<a:dance3:807167807804014602>\n<a:dance4:807167807904940073>"
        )


async def setup(client):
    await client.add_cog(PSD(client))
