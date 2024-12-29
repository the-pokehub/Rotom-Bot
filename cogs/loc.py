import requests
import json
from bs4 import BeautifulSoup
import string
import difflib
from discord.ext import commands
import discord
import math


def monNum(mon):

    with open("data/pokedex.json", "r") as bd:
        data = json.load(bd)

    with open("data/aliases.json", "r") as ala:
        lit = json.load(ala)

    find1 = mon.translate(str.maketrans('', '', string.punctuation))

    find1 = find1.replace(" ", "")

    if find1 in data["Pokedex"]:
        ret = str(data["Pokedex"][find1]["num"])
        return ret.zfill(3)

    if find1 in lit["Pokedex"]:
        mod = lit["Pokedex"][find1]
        ret = str(data["Pokedex"][mod]["num"])
        return ret.zfill(3)

    match = difflib.get_close_matches(find1, data["Pokedex"], 1)

    if match:
        ret = str(data["Pokedex"][match[0]]["num"])
        return ret.zfill(3)

    return None


def gen(gam):
    games = ["gs", "rs", "dp", "bw", "xy", "sm", "swsh"]
    gaDi = {
        "rb": "",
        "frlg": "-rs",
        "hgss": "-dp",
        "bw2": "-bw",
        "oras": "-xy",
        "usum": "-sm",
        "ss": "-swsh",
        "bdsp": "-swsh"
    }

    if gam in games:
        return "-" + gam

    elif gam in gaDi:
        return gaDi[gam]

    else:
        return None


def getLoc(mon, gam):

    if mon and gam:
        url = f"https://www.serebii.net/pokedex{gam}/{mon}.shtml"

        r = requests.get(url)

        # ,  parse_only=SoupStrainer("table", class_="dextable"),)
        soup = BeautifulSoup(r.content, features="html5lib")
        a = soup.find_all("table", attrs={"class": "dextable"})

        for i in a:
            if "Locations" in i.get_text():
                links = i.find_all("a")
                ldict = {}
                baseUrl = "https://www.serebii.net/"
                for link in links:
                    ldict[link.get_text()] = baseUrl + link.get("href")

                send = ""

                cells = i.find_all("td")
                cells = cells[1:]

                for cell in cells:
                    strB = str(cell).replace("<br />", "\n")
                    cell = BeautifulSoup(strB, "html.parser")
                    cell = cell.get_text().split(",")
                    for c in cell:
                        add = False
                        for links in ldict:
                            if links in c:
                                add = True
                                if links == "Details":
                                    continue
                                s = f"[{links}]({ldict[links]})"
                                send += "\n__" + c.replace(links, s) + "__"
                        if not add:

                            games = [
                                "Sword", "Shield", "Brilliant Diamond",
                                "Shining Pearl", "Sun", "Moon", "Ultra Sun",
                                "Ultra Moon", "Let's Go, Pikachu!",
                                "Let's Go, Eevee!", "X", "Y", "Omega Ruby",
                                "Alpha Sapphire", "Black", "White", "Black 2",
                                "White 2", "Dream World", "Diamond", "Pearl",
                                "Platinum", "HeartGold", "SoulSilver", "Ruby",
                                "Sapphire", "Emerald", "FireRed", "LeafGreen",
                                "Colosseum", "XD", "PokéWalker", "Gold",
                                "Silver", "Crystal", "Red", "Yellow",
                                "Green (Jp.)", "Blue (Intl.)", "Blue (Jp.)",
                                "Crown Tundra", "Isle of Armor"
                            ]

                            if c == "Trainer Locations":
                                continue
                            elif c in games:
                                send += "\n**" + c + "**"
                            else:
                                send += "\n" + c
                            add = False

                return send, url

    else:
        return None


currencies = [
    "ars", "aud", "bhd", "bwp", "brl", "bnd", "bgn", "cad", "clp", "cny",
    "cop", "hrk", "czk", "dkk", "eur", "hkd", "huf", "isk", "inr", "idr",
    "irr", "ils", "jpy", "kzt", "krw", "kwd", "lyd", "myr", "mur", "mxn",
    "npr", "nzd", "nok", "omr", "pkr", "php", "pln", "qar", "ron", "rub",
    "sar", "sgd", "zar", "lkr", "sek", "chf", "twd", "thb", "ttd", "try",
    "aed", "gbp", "usd", "vef"
]


def main():
    url = "https://www.x-rates.com/calculator/"
    r = requests.get(url)

    soup = BeautifulSoup(r.content, features="html5lib")
    a = soup.find("ul", attrs={"class": "currencyList currencycalculator"})
    lines = a.find_all("li")

    for line in lines:
        link = line.find("a")
        short = link.get("href").split("from=")[1]
        print(f"\"{short.lower()}\"", end=", ")


def get_currency(currency, from_, to_):

    if from_ not in currencies:
        with open("data/currencies.json") as d:
            data = json.load(d)

        if from_ not in data:
            return "Invalid Source Currency!"

    if to_ not in currencies:
        with open("data/currencies.json") as d:
            data = json.load(d)

        if to_ not in data:
            return "Invalid Destination Currency!"

    url = f"https://www.x-rates.com/calculator/?from={from_}&to={to_}&amount={currency}"
    r = requests.get(url)

    soup = BeautifulSoup(r.content, features="html5lib")
    a = soup.find("span", attrs={"class": "ccOutputRslt"})
    return a.get_text()


class Loc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="location-dex", aliases=["loc"])
    async def location(self, ctx, mon, generation):
        "Get location info of a Pokemon from the Generation."

        async with ctx.typing():

            got = getLoc(monNum(mon.lower()), gen(generation.lower()))

        if got:
            embed = discord.Embed(title="Location Dex",
                                  description=got[0],
                                  color=discord.Color.orange())
            embed.set_footer(
                text="Source: https://www.serebii.net/",
                icon_url="https://cdn.discordapp.com/attachments/770846450896470049/906165178528325632/serebii_icon.png"
            )
            try:
                await ctx.send(embed=embed)
            except Exception:
                await ctx.send(got[1])

        else:
            await ctx.send("You have entered wrong details.")

    @commands.hybrid_command(name="convert-currency", aliases=["cc"])
    async def currencyconvert(self, ctx, amount, source, destination="USD"):
        "Convert Currency from Source to Destination."

        ret = get_currency(amount, source.lower(), destination.lower())

        em = discord.Embed(title="Currency Converter",
                           color=discord.Color.orange())

        em.add_field(name="Input",
                     value=f"{amount} {source.upper()}",
                     inline=False)
        em.add_field(name="Converted", value=ret, inline=False)

        await ctx.send(embed=em)

    @commands.hybrid_command(name="lightning-damage")
    async def dmg(self, ctx, hp, light="9", eq="5"):
        "Check the no. of Lights and Eq required for the given HP."

        with open("data/dmg.json", "r") as file:
            data = json.load(file)

        eq = eq.lower()

        if hp.isnumeric:
            hp = int(hp)
        else:
            return await ctx.send("Wrong Input!")

        if light not in [
                "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"
        ] and eq not in ["1", "2", "3", "4", "5", "none"]:
            return await ctx.send("Wrong Input!")

        ldmg = int(data["light"][light])
        edmg = int(data["eq"][eq])

        hp = hp - (edmg * hp / 100)

        lights = math.ceil(hp / ldmg)

        if eq != "none":
            send = f"Use **{lights}** lvl {light} Lightning spells and a lvl {eq} Earthquake spell."
        else:
            send = f"Use **{lights}** lvl {light} Lightning spells without EQ."

        await ctx.send(send)


async def setup(client):
    await client.add_cog(Loc(client))
