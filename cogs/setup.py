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
    # async def filter(self, ctx, channel:discord.channel = None):

    #     guild = db["guild"]

    #     if channel is not None:
    #         if "filter" not in guild[str(ctx,guild.id)]:
    #             guild[str(ctx,guild.id)]['filter'] = {
    #                 'active': "true",
    #                 'channel': str(channel.id)
    #             }
    #     else:

    #         if "filter" not in guild:
    #             guild['filter'] = {
    #                 'active': "true",
    #                 'channel': None
    #             }

    #     db['guild'] = guild



def setup(client):
    client.add_cog(Setup(client))