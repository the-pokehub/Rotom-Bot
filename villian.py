import discord
from discord.ext import commands, tasks
from replit import db
import asyncio
from math import floor
import time

class Villain(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.update_team_list.start()

    def cog_unload(self):
        self.update_team_list.stop()

    async def update_vt_list(self):
        """
        Update villian teams list based on team roles changes 

        :param self: Villian class
        """
        # Set channel to villian teams list and get roles from Pokehub
        channel = self.client.get_channel(792627468774670388)
        roles = await self.client.get_guild(676777139776913408).fetch_roles()

        team_message_ids = db["team_message_ids"]
        team_emojis = list(db["team_emojis"].values())

        # get team roles from roles list
        team_roles = []
        for team, message_id in team_message_ids.items():
            for role in roles:
                if role.name == team:
                    team_roles.append(role)
                    break

        # Edit message by message ID
        for i, (team, message_id) in enumerate(team_message_ids.items()):
            team_name = (
                team.split("-")[0].capitalize() + " " + team.split("-")[1].capitalize()
            )
            msg = team_emojis[i] + " **" + team_name + "** " + team_emojis[i] + "\n"

            for i, mem in enumerate(team_roles[i].members):
                msg += str(i + 1) + ". " + mem.mention + "\n"

            if msg == team_name:
                msg += "1. No one"

            msg += "\n"
            message = await channel.fetch_message(message_id)
            await message.edit(content=msg)

    @tasks.loop(hours=3)
    async def update_team_list(self):
        """
        Update villian teams list every 3 hours

        :param self: Villian class
        """
        await self.update_vt_list()

    @commands.command()
    @commands.is_owner()
    async def update_team_list_owner(self, ctx):
        """
        Update villian teams list via command 

        :param self: Villian class
        :param ctx: Discord.py command context
        """
        await self.update_vt_list()
        await ctx.send("Updated!")


def setup(client):
    """
    Add Villian extension/cog to client

    :param client: Discord.py bot client
    """
    client.add_cog(Villain(client))
