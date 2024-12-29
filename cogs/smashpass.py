
import discord as discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import random
from discord import app_commands

genD = {
    "game": "spec",
    "disney": "spec",
    "anime": "anime",
    "celebraty": "celeb",
    "cartoon": "spec"
}

with open("id.txt", encoding="utf-8") as f:
    dataAni = f.readlines()


def celeb():
    def celebF():
        get = requests.get("https://www.generatormix.com/random-female-celebrities")
        soup = BeautifulSoup(get.content, "html.parser")
        divs = soup.find_all("div", {"class": "thumbnail-col-1"})
        pick = random.choice(divs)
        ind = divs.index(pick)

        img = pick.find("img", {"class": "lazy thumbnail aspect-tall-contain"})
        name = soup.find_all("h3")[ind]

        return img["data-src"], name.get_text()

    def celebM():
        get = requests.get("https://www.generatormix.com/random-male-celebrities")
        soup = BeautifulSoup(get.content, "html.parser")
        divs = soup.find_all("div", {"class": "thumbnail-col-1"})
        pick = random.choice(divs)
        ind = divs.index(pick)

        img = pick.find("img", {"class": "lazy thumbnail aspect-square-contain"})
        name = soup.find_all("h3")[ind]

        return img["data-src"], name.get_text()

    return random.choice([celebF(), celebM()])


def character():
    get = requests.get("https://www.generatormix.com/random-character-generator")
    soup = BeautifulSoup(get.content, "html.parser")
    divs = soup.find_all("div", {"class": "thumbnail-col-1"})
    pick = random.choice(divs)
    ind = divs.index(pick)

    img = pick.find("img", {"class": "lazy thumbnail"})
    name = soup.find_all("h3")[ind]

    return img["data-src"], name.get_text()


def Specific(got=None):
    charD = {
        "game": "https://www.generatormix.com/random-female-video-game-character-generator",
        "disney": "https://www.generatormix.com/random-disney-characters",
        "anime": "https://www.generatormix.com/random-anime-character-generator",
        "cartoon": "https://www.generatormix.com/random-cartoon-characters"}

    characters = [
        "https://www.generatormix.com/random-female-video-game-character-generator",
        "https://www.generatormix.com/random-disney-characters",
        "https://www.generatormix.com/random-anime-character-generator",
        "https://www.generatormix.com/random-female-superheroes",
        "https://www.generatormix.com/random-cartoon-characters"
    ]

    dataset = {
        "https://www.generatormix.com/random-female-video-game-character-generator": "lazy thumbnail aspect-square-contain",
        "https://www.generatormix.com/random-anime-character-generator": "lazy thumbnail aspect-tall-contain",
        "https://www.generatormix.com/random-disney-characters": "lazy thumbnail aspect-tall-contain",
        "https://www.generatormix.com/random-female-superheroes": "lazy thumbnail aspect-tall-contain",
        "https://www.generatormix.com/random-cartoon-characters": "lazy thumbnail aspect-tall-contain"
    }

    if not got:
        char = random.choice(characters)
    else:
        char = charD[got]

    dat = dataset[char]

    get = requests.get(char)
    soup = BeautifulSoup(get.content, "html.parser")
    divs = soup.find_all("div", {"class": "thumbnail-col-1"})
    pick = random.choice(divs)
    ind = divs.index(pick)

    img = pick.find("img", {"class": dat})
    name = soup.find_all("h3")[ind]

    return img["data-src"], name.get_text()


def anime():
    got = random.choice(dataAni)
    spl = got.split("- ")
    name = spl[0]
    url = "https://ami.animecharactersdatabase.com/" + spl[1]
    return url, name


def main(got=None):
    if not got:
        run = random.choice(["char", "spec", "celeb", "anime", "anime", "anime"])
    else:
        run = genD[got]

    if run == "char":
        return character()
    elif run == "spec":
        return Specific(got)
    elif run == "anime":
        return anime()
    else:
        return celeb()


class SOP(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="smash-or-pass", aliases=['sop'])
    @app_commands.describe(type="Choose character type.")
    @app_commands.choices(type=[
        discord.app_commands.Choice(name="Anime", value=1),
        discord.app_commands.Choice(name="Cartoon", value=2),
        discord.app_commands.Choice(name="Celebraty", value=3),
        discord.app_commands.Choice(name="Disney", value=4),
        discord.app_commands.Choice(name="Game", value=5),

    ])
    async def _sop(self, ctx, type: discord.app_commands.Choice[int] = None):

        if ctx.channel.id in [761502109459677185]:
            return

        await ctx.defer()
        if type:
            type = type.name.lower()

        img, name = main(type)
        name = name.split("-")[0]

        embed = discord.Embed(title="Smash or Pass", description=f"**{name}**", color=discord.Color.orange())
        embed.set_image(url=img)

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(SOP(client))
