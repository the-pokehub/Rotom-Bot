import discord
from discord.ext import commands
import asyncio
from replit import db
import json

file = ""


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, filename):
        global file

        file = filename

        try:
            data = db[filename]

            with open("manage.json", "w") as bot_data:
                json.dump(data, bot_data)

            await ctx.send(f"{filename} has been transferred")

        except KeyError:
            await ctx.send(f"No DataBase named {filename} found")

    @commands.command()
    @commands.is_owner()
    async def rewrite(self, ctx):

        global file

        filename = file

        with open("manage.json", "r") as bot_data:
            data = json.load(bot_data)

        db[filename] = data

        file = ""

        await ctx.send(f"{filename} has been rewritten")

def setup(client):
    client.add_cog(Mod(client))