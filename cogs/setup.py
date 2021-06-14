# BETA
"""
For giving the bot support to multi server support
"""

import discord
from discord.ext import commands
from replit import db


class Setup(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command()
    # @commands.has_permissions(administrative=True)
    # async def mod_roles(self, ctx, role:discord.Role):



def setup(client):
    client.add_cog(Setup(client))