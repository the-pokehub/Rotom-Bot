import discord
from discord.ext import commands
import asyncio
import random
import  requests
from bs4 import BeautifulSoup


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def roll(self, ctx, num:int=None):

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

        await ctx.send(f"You roled: {rolled}")


    @commands.command()
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

            em.set_thumbnail(url="https://images.squarespace-cdn.com/content/v1/586bd48d03596e5605450cee/1484851165621-U1SMXTW7C9X3BB3IEQ2U/ke17ZwdGBToddI8pDm48kJByspMdSfv7m9ZIGPyubZ4UqsxRUqqbr1mOJYKfIPR7LoDQ9mXPOjoJoqy81S2I8N_N4V1vUb5AoIIIbLZhVYxCRW4BPu10St3TBAUQYVKcthlIMN9gg26tnxitDRAP9bmUoptCGNviqECz5gO8BYCGUi3wS_nhCZz__XN4iPcB/image-asset.jpeg?format=500w")

            soup = BeautifulSoup(r.content, features="html5lib")

            a = soup.find("div",attrs={"class":"meaning"}).text
            b = soup.find("div",attrs={"class":"example"}).text
            c = soup.find("div",attrs={"class":"contributor"}).text

            up = soup.find(attrs={"class":"up"})
            d = up.find("span",attrs={"class":"count"}).text

            down = soup.find(attrs={"class":"down"})
            e = down.find("span",attrs={"class":"count"}).text

            if a:
                em.add_field(name="Defination", value=a, inline=False)
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


def setup(client):
    client.add_cog(Fun(client))
