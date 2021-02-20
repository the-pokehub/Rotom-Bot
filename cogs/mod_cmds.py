import discord
from discord.ext import commands
import json
import os
import asyncio

with open("mod.json", "r") as mod_data:
    save = json.load(mod_data)

current_prefix = str(save["prefix"])


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["sc"])
    @commands.has_any_role("moderator", "admin")
    async def swap_close(self, ctx):

        with open("mod.json", "r") as bot_data:
            data = json.load(bot_data)

        data["start"] = "yes"
        with open("mod.json", "w") as bot_data:
            json.dump(data, bot_data, indent=4)

        await ctx.send("Pokémon Swap has been closed now")

    @commands.command(aliases=["rl"])
    @commands.has_any_role("moderator", "admin")
    async def restart_league(self, ctx, *, title):

        with open("gen6.json", "r") as bot_data:
            data = json.load(bot_data)

        for items in data:
            achievements = data[items]["Achievements"]
            data[items] = {
                "Registered": list(),
                "Badges": list(),
                "Elite_Streak": list(),
                "Reset_Token": 1,
                "Achievements": list()
            }
            with open("gen6.json", "w") as bot_data:
                json.dump(data, bot_data, indent=4)
            data[items]["Achievements"] = achievements
            with open("gen6.json", "w") as bot_data:
                json.dump(data, bot_data, indent=4)

        with open("gen7.json", "r") as bot_data:
            data = json.load(bot_data)

        for items in data:
            achievements = data[items]["Achievements"]
            data[items] = {
                "Registered": list(),
                "Badges": list(),
                "Elite_Streak": list(),
                "Reset_Token": 1,
                "Achievements": list()
            }
            with open("gen7.json", "w") as bot_data:
                json.dump(data, bot_data, indent=4)
            data[items]["Achievements"] = achievements
            with open("gen7.json", "w") as bot_data:
                json.dump(data, bot_data, indent=4)

        with open("mod.json", "r") as bot_data:
            data = json.load(bot_data)

        data["start"] = "no"

        with open("mod.json", "w") as bot_data:
            json.dump(data, bot_data, indent=4)

        data["current_league"] = title
        with open("mod.json", "w") as bot_data:
            json.dump(data, bot_data, indent=4)

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.client.unload_extension(f"cogs.{filename[:-3]}")
                self.client.load_extension(f"cogs.{filename[:-3]}")

        await ctx.send("League data has been reseted.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):

        if ctx.author == member:
            await ctx.send("You cannot kick yourself.")
            return

        role = discord.utils.get(ctx.guild.roles, name="moderator")

        if role in member.roles:
            await ctx.send("You cannot kick a Moderator.")
            return

        if member == ctx.guild.owner:
            await ctx.send("You cannot kick the owner of the server.")
            return

        if reason is None:
            await ctx.send(f"{member.mention} has been kicked from the server.")
            await member.send(f"You have been kicked from {ctx.guild.name}")
        else:
            await ctx.send(f"{member.mention} has been kicked from the server for {reason}")
            await member.send(f"You have been kicked from {ctx.guild.name} for {reason}")

        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason):

        if ctx.author == member:
            await ctx.send("You cannot ban yourself.")
            return

        role = discord.utils.get(ctx.guild.roles, name="moderator")

        if role in member.roles:
            await ctx.send("You cannot ban a Moderator.")
            return

        if member == ctx.guild.owner:
            await ctx.send("You cannot kick the owner of the server.")
            return

        if reason is None:
            await ctx.send(f"{member.mention} has been banned from the server.")
            await member.send(f"You have been banned from {ctx.guild.name}")
        else:
            await ctx.send(f"{member.mention} has been banned from the server for {reason}")
            await member.send(f"You have been banned from {ctx.guild.name} for {reason}")

        await member.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"I have deleted {amount} messages.")
        await asyncio.sleep(3)
        await msg.delete()

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def emoji(self, ctx, ji: discord.Emoji):
        await ctx.send(f"ID: {ji.id}, Emoji: `{ji}`")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def history(self, ctx, member: discord.Member):
        async for msg in member.history(limit=1):
            await ctx.send(msg.content)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, new_prefix):

        global current_prefix


def setup(client):
    client.add_cog(Mod(client))
