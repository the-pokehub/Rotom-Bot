from discord.ext import commands
import discord
from replit import db
import datetime
import shutil
import requests


def load(url, path, guild):

    r = requests.get(url, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True

        if "png" in url:
            with open(f"{guild}/{path}.png", 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        elif "gif" in url:
            with open(f"{guild}/{path}.gif", 'wb') as f:
                shutil.copyfileobj(r.raw, f)


class Logger(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_invite_create(self, invite):

        if invite.guild.id not in [676777139776913408, 782112126579114026, 770846450896470046]:
            return

        inv = db["invites"]
        inv[invite.code] = invite.uses
        db["invites"] = inv

    @commands.Cog.listener()
    async def on_member_join(self, member):

        if member.guild.id not in [676777139776913408, 782112126579114026, 770846450896470046]:
            return

        inv = db["invites"]
        invite = None

        invites = await member.guild.invites()

        for i in invites:
            for j in inv:
                if i.code == j:
                    if i.uses != inv[j]:
                        if inv[j] + 1 == i.uses:
                            invite = i
                            inv[j] += 1

        db["invites"] = inv

        em = discord.Embed(color=discord.Color.green(), description=f"{member.mention} {member}")

        timesta = int(datetime.datetime.timestamp(member.created_at))

        em.add_field(name="Account Created at", value=f"<t:{timesta}:F>", inline=False)

        if invite:
            em.add_field(name="Inviter", value=f"{invite.inviter.mention}")

        em.set_author(name="Member Joined", icon_url=member.display_avatar)

        em.set_footer(text=f"ID: {member.id}")
        em.timestamp = member.joined_at
        em.set_thumbnail(url=member.display_avatar)

        channel = await self.client.fetch_channel(780981187317465119)
        await channel.send(embed=em)

    @commands.hybrid_command(name="whois")
    async def whois(self, ctx, member: discord.Member = None):

        if not member:
            member = ctx.author

        em = discord.Embed(color=member.color, description=f"{member.mention}")

        em.set_author(name=member, icon_url=member.display_avatar)
        em.set_thumbnail(url=member.display_avatar)

        joined = int(datetime.datetime.timestamp(member.joined_at))
        created = int(datetime.datetime.timestamp(member.created_at))
        em.add_field(name="Joined", value=f"<t:{joined}:F>")
        em.add_field(name="Registered", value=f"<t:{created}:F>")

        roles = ""

        for i in reversed(member.roles):
            if i.name == "@everyone":
                pass
            else:
                roles += f" {i.mention}"

        key_perm = {"kick_members": "Kick Members", "ban_members": "Ban Members", "administrator": "Administrator", "manage_channels": "Manage Channels", "manage_guild": "Manage Server", "manage_messages": "Manage Messages", "mention_everyone": "Mention Everyone", "manage_nicknames": "Manage Nicknames", " manage_roles": "Manage Roles", "manage_webhooks": "Manage Webhooks", "manage_emojis": "Manage Emojis", "manage_events": "Manage Events", "manage_threads": "Manage Threads"}

        perms = ""
        for i in member.guild_permissions:
            if i[1]:
                if i[0] in key_perm:
                    perms += key_perm[i[0]] + ", "

        # print(perms)

        if roles:
            em.add_field(name="Roles", value=roles, inline=False)
        if perms:
            em.add_field(name="Key Permissions", value=perms[:-2], inline=False)

        em.set_footer(text=f"ID: {member.id}")
        em.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=em)


async def setup(client):
    await client.add_cog(Logger(client))
