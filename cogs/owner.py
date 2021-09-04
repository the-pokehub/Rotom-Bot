import discord
from discord.ext import commands
import asyncio
from replit import db
import json
import os

file = ""


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, filename):

        global file

        file = filename

        try:
            
            data = db[filename]

            for i in data:
                await ctx.send(f"{i} : {data[i]}")

            # with open("manage.txt", "w") as bot_data:
            #     bot_data.write(str(data))

            # await ctx.send(f"{filename} has been transferred")

        except KeyError:
            await ctx.send(f"No DataBase named {filename} found")

    @commands.command()
    @commands.is_owner()
    async def rewrite(self, ctx, file):

        with open("manage.json", "r") as bot_data:
            data = json.load(bot_data)

        db[file] = data

        await ctx.send(f"{file} has been rewritten")

    @commands.command()
    @commands.is_owner()
    async def keys(self, ctx): 
        
        keys = db.keys()   
        await ctx.send(keys)
        await ctx.send(os.getenv("REPLIT_DB_URL"))

    @commands.command()
    @commands.is_owner()
    async def delete(self, ctx, file):

        del db[file]

        await ctx.send(f"Deleted {file} from DataBase")

    @commands.command()
    async def owner(self, ctx):

        member = ctx.guild.owner

        await ctx.send(member)

    
def setup(client):
    client.add_cog(Owner(client))
    