import discord
from discord.ext import commands
import asyncio
import random


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


def setup(client):
    client.add_cog(Fun(client))
