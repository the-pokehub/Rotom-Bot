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


    async def up_lst(self):

        # TODO if possible can help to dynamically get guild id, im too lazy to look into it
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
            team_name = team.split('-')[0].capitalize() + ' ' + team.split('-')[1].capitalize()
            msg = team_emojis[i] + ' **' + team_name + '** ' + team_emojis[i] + '\n'
            
            for i, mem in enumerate(team_roles[i].members):
                msg += str(i+1) + '. ' + mem.mention + '\n'
            
            if msg == team_name:
                msg += '1. No one'

            msg += '\n'
            message = await channel.fetch_message(message_id)
            await message.edit(content=msg)


    # @commands.command(aliases=["jointeam", "jt"])
    # async def join_team(self, ctx, *, text = ''):

    #     if ctx.channel.id != 791488051410239518:
    #         return

    #     # check if team parameter is given
    #     if text == '':
    #         embed = discord.Embed(
    #                 description=f"**Add a team name behind `.jointeam` to join villian teams. The available villian teams are:**\nTeam Rocket <:rocket:889828530039431209>\nTeam Magma <:magma:889828723963084840>\nTeam Galactic <:galactic:889828637698846760>\nTeam Plasma <:plasma:889828464385994763>\nTeam Skull <:skull:889828839541338163>\n\n**To leave your current team, type `.jointeam none`**",
    #                 colour=discord.Colour.blue())

    #         msg = await ctx.send(embed=embed)

    #         # await asyncio.sleep(10)
    #         # try:
    #         #     await msg.delete()
    #         # except discord.errors.NotFound:
    #         #     pass
                
    #         return

    #     async def rm_role():
    #         for team, role_id in team_role_ids.items():

    #             if role_id in [role.id for role in ctx.author.roles]:
    #                 role_remove = discord.utils.get(ctx.guild.roles, id=role_id)

    #                 await ctx.author.remove_roles(role_remove)
                    

    #     # check if user wants to leave his current team without a joining new team
    #     team_role_ids = db["team_role_ids"]
    #     if text.lower() == 'none':
            
    #         for team, role_id in team_role_ids.items():

    #             if role_id in [role.id for role in ctx.author.roles]:
    #                 role_remove = discord.utils.get(ctx.guild.roles, id=role_id)

    #                 await ctx.author.remove_roles(role_remove)
    #                 await ctx.message.add_reaction('👋')
    #                 return

    #         embed = discord.Embed(
    #                 description=f"**You are currently not in any team!**",
    #                 colour=discord.Colour.blue())

    #         msg = await ctx.send(embed=embed)

    #         # await asyncio.sleep(10)
    #         # try:
    #         #     await msg.delete()
    #         # except discord.errors.NotFound:
    #         #     pass
    #         return
                    
    #     # check if member is currently in that team
    #     rm = ["team", "-", " "]
    #     for i in rm:
    #         text = text.lower().replace(i, "")
    #     text = 'team-' + text
    #     if text.lower() in [role.name.lower() for role in ctx.author.roles]:
    #         embed = discord.Embed(
    #                 description=f"**You are currently in that team!**",
    #                 colour=discord.Colour.blue())

    #         msg = await ctx.send(embed=embed)

    #         # await asyncio.sleep(10)
    #         # try:
    #         #     await msg.delete()
    #         # except discord.errors.NotFound:
    #         #     pass
    #         return
        
    #     # check if team joining is in roles list
    #     team_role_ids = db["team_role_ids"]
    #     if text.lower() not in list(team_role_ids.keys()):
    #         embed = discord.Embed(
    #                 description=f"**This team does not exist.**",
    #                 colour=discord.Colour.blue())

    #         msg = await ctx.send(embed=embed)

    #         # await asyncio.sleep(10)
    #         # try:
    #         #     await msg.delete()
    #         # except discord.errors.NotFound:
    #         #     pass
    #         return

    #     # check if join team timer is reached
    #     grunt_timers = db["grunt_timers"]
    #     timer = grunt_timers.get(str(ctx.author.id))
        
    #     if str(ctx.author.id) in grunt_timers:
    #         time_limit = 86400   # in seconds
    #         if round(time.time()) - timer < time_limit:
    #             time_remaining = time_limit - (round(time.time()) - timer)

    #             hrs = floor(time_remaining/3600)
    #             mins = floor((time_remaining - hrs*3600)/60)
    #             secs = (time_remaining - hrs*3600 - mins*60)

    #             if hrs == 0 and mins == 0:
    #                 description = f"**Please wait for another {secs} sec before changing your team.**"
    #             else:
    #                 description = f"**Please wait for another {hrs} hr {mins} min before changing your team.**"

    #             embed = discord.Embed(
    #             description=description,
    #             colour=discord.Colour.blue())

    #             msg = await ctx.channel.send(embed=embed)

    #             # await asyncio.sleep(10)
    #             # try:
    #             #     await msg.delete()
    #             # except discord.errors.NotFound:
    #             #     print('error')
    #             #     pass
    #             return
        
    #     # transfer from one team to another
    #     grunt_timers[str(ctx.author.id)] = round(time.time())
        
    #     await rm_role()

    #     # add new role
    #     role_add = discord.utils.get(ctx.guild.roles, name=text)
    #     await ctx.author.add_roles(role_add)
    #     await ctx.message.add_reaction('👍')
    #     db["grunt_timers"] = grunt_timers

    #     await self.up_lst()
        
    #     return


    @tasks.loop(hours=3)
    async def update_team_list(self):

        await self.up_lst()

    @commands.command()
    @commands.is_owner()
    async def upvt(self, ctx):
        await self.up_lst()
        await ctx.send("Updated!")

            
def setup(client):
    client.add_cog(Villain(client))