import discord
from math import inf
from discord.ext import commands
import random
import asyncio
from replit import db
import json
import datetime


class Try(commands.Cog):
    def __init__(self, client):
        self.client = client



def setup(client):
    client.add_cog(Try(client))
