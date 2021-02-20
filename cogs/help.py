import discord
from discord.ext import commands
import json

with open("mod.json", "r") as mod_data:
    save = json.load(mod_data)

prefix = str(save["prefix"])


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True,
                    case_insensitive=True,
                    aliases=["h"])
    async def help(self, ctx):

        if ctx.channel.name == "📝registration":
            return

        help_embed = discord.Embed(
            title="Commands",
            description=
            f"If you need more information about a specific command, type `{prefix}help <command>` or `{prefix}h <command>`",
            colour=discord.Colour.green())
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(name="Register",
                             value="The registration command.",
                             inline=False)

        # help_embed.add_field(name="Reset", value="Claim your reset token and swap 6 of your Pokémon Pool.",
        #                      inline=False)

        help_embed.add_field(
            name="Profile",
            value="Check profile of provided generation and user.",
            inline=False)

        help_embed.add_field(
            name="Swap",
            value=
            "Swap one of your Pokémon of the desired generation before league starts",
            inline=False)

        help_embed.add_field(
            name="Pool",
            value=
            "See your or someone's current registered pool of the current generation.",
            inline=False)

        # help_embed.add_field(name="Check_team", value="Check if the battling team of the member mentioned is valid or not.", inline=False)

        help_embed.add_field(
            name="Hall_of_fame",
            value="See the Hall of Fame of all the champions.",
            inline=False)

        # help_embed.add_field(name="GG",
        #                      value="A basic chat game.",
        #                      inline=False)

        help_embed.add_field(
            name="Elite_team",
            value="Command to submit the elite team of the challenger.",
            inline=False)

        help_embed.add_field(
            name="Elite_pool",
            value="Command to see and check the elite pool of a chelenger.",
            inline=False)

        name_roles = ["gym-leaders", "elites", "moderator", "admin"]
        roles = []
        for names in name_roles:
            role = discord.utils.get(ctx.guild.roles, name=names)
            roles.append(role)

        for r in roles:
            if r in ctx.author.roles:
                help_embed.add_field(
                    name="Add_badge",
                    value=
                    "Add defined badge of the provided generation to the mentioned user.",
                    inline=False)

                help_embed.add_field(
                    name="Add_streak",
                    value=
                    "Increase elite streak of the provided generation and mentioned user by one.",
                    inline=False)

                break

        name_roles = ["champion", "moderator", "admin"]
        roles = []
        for names in name_roles:
            role = discord.utils.get(ctx.guild.roles, name=names)
            roles.append(role)

        for r in roles:
            if r in ctx.author.roles:
                help_embed.add_field(
                    name="Champion",
                    value="Make new champion and update hall of fame.",
                    inline=False)
                help_embed.add_field(
                    name="Reset_streak",
                    value=
                    "Reset the elite streak if the member and if streak was 4, increase champion endurance by 1."
                )

                break

        name_roles = ["moderator", "admin"]
        roles = []
        for names in name_roles:
            role = discord.utils.get(ctx.guild.roles, name=names)
            roles.append(role)

        for r in roles:
            if r in ctx.author.roles:
                help_embed.add_field(
                    name="Moderator",
                    value="See all the Moderator commands for managing league.",
                    inline=False)

                break

        help_embed.add_field(name="Game", value="See all the games.", inline=False)

        await ctx.send(embed=help_embed)

    @help.command(aliases=["r", "registration"])
    async def register(self, ctx):

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Register",
            description="Register your pool of 12 Pokémon for league.",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(name="Channel Specific Command.",
                     value="<#764672011087642645>")
        em.add_field(
            name="Syntax",
            value=
            f"`{prefix}register <generation> <pool>`\n\n*Generation can be 6 or 7*\n*The Pool of 12 should be written continuously separated by a **comma(,)** and a **space( )**.*",
            inline=False)
        em.add_field(name="Aliases",
                     value="`r` , `register` , `registration`",
                     inline=False)
        em.add_field(
            name="Usage",
            value=
            f"`{prefix}r 6 metagross, talonflame, absol, zweilous, zapdos, wobbuffet, whimsicott, volcanion, vanillite, altaria, alakazam, seismitoad`",
            inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["p", "summary"])
    async def profile(self, ctx):

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Profile",
            description=
            "Check your or someone's profile of the provided generation",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(
            name="Syntax",
            value=
            f"`{prefix}profile <generation> <user>`\n\n*Generation can be 6 or 7*\n*Mention the user you wanna check*\n*It will show your profile by default if no user is mentioned.*",
            inline=False)
        em.add_field(name="Aliases",
                     value="`p` , `profile` , `summary`",
                     inline=False)
        em.add_field(
            name="Usage",
            value=f"`{prefix}profile 6 @{ctx.author.name}`\n`{prefix}p 6`",
            inline=False)

        await ctx.send(embed=em)

    # @help.command(aliases=["rs", "restart"])
    # async def reset(self, ctx):

    #     if ctx.channel.name == "📝registration":
    #         return

    #     em = discord.Embed(title="Reset",
    #                        description="Change 6 of your Pokémon pool and use up your reset token. Nothing if already used all of your reset token.",
    #                        colour=discord.Colour.green())
    #     em.set_thumbnail(url=self.client.user.avatar_url)
    #     em.add_field(name="Channel Specific Command.", value=f"<#764672011087642645>")
    #     em.add_field(name="Syntax",
    #                  value=f"`{prefix}reset <generation> <new pool>`\n\n*Generation can be 6 or 7*\n*New Pool must also be written as the same format as of Pool while registration, i.e. each separated by a **comma(,)** and a **space( )***\n*New Pool would contain 6 changes at maximum than the previous pool*",
    #                  inline=False)
    #     em.add_field(name="Aliases", value="`rs` , `reset` , `restart`", inline=False)
    #     em.add_field(name="Usage",
    #                  value=f"`{prefix}rs 6 Metagross, Talonflame, Keldeo, Zygarde, Zapdos, Tyranitar, Jolteon, Volcanion, Swampert, Altaria, Alakazam, Politoed`",
    #                  inline=False)

    #     await ctx.send(embed=em)

    @help.command(aliases=["as"])
    async def add_streak(self, ctx):

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Add_streak",
            description=
            "Add elite streak by one of the provided generation and mentioned user.",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(
            name="Needed Roles",
            value=
            "<@&761487391147950111>, <@&776871326371020830>, <@&761514056439562240>",
            inline=False)
        em.add_field(
            name="Syntax",
            value=
            f"`{prefix}add_streak <generation> <user>`\n\n*Generation can be 6 or 7*\n*The user to whom the streak to be added*",
            inline=False)
        em.add_field(name="Aliases", value="`add_streak` , `as`", inline=False)
        em.add_field(name="Usage",
                     value=f"`{prefix}add_streak 6 @Sayan`",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["ab"])
    async def add_badge(self, ctx):

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Add_badge",
            description=
            "Add given badge to the mentioned user of the provided generation.",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(
            name="Needed Roles",
            value=
            "<@&761488015829762048>, <@&776871326371020830>, <@&761514056439562240>",
            inline=False)
        em.add_field(
            name="Syntax",
            value=
            f"`{prefix}add_badge <generation> <user> <badge>`\n\n*Generation can be 6 or 7*\n*The user to whom the badge to be added*\n*Badge which to be added in text format.*",
            inline=False)
        em.add_field(name="Aliases", value="`add_badge` , `ab`", inline=False)
        em.add_field(name="Usage",
                     value=f"`{prefix}add_badge 6 @Sayan grass`",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["s", "sp", "swap_pokemon", "swap_pool", "change"])
    async def swap(self, ctx):

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Swap",
            description=
            "Swap one of Pokémon from pool of the given generation before starting of League",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(name="Channel Specific Command.",
                     value="<#764672011087642645>")
        em.add_field(
            name="Syntax",
            value=
            f"`{prefix}swap <generation> <prev Pokémon> <new Pokémon>`\n\n*Generation can be 6 or 7*\n*Pokémon to be swapped*\n*Pokémon with whom to be swapped.*",
            inline=False)
        em.add_field(
            name="Aliases",
            value=
            "`s` , `swap` , `sp` , `swap_pokemon` , `swap_pool` , `change`",
            inline=False)
        em.add_field(name="Usage",
                     value=f"`{prefix}swap 6 alakazam gengar`",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["pl", "pokemon"])
    async def pool(self, ctx):

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Pool",
            description=
            "See your or anyone's currently registered pool of 12 Pokémon of the provided generation.",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(
            name="Syntax",
            value=
            f"`{prefix}pool <generation> <user>`\n\n*Generation can be 6 or 7*\n*Mention the user you wanna check*\n*It will show your pool by default if no user is mentioned.*",
            inline=False)
        em.add_field(name="Aliases",
                     value="`pool` , `pokemon` , `pl`",
                     inline=False)
        em.add_field(name="Usage",
                     value=f"`{prefix}pool 6 {ctx.author}`\n`{prefix}pl 7`",
                     inline=False)

        await ctx.send(embed=em)

    # @help.command(aliases=["ct"])
    # async def check_team(self, ctx):

    #     if ctx.channel.name == "📝registration":
    #         return

    #     em = discord.Embed(title="Check_team", description="Check the battling team of the desired member and of provided generation and check if team is valid or not.", colour=discord.Colour.green())
    #     em.set_thumbnail(url=self.client.user.avatar_url)
    #     em.add_field(name="Syntax", value=f"`{prefix}ct <generation> <user> <team>`\n\n*Generation can be 6 or 7*\n*Mention of user whose team you wanna check.*\n*Battling Team of the member separated by a **comma(,)** and a **space( )**.*", inline=False)
    #     em.add_field(name="Aliases", value="`ct` , `check_team`", inline=False)
    #     em.add_field(name="Usage", value=f"`{prefix}ct @{ctx.author.name} Jolteon, Volcanion, Swampert, Altaria, Alakazam, Politoed`", inline=False)

    #     await ctx.send(embed=em)

    @help.command(aliases=["mod"])
    @commands.has_any_role("admin", "moderator")
    async def moderator(self, ctx):

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Moderator Commands",
            description="Here's are a list of all the moderator commands:",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(
            name="Swap_close",
            value=
            f"Stops the Pokémon swappable option available earlier.\n`{prefix}sc` or `{prefix}swap_close`",
            inline=False)
        em.add_field(
            name="Restart_league",
            value=
            f"Erases the data of the Current league for the preparation of the new league.\n`{prefix}restart_league <new_title>` or `{prefix}rl <new_title>`",
            inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["hof"])
    async def hall_of_fame(self, ctx):

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Hall_of_fame",
            description=
            "See the Hall of Fame of all the Champions formed in our server.",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(name="Syntax", value=f"`{prefix}hof`", inline=False)
        em.add_field(name="Aliases",
                     value="`hof` , `hall_of_fame`",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["champ", "nc"])
    async def champion(self, ctx):

        em = discord.Embed(
            title="Champion",
            description=
            "Command to make the mentioned user champion of the given generation",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(
            name="Needed Roles",
            value=
            "<@&767742527818039317>, <@&776871326371020830>, <@&761514056439562240>",
            inline=False)
        em.add_field(
            name="Syntax",
            value=
            f"`{prefix}champ <generation> <user>`\n\n*Generation can be 6 or 7*\n*Mention the New Champion*",
            inline=False)
        em.add_field(name="Aliases",
                     value="`champ` , `champion` , `nc`",
                     inline=False)
        em.add_field(name="Usage",
                     value=f"`{prefix}champ 6 @{ctx.author.name}`",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["res"])
    async def reset_streak(self, ctx):

        em = discord.Embed(
            title="Reset_streak",
            description=
            "Reset the elite streak of the mention user of the generation and check if challenger had 4 elite streak to increase endured matches of the current champion by 1.",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(
            name="Needed Roles",
            value=
            "<@&767742527818039317>, <@&776871326371020830>, <@&761514056439562240>",
            inline=False)
        em.add_field(
            name="Syntax",
            value=
            f"`{prefix}res <generation> <user>`\n\n*Generation can be 6 or 7*\n*Mention the user whose streak to be reseted.*",
            inline=False)
        em.add_field(name="Aliases",
                     value="`res` , `reset_streak`",
                     inline=False)
        em.add_field(name="Usage",
                     value=f"`{prefix}res @{ctx.author.name}`",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["epl", "epk"])
    async def elite_pool(self, ctx):

        em = discord.Embed(title="Elite_pool",
                           description="See the elite pool if available",
                           colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(
            name="Syntax",
            value=
            f"`{prefix}epl <generation> <user>`\n\n*Generation can be 6 or 7*\n*Mention the user you wanna check*\n*It will show your pool by default if no user is mentioned.*",
            inline=False)
        em.add_field(name="Aliases",
                     value="`elite_pool` , `epl` , `epk`",
                     inline=False)
        em.add_field(
            name="Usage",
            value=f"`{prefix}epl 6 @{ctx.author.name}`\n`{prefix}epk 7`",
            inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["et", "ep"])
    async def elite_team(self, ctx):

        em = discord.Embed(title="Elite_team",
                           description="Submit the elite team of a member.",
                           colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(
            name="Needed Roles",
            value=
            "<@&767743473116905474>, <@&761487391147950111>, <@&776871326371020830>, <@&761514056439562240>",
            inline=False)
        em.add_field(
            name="Syntax",
            value=
            f"`{prefix}et <generation> <user> <team>`\n\n*Generation can be 6 or 7*\n*Mention the user whose pool to be submitted*\n*User's used team in elite battle*",
            inline=False)
        em.add_field(name="Aliases",
                     value="`elite_team` , `et` , `ep`",
                     inline=False)
        em.add_field(
            name="Usage",
            value=
            f"`{prefix}et 6 @Sayan  Dragonite, Excadrill, Ferrothorn, Zapdos, Pinsir, Keldeo-resolute`",
            inline=False)

        await ctx.send(embed=em)


    
    @help.command(aliases=["fun"])
    async def game(self, ctx):

        em = discord.Embed(title="Game", description="", colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)
        em.add_field(name="GG", value="A basic guessing text based game.", inline=False)
        em.add_field(name="tic-tac-toe", value="Play Tic-Tac-Toe with another member. Aliases: `ttt`", inline=False)

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Help(client))
