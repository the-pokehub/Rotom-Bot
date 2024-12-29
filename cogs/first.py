import discord as discord
from discord.ext import commands
import requests


class Setup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="userbanner", aliases=['ub'])
    async def userbanner(self, ctx, *, member: discord.Member = None):
        "See your or the mentioned user's profile banner."

        if member is None:
            member = ctx.author.id
        else:
            member = member.id

        mem = await self.client.fetch_user(member)

        em = discord.Embed(title=f"{mem}'s Banner")

        try:
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar)
        except Exception:
            return

        try:
            em.set_image(url=mem.banner)

            await ctx.send(embed=em)
        except Exception:
            await ctx.send(f"{mem} have no Banner.")

    @commands.hybrid_command(name="avatar", aliases=["av"])
    async def avatar(self, ctx, *, member: discord.Member = None):

        "See your or the mentioned user's profile picture."

        if member is None:
            member = ctx.author

        em = discord.Embed(title=f"{member}'s Avatar")
        em.set_image(url=member.display_avatar)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar)

        await ctx.send(embed=em)

    @commands.hybrid_command(name="calculate", aliases=["c", "calculator"])
    async def calculate(self, ctx, expression):

        "Calculate the given expression."

        await ctx.send(eval(str(expression), {"__builtins__": None}, {}))

    @commands.hybrid_command(name="banner")
    async def banner(self, ctx):

        "Check the server's banner, if any."

        em = discord.Embed(title=f"{ctx.guild.name}'s Banner")
        url = ctx.guild.banner
        if url:
            url.replace(format="png")
            finalurl = url.url
            finalurl = finalurl.replace("png", "gif")
            get = requests.get(finalurl).status_code
            if get != 200:
                finalurl = url.url
        else:
            return await ctx.send(f"{ctx.guild.name} has no banner.")

        em.set_image(url=finalurl)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar)

        await ctx.send(embed=em)

    @commands.hybrid_command(name="serverinfo")
    async def serverinfo(self, ctx):

        "Get info about the server."

        desc = ctx.guild.description

        if desc:

            embed = discord.Embed(
                title=ctx.guild.name + " Server Information",
                description=desc,
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title=ctx.guild.name + " Server Information",
                color=discord.Color.green()
            )

        channel = len(ctx.guild.channels)
        vc = len(ctx.guild.voice_channels)
        booster = len(ctx.guild.premium_subscribers)
        roles = len(ctx.guild.roles)
        lvl = ctx.guild.premium_tier
        boosts = ctx.guild.premium_subscription_count
        icon = ctx.guild.icon

        url = ctx.guild.banner
        if url:
            url.replace(format="png")
            finalurl = url.url
            finalurl = finalurl.replace("png", "gif")
            get = requests.get(finalurl).status_code
            if get != 200:
                finalurl = url.url
        else:
            finalurl = None

        info = f"Verification Level: {ctx.guild.verification_level}"

        if finalurl:
            info += f"\n[Banner]({finalurl})"
        if icon:
            info += f"\n[Icon]({icon.url})"
            embed.set_thumbnail(url=icon.url)

        embed.add_field(name="Owner:", value=ctx.guild.owner)

        embed.add_field(name="Server ID:", value=ctx.guild.id)

        # embed.add_field(name="Region:", value=str(ctx.guild.region).capitalize())

        embed.add_field(name="Member Count:", value=ctx.guild.member_count)

        embed.add_field(name="Server Boosts:", value=f"Level: {lvl}\nBoosts: {boosts}\nBoosters: {booster}")

        embed.add_field(name="Channels:", value=f"Text: {channel}\nVoice: {vc}")

        embed.add_field(name="Roles:", value=roles)

        embed.add_field(name="Emojis:", value=len(ctx.guild.emojis))

        embed.add_field(name="Other Infos:", value=info)

        embed.set_footer(text="Created on:")
        embed.timestamp = ctx.guild.created_at

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Setup(client))
