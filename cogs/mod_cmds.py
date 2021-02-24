import discord
from discord.ext import commands
import asyncio


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

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


def setup(client):
    client.add_cog(Mod(client))
