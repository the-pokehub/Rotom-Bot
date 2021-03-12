import json
import discord
from discord.ext import commands
import asyncio
import os

with open("mod.json", "r") as mod_data:
    save = json.load(mod_data)


def server_prefix(msg):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
        s_prefix = prefixes[str(msg.guild.id)]

    return s_prefix


current_title = str(save["current_league"])

badges_dict6 = dict(save["gen6_badges"])

badges_dict7 = dict(save["gen7_badges"])

elite_streak = {
    "0": "<:pokeball:790056814216740874>",
    "1": "<:greatball:792262525835018250>",
    "2": "<:ultraball:790056815652110386>",
    "3": "<:masterball:790056815173828628>"
}


class League(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ab"])
    @commands.has_any_role("gym-leaders", "admin", "moderator")
    async def add_badge(self, ctx, generation, member: discord.Member, badge):

        prefix = server_prefix(ctx)

        obtained = []
        valid_badges = []
        empty_list = []
        channel = self.client.get_channel(802027595302174730)

        if ctx.channel.name == "📝registration":
            return

        if member == ctx.author:
            await ctx.send("You cannot give yourself a badge...")
            return

        if generation == "6":
            data_file = "gen6.json"
            badges_dict = badges_dict6
            prof_file = "league_prof6.json"
        elif generation == "7":
            data_file = "gen7.json"
            badges_dict = badges_dict7
            prof_file = "league_prof7.json"
        else:
            await ctx.send(
                f"Enter a valid Generation(6/7)\nUse `{prefix}help ab` to know more."
            )
            return

        for key in badges_dict.keys():
            valid_badges.append(key.capitalize())

        badge_str = ", ".join(valid_badges)

        if badge not in badges_dict:
            await ctx.send(
                f"{badge.capitalize()} Badge is not available\nAvailable Badges:\n{badge_str}"
            )
            return

        async def ab():
            with open(data_file, "r") as badge_data:
                data1 = json.load(badge_data)

                if str(member.id) not in data1:
                    await ctx.send(
                        f"{member} is not registered for this generation.")
                    return

                if data1[str(member.id)]["Registered"] == empty_list:
                    await ctx.send(
                        f"{member} is not registered for this generation.")
                    return

                for a in data1[str(member.id)]["Badges"]:
                    obtained.append(a)

                if badges_dict[badge] in obtained:
                    await ctx.send(f"{member} already has the badge.")
                    return

                b = badges_dict[badge]
                obtained.append(b)

                data1[str(member.id)]["Badges"] = obtained
                with open(data_file, "w") as badge_data1:
                    json.dump(data1, badge_data1, indent=4)

            await ctx.send(f"{member}'s profile has been updated.")
            await channel.send(
                f"{member.mention} won {badges_dict[badge]} Badge")
            return

        role1 = discord.utils.get(ctx.guild.roles, name="gym-leaders")
        role2 = discord.utils.get(ctx.guild.roles, name="elites")

        if role1 in member.roles:
            try:
                with open(prof_file, "r") as bot_data:
                    data = json.load(bot_data)

                for badges in data["gym-leaders"][str(member.id)]["Badges"]:
                    obtained.append(badges)

                if badges_dict[badge] in obtained:
                    await ctx.send(f"{member} already has the badge.")
                    return

                new_badge = badges_dict[badge]
                obtained.append(new_badge)

                data["gym-leaders"][str(member.id)]["Badges"] = obtained

                with open(prof_file, "w") as bot_data:
                    json.dump(data, bot_data, indent=4)

            except KeyError:
                await ab()

        elif role2 in member.roles:

            try:
                with open(prof_file, "r") as bot_data:
                    data = json.load(bot_data)

                for badges in data["elites"][str(member.id)]["Badges"]:
                    obtained.append(badges)

                if badges_dict[badge] in obtained:
                    await ctx.send(f"{member} already has the badge.")
                    return

                new_badge = badges_dict[badge]
                obtained.append(new_badge)

                data["elites"][str(member.id)]["Badges"] = obtained
                with open(prof_file, "w") as bot_data:
                    json.dump(data, bot_data, indent=4)

            except KeyError:
                await ab()

        else:
            await ab()

    @commands.command(aliases=["as"])
    @commands.has_any_role("elites", "admin", "moderator")
    async def add_streak(self, ctx, generation, *, member: discord.Member):

        prefix = server_prefix(ctx)

        if ctx.channel.name == "📝registration":
            return

        if member == ctx.author:
            await ctx.send("You cannot add yourself an elite streak...")
            return

        if generation == "6":
            data_file = "gen6.json"
            prof_file = "league_prof6.json"
        elif generation == "7":
            data_file = "gen7.json"
            prof_file = "league_prof7.json"
        else:
            await ctx.send(
                f"Enter a valid Generation(6/7)\nUse `{prefix}help as` to know more."
            )
            return

        obtained = []
        empty_list = []
        channel = self.client.get_channel(802027595302174730)

        role1 = discord.utils.get(ctx.guild.roles, name="gym-leaders")
        role2 = discord.utils.get(ctx.guild.roles, name="elites")

        async def a_s():
            won = 0

            with open(data_file, "r") as bot_data:
                data = json.load(bot_data)

            if str(member.id) not in data:
                await ctx.send(
                    f"{member} is not registered for this generation.")
                return

            if data[str(member.id)]["Registered"] == empty_list:
                await ctx.send(
                    f"{member} is not registered for this generation.")
                return

            for streaks in data[str(member.id)]["Elite_Streak"]:
                won += 1
                obtained.append(streaks)

            if won == 4:
                await ctx.send(f"{member} has already completed elite streak.")
                return

            if won <= 4:
                obtained.append(elite_streak[str(won)])

            data[str(member.id)]["Elite_Streak"] = obtained

            with open(data_file, "w") as bot_data:
                json.dump(data, bot_data, indent=4)

            await ctx.send(f"{member}'s Profile has been Updated")
            await channel.send(
                f"{member.mention}'s Generation {generation} Elite Streak increased to {elite_streak[str(won)]}"
            )

            return

        if role1 in member.roles:
            try:
                with open(prof_file, "r") as prof_data:
                    data1 = json.load(prof_data)

                if data1['gym-leaders'][str(member.id)]:
                    pass

                await ctx.send("Gym-Leaders cannot challenge Elites")
                return

            except KeyError:
                await a_s()

        elif role2 in member.roles:
            try:
                with open(prof_file, "r") as prof_data:
                    data1 = json.load(prof_data)

                if data1['elites'][str(member.id)]:
                    pass

                await ctx.send("Elites cannot challenge Elites")
                return

            except KeyError:
                await a_s()

        else:
            await a_s()

    @commands.command(aliases=["p", "summary"])
    async def profile(self, ctx, generation, *, member: discord.Member = None):

        prefix = server_prefix(ctx)

        if ctx.channel.name == "📝registration":
            return

        if generation == "6":
            data_file = "gen6.json"
            prof_file = "league_prof6.json"
        elif generation == "7":
            data_file = "gen7.json"
            prof_file = "league_prof7.json"

        else:
            await ctx.send(
                f"Enter a valid Generation(6/7)\nUse `{prefix}help profile` to know more."
            )
            return

        if member is None:
            member = ctx.author
        else:
            pass

        total = 0
        badges_list = []
        titles = []

        embed = discord.Embed(
            title=f"**{current_title}**\n{member.name}'s Generation {generation} Profile",
            colour=discord.Colour.green())

        async def pf():
            total2 = 0
            badges_list2 = []
            streak = 0
            streak_list = []
            titles2 = []
            empty_list = []
            with open(data_file, "r") as bot_data2:
                data2 = json.load(bot_data2)

            if str(member.id) not in data2:
                await ctx.send(
                    f"{member} is not registered for the current generation.")
                return

            if data2[str(member.id)]["Registered"] == empty_list:
                await ctx.send(
                    f"{member} is not registered for the current generation.")
                return

            embed.set_thumbnail(url=member.avatar_url)

            if data2[str(member.id)]["Reset_Token"] == 0:
                emoji = "<:reset:794439173871239219>"
            else:
                emoji = ""

            for badges2 in data2[str(member.id)]["Badges"]:
                total2 += 1
                badges_list2.append(badges2)

            if total2 == 0:
                embed.add_field(name=f"**{emoji} Gym Badges:** {total2}",
                                value="\u200b\n",
                                inline=False)
            else:
                embed.add_field(name=f"**{emoji} Gym Badges:** {total2}",
                                value="**Obtained:**",
                                inline=False)

                for badges2 in data2[str(member.id)]["Badges"]:
                    badge_name2 = badges2.split(":")
                    embed.add_field(
                        name=f"{badge_name2[1].capitalize()} Badge",
                        value=badges2,
                        inline=True)

            with open(data_file, "r") as bot_data2:
                data2 = json.load(bot_data2)
                for streaks in data2[str(member.id)]["Elite_Streak"]:
                    streak += 1
                    streak_list.append(streaks)

            if streak >= 1:
                final_streak = " ".join(streak_list)
                streak_name_list = streak_list[-1]
                streak_name = streak_name_list.split(":")
                embed.add_field(
                    name=f"**{emoji} Elite Beaten: {streak}**",
                    value=f"{streak_name[1].capitalize()} Rank\n{final_streak}",
                    inline=False)

            else:
                embed.add_field(name=f"**{emoji} Elite Beaten: {streak}**",
                                value="\u200b\n",
                                inline=False)

            # tokens = data[str(member.id)]["Reset_Token"]
            # embed.add_field(name=f"Reset Tokens: {tokens}", value="\u200b\n", inline=False)

            for achievements2 in data2[str(member.id)]["Achievements"]:
                titles2.append(achievements2)

            titles_str2 = ", ".join(titles2)

            if len(titles2) >= 1:
                embed.add_field(name="**Achievements:**",
                                value=f"{titles_str2}",
                                inline=False)

            await ctx.send(embed=embed)

        role1 = discord.utils.get(ctx.guild.roles, name="gym-leaders")
        role2 = discord.utils.get(ctx.guild.roles, name="elites")
        role3 = discord.utils.get(ctx.guild.roles, name="champion")
        role4 = discord.utils.get(ctx.guild.roles, name="challengers")

        if role1 in member.roles:  # gym-leaders
            try:
                with open(prof_file, "r") as bot_data:
                    data = json.load(bot_data)

                if {data['gym-leaders'][str(member.id)]['Badge']}:
                    pass

                name = str({data['gym-leaders'][str(member.id)]['Badge']})

                embed.set_thumbnail(url=member.avatar_url)

                embed.add_field(name="**Status:**",
                                value="<@&761488015829762048>",
                                inline=False)

                badge_name = name.split(":")

                embed.add_field(
                    name="**Type:**",
                    value=f"**{data['gym-leaders'][str(member.id)]['Type']}**",
                    inline=True)
                embed.add_field(
                    name=f"**Badge:** {badge_name[1].capitalize()} Badge",
                    value=f"{data['gym-leaders'][str(member.id)]['Badge']}",
                    inline=True)

                for badges in data["gym-leaders"][str(member.id)]["Badges"]:
                    total += 1
                    badges_list.append(badges)

                if total == 0:
                    embed.add_field(name=f"**Gym Badges:** {total}",
                                    value="\u200b\n",
                                    inline=False)
                else:
                    embed.add_field(name=f"**Gym Badges:** {total}",
                                    value="**Obtained:**",
                                    inline=False)

                    for badges in data["gym-leaders"][str(
                            member.id)]["Badges"]:
                        badge_name = badges.split(":")
                        embed.add_field(
                            name=f"{badge_name[1].capitalize()} Badge",
                            value=badges,
                            inline=True)

                for achievements in data['gym-leaders'][str(
                        member.id)]["Achievements"]:
                    titles.append(achievements)

                titles_str = ", ".join(titles)

                if len(titles) >= 1:
                    embed.add_field(name="**Achievements:**",
                                    value=f"{titles_str}",
                                    inline=False)

                await ctx.send(embed=embed)

            except KeyError:
                if role2 in member.roles:
                    try:
                        with open(prof_file, "r") as bot_data:
                            data = json.load(bot_data)

                        if data['gym-leaders'][str(member.id)]:
                            pass

                    except KeyError:
                        await pf()

                elif role3 in member.roles:
                    try:
                        with open(prof_file, "r") as bot_data:
                            data = json.load(bot_data)

                        if data['champion'][str(member.id)]:
                            pass

                    except KeyError:
                        await pf()
                else:
                    await pf()

        if role2 in member.roles:  # elites

            try:

                with open(prof_file, "r") as bot_data:
                    data = json.load(bot_data)

                embed.set_thumbnail(url=member.avatar_url)

                if data['elites'][str(member.id)]:
                    pass

                embed.add_field(name="**Status:**",
                                value="<@&761487391147950111>",
                                inline=False)

                embed.add_field(
                    name="**Type:**",
                    value=f"**{data['elites'][str(member.id)]['Type']}**",
                    inline=True)

                for badges in data["elites"][str(member.id)]["Badges"]:
                    total += 1
                    badges_list.append(badges)

                if total == 0:
                    embed.add_field(name=f"**Gym Badges:** {total}",
                                    value="\u200b\n",
                                    inline=False)
                else:
                    embed.add_field(name=f"**Gym Badges:** {total}",
                                    value="**Obtained:**",
                                    inline=False)

                    for badges in data['elites'][str(member.id)]["Badges"]:
                        badge_name = badges.split(":")
                        embed.add_field(
                            name=f"{badge_name[1].capitalize()} Badge",
                            value=badges,
                            inline=True)

                for achievements in data["elites"][str(
                        member.id)]["Achievements"]:
                    titles.append(achievements)

                titles_str = ", ".join(titles)

                if len(titles) >= 1:
                    embed.add_field(name="**Achievements:**",
                                    value=f"{titles_str}",
                                    inline=False)

                await ctx.send(embed=embed)

            except KeyError:
                if role1 in member.roles:
                    try:
                        with open(prof_file, "r") as bot_data:
                            data = json.load(bot_data)

                        if data['elites'][str(member.id)]:
                            pass

                    except KeyError:
                        await pf()

                elif role3 in member.roles:
                    try:
                        with open(prof_file, "r") as bot_data:
                            data = json.load(bot_data)

                        if data['champion'][str(member.id)]:
                            pass

                    except KeyError:
                        await pf()
                else:
                    await pf()

        if role3 in member.roles:  # champion

            try:

                with open(prof_file, "r") as bot_data:
                    data = json.load(bot_data)

                if data['champion'][str(member.id)]:
                    pass

                embed.set_thumbnail(url=member.avatar_url)

                embed.add_field(name="**Status:**",
                                value="<@&767742527818039317>",
                                inline=False)

                embed.add_field(
                    name="**Champion Season:**",
                    value=f"{data['champion'][str(member.id)]['Season']}",
                    inline=False)

                embed.add_field(
                    name="**Challenges Endured:**",
                    value=f"{data['champion'][str(member.id)]['Saved']}",
                    inline=False)

                for achievements in data["champion"][str(
                        member.id)]["Achievements"]:
                    titles.append(achievements)

                titles_str = ", ".join(titles)

                if len(titles) >= 1:
                    embed.add_field(name="**Achievements:**",
                                    value=f"{titles_str}",
                                    inline=False)

                if data['champion'][str(member.id)]['Image'] != "":

                    embed.add_field(name="**Champion Team:**", value="\u200b")
                    embed.set_image(
                        url=f"{data['champion'][str(member.id)]['Image']}")

                await ctx.send(embed=embed)

            except KeyError:
                await pf()

        if role4 in member.roles:  # else all
            if role1 in member.roles:
                pass

            elif role2 in member.roles:
                pass

            elif role3 in member.roles:
                pass

            else:
                await pf()

    @commands.command(aliases=["champ", "nc"])
    @commands.has_any_role("champion", "admin", "moderator")
    async def champion(self, ctx, generation, member: discord.Member):

        prefix = server_prefix(ctx)

        if generation == "6":
            data_file = "gen6.json"
            prof_file = "league_prof6.json"
        elif generation == "7":
            data_file = "gen7.json"
            prof_file = "league_prof7.json"
        else:
            await ctx.send(
                f"Enter a valid Generation(6/7)\nUse `{prefix}help nc` to know more."
            )
            return

        past_titles = []
        channel = self.client.get_channel(802027595302174730)
        prev_champ = ""
        empty_list = []

        with open(prof_file, "r") as champ_data:
            data1 = json.load(champ_data)

        json_champ = data1["champion"]

        for mem in json_champ:
            prev_champ = await ctx.guild.fetch_member(int(mem))

        with open(data_file, "r") as bot_data:
            data2 = json.load(bot_data)

        data2[str(prev_champ.id)]["Elite_Streak"] = empty_list

        with open(data_file, "w") as bot_data:
            json.dump(data2, bot_data, indent=4)

        json_champ.pop(str(prev_champ.id))

        data1["champion"][str(member.id)] = {
            "Season": f"{current_title}",
            "Saved": 0,
            "Image": "",
            "Achievements": []
        }

        with open(prof_file, "w") as champ_data:
            json.dump(data1, champ_data, indent=4)

        with open(data_file, "r") as bot_data:
            data2 = json.load(bot_data)

        for achievements in data2[str(member.id)]["Achievements"]:
            past_titles.append(achievements)

        past_titles.append(current_title)

        data2[str(member.id)]["Achievements"] = past_titles
        data1["champion"][str(member.id)]["Achievements"] = past_titles

        with open(data_file, "w") as bot_data:
            json.dump(data2, bot_data, indent=4)

        with open(prof_file, "w") as champ_data:
            json.dump(data1, champ_data, indent=4)

        role = discord.utils.get(ctx.guild.roles, name="champion")
        await member.add_roles(role)
        role = discord.utils.get(ctx.guild.roles, name="master-trainers")
        await member.add_roles(role)

        with open("hall_of_fame.json", "r") as bot_data:
            data = json.load(bot_data)

        winners = list(data[current_title][f"Gen {generation}"])
        winners.append(str(member.mention))
        data[current_title][f"Gen {generation}"] = winners

        with open("hall_of_fame.json", "w") as bot_data:
            json.dump(data, bot_data, indent=4)

        await ctx.send(
            f"{member.mention} is the new Generation {generation} Champion")
        await channel.send(
            f"Congratulations {member.mention}!\nYou are the new champion of Generation {generation} until someone defeats you in a champion battle."
        )
        await ctx.send(f"{prev_champ.mention}'s Elite streak has now been resetted.")

    @commands.command(aliases=["res"])
    @commands.has_any_role("elites", "champion", "admin", "moderator")
    async def reset_streak(self, ctx, generation, member: discord.Member):

        prefix = server_prefix(ctx)

        if ctx.channel.name == "📝registration":
            return

        if generation == "6":
            data_file = "gen6.json"
            prof_file = "league_prof6.json"
        elif generation == "7":
            data_file = "gen7.json"
            prof_file = "league_prof7.json"
        else:
            await ctx.send(
                f"Enter a valid Generation(6/7)\nUse `{prefix}help res` to know more."
            )
            return

        empty_list = []
        channel = self.client.get_channel(802027595302174730)

        async def res():

            endured2 = 0
            champ2 = ""

            with open(data_file, "r") as bot_data:
                data = json.load(bot_data)

            if str(member.id) not in data:
                await ctx.send(
                    f"{member} is not registered for this generation.")
                return

            if data[str(member.id)]["Registered"] == empty_list:
                await ctx.send(
                    f"{member} is not registered for this generation.")
                return

            streak = len(data[str(member.id)]["Elite_Streak"])

            data[str(member.id)]["Elite_Streak"] = empty_list

            with open(data_file, "w") as bot_data:
                json.dump(data, bot_data, indent=4)

            await ctx.send(f"{member.mention}'s Elite Streak has been reseted."
                           )
            await channel.send(
                f"{member.mention}'s Generation {generation} Elite Streak has been reseted.")

            if streak == 4:

                with open(prof_file, "r") as champ_data:
                    data1 = json.load(champ_data)

                json_champ = data1["champion"]

                for mem in json_champ:
                    champ2 = await ctx.guild.fetch_member(int(mem))
                    endured2 = int(data1["champion"][str(mem)]["Saved"])

                endured2 += 1
                data1["champion"][str(champ2.id)]["Saved"] = endured2

                with open(prof_file, "w") as champ_data:
                    json.dump(data1, champ_data, indent=4)

                await channel.send(
                    f"{champ2.mention} has endured {endured2} match/es now.")
            return

        role1 = discord.utils.get(ctx.guild.roles, name="gym-leaders")
        role2 = discord.utils.get(ctx.guild.roles, name="elites")

        if role1 in member.roles:

            try:
                with open(prof_file, "r") as champ_data1:
                    data2 = json.load(champ_data1)

                if data2['gym-leaders'][str(member.id)]:
                    pass

                await ctx.send("Gym-Leaders cannot get elite streak")
                return

            except KeyError:
                await res()

        elif role2 in member.roles:
            try:
                with open(prof_file, "r") as champ_data1:
                    data2 = json.load(champ_data1)

                if data2['elites'][str(member.id)]:
                    pass

                await ctx.send("Elites cannot get elite streak")
                return

            except KeyError:
                await res()

        else:
            await res()

    @commands.command(aliases=["et", "ep"])
    @commands.has_any_role("challengers", "elites", "admin", "moderator")
    async def elite_team(self, ctx, generation, member: discord.Member, *, team):

        prefix = server_prefix(ctx)

        if generation == "6":
            data_file = "gen6.json"
            dex = "mons6.txt"
            prof_file = "league_prof6.json"
        elif generation == "7":
            data_file = "gen7.json"
            dex = "mons7.txt"
            prof_file = "league_prof7.json"
        else:
            await ctx.send(
                f"Enter a valid Generation(6/7)\nUse `{prefix}help et` to know more."
            )
            return

        empty_list = []
        team = team.replace(" ", "")
        team = team.split(",")
        pokemon = set()
        pool_of_6 = set()
        elite_pool = set()
        channel = self.client.get_channel(802027595302174730)

        role1 = discord.utils.get(ctx.guild.roles, name="gym-leaders")
        role2 = discord.utils.get(ctx.guild.roles, name="elites")

        async def et():

            with open(data_file, "r") as bot_data:
                data = json.load(bot_data)

            if data[str(member.id)]["Elite_Streak"] != empty_list:
                await ctx.send("You cannot register your elite team when you have streak.")
                return

            for a in team:
                pokemon.add(a.capitalize())

            if str(member.id) not in data:
                await ctx.send(
                    f"{member} is not registered for this generation.")
                return

            if data[str(member.id)]["Registered"] == empty_list:
                await ctx.send(
                    f"{member} is not registered for this generation.")
                return

            registered = data[str(member.id)]["Registered"]

            with open(dex, "r") as file:
                pokedex = file.read().split("\n")

            for a in pokemon:
                for b in pokedex:
                    if a.casefold() == b.casefold():
                        pool_of_6.add(a.capitalize())

            not_valid = list(pokemon.difference(pool_of_6))
            wrong = ", ".join(not_valid)

            if len(pokemon) != len(pool_of_6):
                await ctx.send(
                    f"{wrong} is/are not valid.\nWeather you have spelt wrong or entered wrong Pokémon"
                )
                return

            for a in pokemon:
                for b in registered:
                    if a.casefold() == b.casefold():
                        elite_pool.add(a.capitalize())

            not_valid = list(pokemon.difference(elite_pool))
            wrong = ", ".join(not_valid)

            if len(pokemon) != len(elite_pool):
                await ctx.send(
                    f"{wrong} not in registered pool of {member.mention}")
                return

            if len(elite_pool) < 6:
                await ctx.send("Team contains less than 6 Pokémon")
                return
            elif len(elite_pool) > 6:
                await ctx.send("Team contains more than 6 Pokémon")
                return

            submitted = ", ".join(elite_pool)
            data[str(member.id)]["Elite_Pool"] = list(elite_pool)

            with open(data_file, "w") as bot_data:
                json.dump(data, bot_data, indent=4)

            await ctx.send(
                f"Generation {generation} Elite Pool of {member.mention} has been submitted.\nSubmitted: {submitted}"
            )
            await channel.send(
                f"Generation {generation} Elite Pool of {member.mention} has been submitted.\nSubmitted: {submitted}"
            )
            return

        if role1 in member.roles:

            try:
                with open(prof_file, "r") as champ_data1:
                    data2 = json.load(champ_data1)

                if data2['gym-leaders'][str(member.id)]:
                    pass

                await ctx.send("Gym-Leaders cannot challenge Elites")
                return

            except KeyError:
                await et()

        elif role2 in member.roles:
            try:
                with open(prof_file, "r") as champ_data1:
                    data2 = json.load(champ_data1)

                if data2['elites'][str(member.id)]:
                    pass

                await ctx.send("Elites cannot challenge Elites")
                return

            except KeyError:
                await et()

        else:
            await et()

    @commands.command(aliases=["epl", "epk"])
    async def elite_pool(self, ctx, generation, member: discord.Member = None):

        prefix = server_prefix(ctx)

        if member is None:
            member = ctx.author

        if member is None:
            member = ctx.author

        if generation == "6":
            data_file = "gen6.json"
            prof_file = "league_prof6.json"
        elif generation == "7":
            data_file = "gen7.json"
            prof_file = "league_prof7.json"
        else:
            await ctx.send(
                f"Enter a valid Generation(6/7)\nUse `{prefix}help epl` to know more."
            )
            return

        role1 = discord.utils.get(ctx.guild.roles, name="gym-leaders")
        role2 = discord.utils.get(ctx.guild.roles, name="elites")

        async def ep():

            with open(data_file, "r") as bot_data:
                data = json.load(bot_data)

            if str(member.id) not in data:
                await ctx.send(
                    f"{member} is not registered for the current generation.")
                return

            if "Elite_Pool" not in data[str(member.id)]:
                await ctx.send(
                    f"{member}'s Elite Team of the current generation has not submitted yet."
                )
                return
            else:
                pass

            registered = data[str(member.id)]["Elite_Pool"]
            registered_str = "\n".join(registered)

            em = discord.Embed(
                title=f"{member}'s Generation {generation} Elite Pool:",
                description=f"**{registered_str}**",
                colour=discord.Colour.green())

            await ctx.send(embed=em)
            return

        if role1 in member.roles:

            try:
                with open(prof_file, "r") as champ_data1:
                    data2 = json.load(champ_data1)

                if data2['gym-leaders'][str(member.id)]:
                    pass

                await ctx.send("Gym-Leaders cannot challenge Elites")
                return

            except KeyError:
                await ep()

        elif role2 in member.roles:
            try:
                with open(prof_file, "r") as champ_data1:
                    data2 = json.load(champ_data1)

                if data2['elites'][str(member.id)]:
                    pass

                await ctx.send("Elites cannot challenge Elites")
                return

            except KeyError:
                await ep()

        else:
            await ep()

    # @commands.command(aliases=["r", "registration"])
    # async def register(self, ctx, generation, *, raw_input):

    #     prefix = server_prefix(ctx)

    #     if ctx.channel.name == "📝challengers-registration":
    #         pass
    #     else:
    #         return

    #     illegal_found = 0
    #     illegal_mon = []
    #     pool_of_12 = set()
    #     perfect_mons = set()
    #     pokemon = set()
    #     empty_list = []
    #     user = ctx.author
    #     channel = self.client.get_channel(802027595302174730)

    #     if generation == "6":
    #         illegal = "illegal6.txt"
    #         data_file = "gen6.json"
    #         dex = "mons6.txt"
    #     elif generation == "7":
    #         illegal = "illegal7.txt"
    #         data_file = "gen7.json"
    #         dex = "mons7.txt"
    #     else:
    #         await user.send(f"Enter a valid Generation(6/7)\nUse `{prefix}help r` to know more.")
    #         return

    #     raw_input = raw_input.replace(" ", "")

    #     raw_pokemon = set(raw_input.split(","))

    #     for mons in raw_pokemon:
    #         pokemon.add(mons.capitalize())

    #     with open(illegal, "r") as banned:
    #         illegal_mons = banned.read().split("\n")

    #     with open(data_file, "r") as bot_data:
    #         data = json.load(bot_data)

    #     if str(ctx.author.id) not in data:
    #         data[str(ctx.author.id)] = {"Registered": list(), "Badges": list(), "Elite_Streak": list(),
    #                                     "Reset_Token": 1, "Achievements": list()}

    #         with open(data_file, "w") as bot_data:
    #             json.dump(data, bot_data, indent=4)

    #     if data[str(ctx.author.id)]["Registered"] != empty_list:
    #         await user.send("You have already registered for this generation.")
    #         return

    #     with open(dex, "r") as file:
    #         pokedex = file.read().split("\n")

    #     for a in pokemon:
    #         for b in pokedex:
    #             if a.casefold() == b.casefold():
    #                 pool_of_12.add(a.capitalize())

    #     not_valid = list(pokemon.difference(pool_of_12))
    #     wrong = ", ".join(not_valid)

    #     if len(pokemon) != len(pool_of_12):
    #         await user.send(f"{wrong} is/are not valid.\nWhether you have spelt wrong or entered wrong Pokémon")
    #         return

    #     for pmon in pool_of_12:
    #         for mons in illegal_mons:
    #             if pmon.casefold() == mons.casefold():
    #                 illegal_mon.append(pmon.capitalize())
    #                 illegal_found += 1
    #             else:
    #                 perfect_mons.add(pmon.capitalize())

    #     if illegal_found >= 1:
    #         not_legal = ", ".join(illegal_mon)
    #         await user.send(
    #             f"Your team is not valid because it contains {not_legal} which is/are in higher tier than OU")
    #         return

    #     if len(perfect_mons) < 12:
    #         await user.send("You Pool contains less than 12 Pokémon")
    #         return
    #     elif len(perfect_mons) > 12:
    #         await user.send("You Pool contains more than 12 Pokémon")
    #         return

    #     submitted = "\n".join(perfect_mons)

    #     data[str(ctx.author.id)]["Registered"] = list(perfect_mons)
    #     with open(data_file, "w") as bot_data:
    #         json.dump(data, bot_data, indent=4)

    #     msg = await ctx.send(
    #         f"{ctx.author.mention}'s Generation {generation} Pool has been submitted...\nSubmitted:\n{submitted}")

    #     await user.send(f"Your Generation {generation} Pool have been Submitted.\n{submitted}")

    #     await channel.send(f"{ctx.author.mention}'s' Generation {generation} Pool have been Submitted.\n{submitted}")

    #     role = discord.utils.get(ctx.guild.roles, name="challengers")
    #     await ctx.author.add_roles(role)

    #     await asyncio.sleep(3)
    #     await msg.delete()

    # @commands.command(aliases=["rs", "restart"])
    # async def reset(self, ctx, generation, *, raw_input):

    #     if ctx.channel.name == "📝registration":
    #         pass
    #     else:
    #         return

    #     illegal_found = 0
    #     illegal_mon = []
    #     pool_of_12 = set()
    #     perfect_mons = set()
    #     pokemon = set()
    #     user = ctx.author

    #     if generation == "6":
    #         illegal = "illegal6.txt"
    #         data_file = "gen6.json"
    #         dex = "mons6.txt"
    #     elif generation == "7":
    #         illegal = "illegal7.txt"
    #         data_file = "gen7.json"
    #         dex = "mons7.txt"
    #     else:
    #         await user.send(f"Enter a valid Generation(6/7)\nUse `{prefix}help rs` to know more.")
    #         return

    #     raw_pokemon = set(raw_input.split(", "))
    #     for mons in raw_pokemon:
    #         pokemon.add(mons.capitalize())

    #     with open(illegal, "r") as banned:
    #         illegal_mons = banned.read().split("\n")

    #     with open(data_file, "r") as bot_data:
    #         data = json.load(bot_data)

    #     if str(ctx.author.id) not in data:
    #         await user.send("You haven't registered for this generation yet.")
    #         return

    #     available_reset = data[str(ctx.author.id)]["Reset_Token"] - 1

    #     if data[str(ctx.author.id)]["Reset_Token"] == 0:
    #         await user.send("You have already claimed all your reset tokens of this generation.")
    #         return

    #     with open(dex, "r") as file:
    #         pokedex = file.read().split("\n")
    #     for a in pokemon:
    #         for b in pokedex:
    #             if a.casefold() == b.casefold():
    #                 pool_of_12.add(a.capitalize())

    #     not_valid = list(pokemon.difference(pool_of_12))
    #     wrong = ", ".join(not_valid)

    #     if len(pokemon) != len(pool_of_12):
    #         await user.send(f"{wrong} is/are not valid.\nWhether you have spelt wrong or entered wrong Pokémon")
    #         return

    #     for pmon in pool_of_12:
    #         for mons in illegal_mons:
    #             if pmon.casefold() == mons.casefold():
    #                 illegal_mon.append(pmon.capitalize())
    #                 illegal_found += 1
    #             else:
    #                 perfect_mons.add(pmon.capitalize())

    #     if illegal_found >= 1:
    #         not_legal = ", ".join(illegal_mon)
    #         await user.send(
    #             f"Your team is not valid because it contains {not_legal} which is/are in higher tier than OU")
    #         return

    #     if len(perfect_mons) < 12:
    #         await user.send("You Pool contains less than 12 Pokémon")
    #     elif len(perfect_mons) > 12:
    #         await user.send("You Pool contains more than 12 Pokémon")
    #     else:

    #         with open(data_file, "r") as bot_data:
    #             data = json.load(bot_data)

    #         prev_pool = set(data[str(ctx.author.id)]["Registered"])
    #         submitted = ", ".join(perfect_mons)
    #         set_submitted = set(perfect_mons)

    #         difference_pool = set_submitted.difference(prev_pool)

    #         if len(difference_pool) == 0:
    #             await user.send("Your previous pool has no variation with the new pool.")
    #             return
    #         elif len(difference_pool) > 6:
    #             await user.send("Your new pool contains more than 6 changes.")
    #             return
    #         else:
    #             await user.send(f"Your league reset is successful and your new pool has been submitted.\n{submitted}")
    #             await ctx.send(f"{ctx.author.mention} has restarted league.\nNew Pool:{submitted}")

    #             with open(data_file, "r") as bot_data:
    #                 data = json.load(bot_data)

    #             data[str(ctx.author.id)] = {"Registered": list(), "Badges": list(), "Elite_Streak": list(),
    #                                         "Reset_Token": available_reset, "Achievements": list()}
    #             with open(data_file, "w") as bot_data:
    #                 json.dump(data, bot_data, indent=4)

    #             data[str(ctx.author.id)]["Registered"] = list(perfect_mons)
    #             with open(data_file, "w") as bot_data:
    #                 json.dump(data, bot_data, indent=4)

    # @commands.command(aliases=["ct"])
    # async def check_team(self, ctx, generation, member: discord.Member, *, raw_input):

    #     if ctx.channel.name == "📝registration":
    #         return

    #     pool_check = set()
    #     pokemon = set()
    #     empty_list = []

    #     if generation == "6":
    #         data_file = "gen6.json"
    #         dex = "mons6.txt"
    #     elif generation == "7":
    #         data_file = "gen7.json"
    #         dex = "mons7.txt"
    #     else:
    #         await ctx.send(f"Enter a valid Generation(6/7)\nUse `{prefix}help ct` to know more.")
    #         return

    #     raw_pokemon = set(raw_input.split(", "))
    #     for mons in raw_pokemon:
    #         pokemon.add(mons.capitalize())

    #     with open(data_file, "r") as bot_data:
    #         data = json.load(bot_data)

    #     if str(ctx.author.id) not in data:
    #         await ctx.send(f"{member} has not registered for the current generation")
    #         return
    #     else:
    #         if data[str(member.id)]["Registered"] == empty_list:
    #             await ctx.send(f"{member} has not registered for the current generation")
    #             return
    #         else:
    #             pass

    #     registered_pool = set(data[str(member.id)]["Registered"])

    #     with open(dex, "r") as file:
    #         pokedex = file.read().split("\n")
    #         for a in pokemon:
    #             for b in pokedex:
    #                 if a.casefold() == b.casefold():
    #                     pool_check.add(a.capitalize())

    #         if len(pool_check) != 6:
    #             await ctx.send(f"A team must contain 6 Pokémon. It contains {len(pool_check)} Pokémon.")
    #             return
    #         else:
    #             pass

    #         not_valid = list(pokemon.difference(pool_check))
    #         wrong = ", ".join(not_valid)

    #         if len(pokemon) != len(pool_check):
    #             await ctx.send(f"{wrong} is/are not valid.\nWhether you have spelt wrong or entered wrong Pokémon")
    #             return

    #     xyz = pool_check.difference(registered_pool)

    #     if len(xyz) == 0:
    #         await ctx.send(f"{member}'s team is valid.")
    #     else:
    #         wrong = ", ".join(xyz)
    #         await ctx.send(f"{member}'s team is not valid as it contains {wrong} which is/are not in his registered pool.")

    @commands.command(aliases=["s", "sp", "swap_pokemon", "swap_pool", "change"])
    async def swap(self, ctx, generation, prev_mon, new_mon):

        prefix = server_prefix(ctx)

        if ctx.channel.name == "📝challengers-registration":
            pass
        else:
            return

        with open("mod.json", "r") as bot_data:
            data = json.load(bot_data)

        if data["start"] == "yes":
            await ctx.send("Swapping Pokémon has been closed")
            return

        swap_mon = ""
        illegal_mon = ""
        empty_list = []
        user = ctx.author
        channel = self.client.get_channel(802027595302174730)

        if generation == "6":
            illegal = "illegal6.txt"
            data_file = "gen6.json"
            dex = "mons6.txt"
        elif generation == "7":
            illegal = "illegal7.txt"
            data_file = "gen7.json"
            dex = "mons7.txt"
        else:
            await ctx.send(f"Enter a valid Generation(6/7)\nUse `{prefix}help swap` to know more.")
            return

        with open(data_file, "r") as bot_data:
            data = json.load(bot_data)

        if str(ctx.author.id) not in data:
            await user.send("You are not registered for the current generation.")
            return

        if data[str(ctx.author.id)]["Registered"] == empty_list:
            await user.send("You are not registered for the current generation.")
            return

        pool = list(data[str(ctx.author.id)]["Registered"])

        if prev_mon.capitalize() not in pool:
            await user.send(f"{prev_mon.capitalize()} not in your registered pool.")
            return
        else:
            pass

        with open(dex, "r") as file:
            pokedex = file.read().split("\n")
        for b in pokedex:
            if b.casefold() == new_mon.casefold():
                swap_mon = "valid"
                break

        if swap_mon != "valid":
            await user.send(
                f"{new_mon.capitalize()} is not valid.\nWhether you have spelt wrong or entered wrong Pokémon")
            return

        with open(illegal, "r") as banned:
            illegal_mons = banned.read().split("\n")

        for mons in illegal_mons:
            if mons.casefold() == new_mon.casefold():
                illegal_mon = "yes"
                break

        if illegal_mon == "yes":
            await user.send(f"{new_mon.capitalize()} cannot be swapped as it is in higher tier than OU.")
            return

        pool.remove(prev_mon.capitalize())
        pool.append(new_mon.capitalize())
        data[str(ctx.author.id)]["Registered"] = pool
        with open(data_file, "w") as bot_data:
            json.dump(data, bot_data, indent=4)

        msg = await ctx.send(f"{new_mon.capitalize()} has been swapped with {prev_mon.capitalize()}")

        with open(data_file, "r") as bot_data:
            data = json.load(bot_data)

        submitted = data[str(ctx.author.id)]["Registered"]
        new_pool = ", ".join(submitted)

        await channel.send(f"{ctx.author.mention}'s Generation {generation} New Pool:\n{new_pool}")

        await user.send(f"Your new pool:\n{new_pool}")

        await asyncio.sleep(3)
        await msg.delete()

    @commands.command(aliases=["pl", "pokemon"])
    async def pool(self, ctx, generation, *, member: discord.Member = None):

        prefix = server_prefix(ctx)

        if ctx.channel.name == "📝registration":
            return

        empty_list = []

        if member is None:
            member = ctx.author
        else:
            pass

        if generation == "6":
            data_file = "gen6.json"
        elif generation == "7":
            data_file = "gen7.json"
        else:
            await ctx.send(f"Enter a valid Generation(6/7)\nUse `{prefix}help pool` to know more.")
            return

        with open(data_file, "r") as bot_data:
            data = json.load(bot_data)

        if str(member.id) not in data:
            await ctx.send(f"{member} is not registered for the current generation.")
            return
        else:
            if data[str(member.id)]["Registered"] == empty_list:
                await ctx.send(f"{member} has not registered for the current generation")
                return
            else:
                pass

        registered = list(data[str(member.id)]["Registered"])
        registered_str = "\n".join(registered)

        em = discord.Embed(title=f"{member}'s Generation {generation} Pool:", description=f"**{registered_str}**",
                           colour=discord.Colour.green())

        await ctx.send(embed=em)

    @commands.command()
    async def check(self, ctx, generation, *, mon):

        prefix = server_prefix(ctx)

        valid = False

        if generation == "6":
            dex = "mons6.txt"
        elif generation == "7":
            dex = "mons7.txt"
        else:
            await ctx.send(f"Enter a valid Generation(6/7)\nUse `{prefix}help swap` to know more.")
            return

        with open(dex, "r") as file:
            pokedex = file.read().split("\n")
        for a in pokedex:
            if a.casefold() == mon.casefold():
                await ctx.send(f"{mon} is valid.")
                valid = True

        if valid is False:
            await ctx.send(f"{mon} is not valid.")

    @commands.command(aliases=["hof"])
    async def hall_of_fame(self, ctx):

        if ctx.channel.name == "📝registration":
            return

        empty_list = []

        em = discord.Embed(title="**Hall Of Fame**",
                           colour=discord.Colour.green())

        em.set_thumbnail(url=ctx.guild.icon_url)

        with open("hall_of_fame.json", "r") as bot_data:
            data = json.load(bot_data)

        for league in data:
            em.add_field(name=league,
                         value=f"**Champions of {league}:**",
                         inline=False)
            for generation in data[league]:
                if data[league][generation] == empty_list:
                    value = "None"
                else:
                    winner = data[league][generation]
                    value = "\n".join(winner)
                em.add_field(name=generation,
                             value=f"{value}\u200b\n",
                             inline=True)

        await ctx.send(embed=em)

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


def setup(client):
    client.add_cog(League(client))
