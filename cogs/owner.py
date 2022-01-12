import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from replit import db
import json
import os

file = ""


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def load1(self, ctx, filename):

        global file

        file = filename

        data = db[filename]
            
        if data:

            url = str((os.getenv("REPLIT_DB_URL")))
            
            req = requests.get("{}/{}".format(url,filename))
            soup = BeautifulSoup(req.content, features="html5lib")
            
            a = soup.find("body")

            rm = ["<body>", "</body>", "</strong>", "</strong>"]
            for i in rm:
                a = str(a).replace(i, "")
            a = a.replace("null", "None")

            js = eval(a)
            with open("manage.json", "w") as bd:
                json.dump(js, bd, indent=4)

            await ctx.send(f"{filename} loaded!")
        else:

            await ctx.send(f"No DB {filename} found")


    @commands.command()
    @commands.is_owner()
    async def rewrite1(self, ctx):

        global file

        with open("manage.json", "r") as bot_data:
            data = json.load(bot_data)

        db[file] = data

        await ctx.send(f"{file} has been rewritten")
        
        file = ""


    @commands.command()
    @commands.is_owner()
    async def keys(self, ctx): 
        
        keys = db.keys()   
        await ctx.send(keys)
        await ctx.send(os.getenv("REPLIT_DB_URL"))


    @commands.command()
    @commands.is_owner()
    async def delete1(self, ctx, file):

        del db[file]

        await ctx.send(f"Deleted {file} from DataBase")

    

    
def setup(client):
    client.add_cog(Owner(client))
    