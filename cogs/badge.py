import discord
from discord.ext import commands
from replit import db
import asyncio

def server_prefix(msg):

    if isinstance(msg.message.channel, discord.channel.DMChannel):
        return "."
        
    prefixes = db["prefixes"]
    s_prefix = prefixes[str(msg.guild.id)]

    return s_prefix

elite_streak = {
    "0": "<:pokeball:790056814216740874>",
    "1": "<:greatball:792262525835018250>",
    "2": "<:ultraball:790056815652110386>",
    "3": "<:masterball:790056815173828628>"
}

channelID = int()


class League(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cog_check(self, ctx):

        if isinstance(ctx.channel, discord.channel.DMChannel):

            raise commands.NoPrivateMessage("This command can't be used in DM.")
        else:
            return True

    @commands.command(aliases=["aw", "badgea"])
    async def award(self, ctx, member: discord.Member, badge = None):

        obtained = []

        data = db["badges"]
        gl = db["league"]

        if str(ctx.guild.id) not in data or str(ctx.guild.id) not in gl:
            return

        if gl[str(ctx.guild.id)]["glrole"] != "":

            role = ctx.guild.get_role(int(gl[str(ctx.guild.id)]["glrole"]))
            if role:
                if role in ctx.author.roles or ctx.author.guild_permissions.manage_guild:
                    pass
                else:
                    return await ctx.send("You don't have permission to use this command.")
            else:
                if ctx.author.guild_permissions.manage_guild:
                    pass
                else:
                    return await ctx.send("You don't have permission to use this command.")

        else:
            if ctx.author.guild_permissions.manage_guild:
                pass
            else:
                return await ctx.send("You don't have permission to use this command.")

        if member == ctx.author:
            return await ctx.send("You cannot give yourself a badge...")

        if member.bot:
            return await ctx.send("How high you are?\nNub giving Badge to Bot")

        if str(member.id) not in data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)][str(member.id)] = {
            "Badges": list(),
            "Elite_Streak": list()
        }

        if badge is None:
            try:
                badge = gl[str(ctx.guild.id)]["gymleaders"][str(ctx.author.id)]
            except KeyError:
                return await ctx.send("You have to define a badge name.")

        badge = badge.lower()

        badges_dict = gl[str(ctx.guild.id)]["cbadges"]

        if badge not in badges_dict:
            return await ctx.send(f"{badge} is not a valid badge for this server.")

        for a in data[str(ctx.guild.id)][str(member.id)]["Badges"]:
            obtained.append(a)

        if badges_dict[badge] in obtained:
            return await ctx.send(f"{member} already has the badge.")

        b = badges_dict[badge]
        obtained.append(b)

        data[str(ctx.guild.id)][str(member.id)]["Badges"] = obtained

        db["badges"] = data

        return await ctx.send(
            f"{member.mention} won {badges_dict[badge]} Badge")


    @commands.command(aliases=["rv"])
    async def revoke(self, ctx, member: discord.Member, badge):

        obtained = []

        data = db["badges"]
        gl = db["league"]

        badge = badge.lower()

        if str(ctx.guild.id) not in data or str(ctx.guild.id) not in gl:
            return

        if gl[str(ctx.guild.id)]["glrole"] != "":

            role = ctx.guild.get_role(int(gl[str(ctx.guild.id)]["glrole"]))
            if role:
                if role in ctx.author.roles or ctx.author.guild_permissions.manage_guild:
                    pass
                else:
                    return await ctx.send("You don't have permission to use this command.")
            else:
                if ctx.author.guild_permissions.manage_guild:
                    pass
                else:
                    return await ctx.send("You don't have permission to use this command.")

        else:
            if ctx.author.guild_permissions.manage_guild:
                pass
            else:
                return await ctx.send("You don't have permission to use this command.")

        if str(member.id) not in data[str(ctx.guild.id)]:
            return await ctx.send(f"{member.mention} has not started challenging gym yet.")

        for a in data[str(ctx.guild.id)][str(member.id)]["Badges"]:
            obtained.append(a)

        badges_dict = gl[str(ctx.guild.id)]["cbadges"]

        if badges_dict[badge] not in obtained:
            return await ctx.send(f"{member} don't have the badge.")

        obtained.remove(badges_dict[badge])

        data[str(ctx.guild.id)][str(member.id)]["Badges"] = obtained

        db["badges"] = data

        return await ctx.send(
            f"{badges_dict[badge]} was removed from {member.mention}.")


    @commands.command(aliases=["streakadd", "streaka"])
    async def streak_add(self, ctx, *, member: discord.Member):

        if member == ctx.author:
            return await ctx.send("You cannot add yourself an elite streak...")

        obtained = []

        data = db["badges"]
        gl = db["league"]

        if str(ctx.guild.id) not in data or str(ctx.guild.id) not in gl:
            return

        if gl[str(ctx.guild.id)]["erole"] != "":

            role = ctx.guild.get_role(int(gl[str(ctx.guild.id)]["erole"]))
            if role:
                if role in ctx.author.roles or ctx.author.guild_permissions.manage_guild:
                    pass
                else:
                    return await ctx.send("You don't have permission to use this command.")
            else:
                if ctx.author.guild_permissions.manage_guild:
                    pass
                else:
                    return await ctx.send("You don't have permission to use this command.")

        else:
            if ctx.author.guild_permissions.manage_guild:
                pass
            else:
                return await ctx.send("You don't have permission to use this command.")

        won = 0

        if str(member.id) not in data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)][str(member.id)] = {
            "Badges": list(),
            "Elite_Streak": list()
        }

        for streaks in data[str(ctx.guild.id)][str(member.id)]["Elite_Streak"]:
            won += 1
            obtained.append(streaks)

        if won == 4:
            return await ctx.send(f"{member} has already completed elite streak.")

        if won < 4:
            obtained.append(elite_streak[str(won)])

        data[str(ctx.guild.id)][str(member.id)]["Elite_Streak"] = obtained

        db["badges"] = data

        return await ctx.send(
            f"{member.mention}'s Elite Streak increased to {elite_streak[str(won)]}"
        )
        

    @commands.command(aliases=["streakremove", "streakr"])
    async def streak_reset(self, ctx, member: discord.Member):

        empty_list = []

        data = db["badges"]
        gl = db["league"]

        if str(ctx.guild.id) not in data or str(ctx.guild.id) not in gl:
            return

        if gl[str(ctx.guild.id)]["erole"] != "":

            role = ctx.guild.get_role(int(gl[str(ctx.guild.id)]["erole"]))
            if role:
                if role in ctx.author.roles or ctx.author.guild_permissions.manage_guild:
                    pass
                else:
                    return await ctx.send("You don't have permission to use this command.")
            else:
                if ctx.author.guild_permissions.manage_guild:
                    pass
                else:
                    return await ctx.send("You don't have permission to use this command.")

        else:
            if ctx.author.guild_permissions.manage_guild:
                pass
            else:
                return await ctx.send("You don't have permission to use this command.")

        if str(member.id) not in data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)][str(member.id)] = {
            "Badges": list(),
            "Elite_Streak": list()
        }

        data[str(ctx.guild.id)][str(member.id)]["Elite_Streak"] = empty_list

        db["badges"] = data

        await ctx.send(
            f"{member.mention}'s Elite Streak has been reseted."
        )


    @commands.command(aliases=[])
    async def badges(self, ctx, *, member: discord.Member = None):

        if member is None:
            member = ctx.author

        badge_str = ""
        streak = ""

        data = db["badges"]

        if str(ctx.guild.id) not in data:
                return

        if str(member.id) not in data[str(ctx.guild.id)]:
            badge = []
            es = []

        else:
            badge = data[str(ctx.guild.id)][str(member.id)]["Badges"]
            es = data[str(ctx.guild.id)][str(member.id)]["Elite_Streak"]

        for i in badge:
            badge_str += i + " "

        for i in es:
            streak += i + " "        

        em = discord.Embed(title = f"{member}'s Profile", colour=discord.Color.orange())

        em.set_author(icon_url=ctx.guild.icon_url, name=f"{ctx.guild.name}'s")

        em.set_thumbnail(url=member.avatar_url)

        if badge_str == "":
            badge_str = "\u200b"

        if streak == "":
            streak = "\u200b"

        em.add_field(name="Gym Badges:", value=badge_str, inline=False)   
        em.add_field(name="Elite Streak:", value=streak, inline=False)

        await ctx.send(embed=em)

    @commands.command(aliases=["glrole", "leaderrole"])
    @commands.has_permissions(manage_guild=True)
    async def gl_role(self, ctx, *, role: discord.Role):

        data = db["league"]
        data1 = db["badges"]

        if str(ctx.guild.id) not in data:
            data[str(ctx.guild.id)] = {
                "glrole": "",
                "erole": "",
                "cbadges": {},
                "gymleaders": {}
            }
            data1[str(ctx.guild.id)] = {}

        data[str(ctx.guild.id)]["glrole"] = str(role.id)

        db["league"] = data
        db["badges"] = data1

        return await ctx.send(f"Gym Leader role was set to {role.name}")

    @commands.command(aliases=["elrole", "eliterole"])
    @commands.has_permissions(manage_guild=True)
    async def elite_role(self, ctx, *, role: discord.Role):

        data = db["league"]
        data1 = db["badges"]

        if str(ctx.guild.id) not in data:
            data[str(ctx.guild.id)] = {
                "glrole": "",
                "erole": "",
                "cbadges": {},
                "gymleaders": {}
            }
            data1[str(ctx.guild.id)] = {}

        data[str(ctx.guild.id)]["erole"] = str(role.id)

        db["league"] = data
        db["badges"] = data1

        return await ctx.send(f"Elites role was set to {role.name}")

    @commands.command(aliases=["badgen"])
    @commands.has_permissions(manage_guild=True)
    async def badgenew(self, ctx, name, badge):

        data = db["league"]
        data1 = db["badges"]

        name = name.lower()

        if str(ctx.guild.id) not in data:
            data[str(ctx.guild.id)] = {
                "glrole": "",
                "erole": "",
                "cbadges": {},
                "gymleaders": {}
            }
            data1[str(ctx.guild.id)] = {}
        
        if name in data[str(ctx.guild.id)]["cbadges"]:
            await ctx.send(f"One Badge with name {name} already exists. Do you want to overwrite it?(Y/N)")
            try:
                def check(ms):
                    return ms.author == ctx.author and ms.channel == ctx.channel

                user = await self.client.wait_for("message",
                                                        check=check,
                                                        timeout=30.0)

                user = user.content.lower()
                if user == "y":
                    data[str(ctx.guild.id)]["cbadges"][name] = str(badge)
                    return await ctx.send(f"{badge} added as {name.capitalize()} Badge")
                else:
                    return await ctx.send("Returning...")

            except asyncio.TimeoutError:
                return
        
        data[str(ctx.guild.id)]["cbadges"][name] = str(badge)

        db["league"] = data
        db["badges"] = data1

        return await ctx.send(f"{badge} added as {name.capitalize()} Badge")

    
    @commands.command(aliases=["leada"])
    @commands.has_permissions(manage_guild=True)
    async def leaderadd(self, ctx, member:discord.Member, badge):

        badge = badge.lower()

        data = db["league"]

        if str(ctx.guild.id) not in data:
            return await ctx.send("Set up Gym Badges First.")
        
        if badge not in data[str(ctx.guild.id)]["cbadges"]:
            return await ctx.send("Set up Gym Badges First.")

        if str(member.id) in data[str(ctx.guild.id)]["gymleaders"]:
            return await ctx.send("User is already a Gym Leader.")

        data[str(ctx.guild.id)]["gymleaders"][str(member.id)] = badge

        db["league"] = data

        return await ctx.send(f"{member} Became {badge.capitalize()} Gym Leader.")

    @commands.command(aliases=["leadr"])
    @commands.has_permissions(manage_guild=True)
    async def leaderremove(self, ctx, member:discord.Member, badge):

        badge = badge.lower()

        data = db["league"]

        if str(ctx.guild.id) not in data:
            return await ctx.send("There is no Gym Leaders for this server.")
        
        if badge not in data[str(ctx.guild.id)]["cbadges"]:
            return await ctx.send("There is no Gym Leader for this server.")

        if str(member.id) not in data[str(ctx.guild.id)]["gymleaders"]:
            return await ctx.send("User is not a Gym Leader.")

        if data[str(ctx.guild.id)]["gymleaders"][str(member.id)] != badge:
            return await ctx.send(f"{member} is not the {badge.capitalize} Gym Leader.")

        del data[str(ctx.guild.id)]["gymleaders"][str(member.id)]

        db["league"] = data

        return await ctx.send(f"{member} has been removed from {badge.capitalize()} Gym Leader.")

    @commands.command(aliases=["bdrs"])
    @commands.has_permissions(manage_guild=True)
    async def badgereset(self, ctx):

        data = db["league"]
        data1 = db["badges"]

        await ctx.send("Do you want to RESET badges in this server?(Y/N)")
        try:
            def check(ms):
                return ms.author == ctx.author and ms.channel == ctx.channel

            user = await self.client.wait_for("message",
                                                    check=check,
                                                    timeout=30.0)

            user = user.content.lower()

            if user != "y":
                return await ctx.send("Returning...")

        except asyncio.TimeoutError:
            return

        data[str(ctx.guild.id)] = {
                "glrole": "",
                "erole": "",
                "cbadges": {},
                "gymleaders": {}
            }

        data1[str(ctx.guild.id)] = {}

        db["league"] = data
        db["badges"] = data1

        return await ctx.send("Badges Reset Successful")

    @commands.command(aliases=[])
    async def gyms(self, ctx):

        data = db["league"]

        if str(ctx.guild.id) not in data:
            return await ctx.send("There is No Gym Leader for this server yet.")

        if data[str(ctx.guild.id)]["gymleaders"] == {}:
            return await ctx.send("There is No Gym Leader for this server yet.")

        em = discord.Embed(title=f"Gym Leaders of {ctx.guild.name}", colour=discord.Color.orange())

        for i in data[str(ctx.guild.id)]["gymleaders"]:
            user = self.client.get_user(int(i))
            if user:
                em.add_field(name=data[str(ctx.guild.id)]["gymleaders"][i], value=user)

        await ctx.send(embed=em)

    @commands.command(aliases=["serverbadges"])
    async def sbadges(self, ctx):

        data = db["league"]

        if str(ctx.guild.id) not in data:
            return await ctx.send("There is No Badges set for this server yet.")

        if data[str(ctx.guild.id)]["cbadges"] == {}:
            return await ctx.send("There is No Badges set for this server yet.")

        em = discord.Embed(title=f"Badges of {ctx.guild.name}", colour=discord.Color.orange())

        for i in data[str(ctx.guild.id)]["cbadges"]:
            em.add_field(name=f"{i.capitalize()} Badge", value=data[str(ctx.guild.id)]["cbadges"][i])

        await ctx.send(embed=em)

    @commands.command(aliases=[])
    async def badgelb(self, ctx):

        data1 = db["badges"]

        gg = {}

        if str(ctx.guild.id) not in data1:
            return await ctx.send("No server DATA yet")

        if data1[str(ctx.guild.id)] == {}:
            return await ctx.send("No server DATA yet")

        for i in data1[str(ctx.guild.id)]:
            num  = len(data1[str(ctx.guild.id)][i]["Badges"])
            
            if num == 0:
                pass
            else:
                gg[i] = num

        lb = dict(sorted(gg.items(), key = lambda kv:kv[1], reverse = True))

        des = ""
        no = 1

        for i in lb:
            mem = None
            try:
                mem = await ctx.guild.fetch_member(int(i))
            except discord.HTTPException:
                pass

            if mem:

                if no == 1:
                    des += "🥇 "
                elif no == 2:
                    des += "🥈 "
                elif no == 3:
                    des += "🥉 "
                else:
                    des += "👏 "

                
                wins = lb[i]
                des += f"**{wins}** Badges - {mem}\n"
                no += 1
                if no > 10:
                    break

        em = discord.Embed(title=f"Badge Leaderboard", description=des, colour=discord.Color.orange())

        em.set_author(icon_url=ctx.guild.icon_url, name=f"{ctx.guild.name}'s")

        await ctx.send(embed=em)

    @commands.command(aliases=["badger"])
    @commands.has_permissions(manage_guild=True)
    async def badgerem(self, ctx, name):

        data = db["league"]
        data1 = db["badges"]

        name = name.lower()

        if str(ctx.guild.id) not in data:
            return await ctx.send()

        if data[str(ctx.guild.id)]["cbadges"] == {}:
            return await ctx.send()

        if name not in data[str(ctx.guild.id)]["cbadges"]:
            return
        
        del data[str(ctx.guild.id)]["cbadges"][name]

        db["league"] = data
        db["badges"] = data1

        return await ctx.send(f"{name} has been removed from Server Badges.")

def setup(client):
    client.add_cog(League(client))
