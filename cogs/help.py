import discord
from discord.ext import commands
from replit import db
import asyncio
# from translator.constants import LANGUAGES


def server_prefix(msg):
    prefixes = db["prefixes"]
    s_prefix = prefixes[str(msg.guild.id)]

    return s_prefix


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True,
                    case_insensitive=True,
                    aliases=["h"])
    async def help(self, ctx):

        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Commands",
            description=f"If you need more information about a specific category, type `{prefix}help <category>` or `{prefix}h <category>`",
            colour=discord.Colour.green())

        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(name="🔨 Moderator", value=f"`{prefix}help mod`")

        help_embed.add_field(name="🎮 Game", value=f"`{prefix}help game`", inline=True)
        
        help_embed.add_field(name="📛Badge System", value=f"`{prefix}help badge`")

        # help_embed.add_field(name="🎶 Music", value=f"`{prefix}help music`", inline=True)

        help_embed.add_field(name="🎉 Misc", value=f"`{prefix}help misc`", inline=True)

        help_embed.add_field(name="🎪 Fun", value=f"`{prefix}help fun`", inline=True)

        help_embed.add_field(name="🎴 Pokedex", value=f"`{prefix}help pokedex`", inline=True)

        await ctx.send(embed=help_embed)

    @help.command(aliases=["r", "registration"])
    async def register(self, ctx):

        prefix = server_prefix(ctx)

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
            value=f"`{prefix}register <generation> <pool>`\n\n*Generation can be 6 or 7*\n*The Pool of 12 should be written continuously separated by a **comma(,)** and a **space( )**.*",
            inline=False)

        em.add_field(name="Aliases",
                     value="`r` , `register` , `registration`",
                     inline=False)

        em.add_field(
            name="Usage",
            value=f"`{prefix}r 6 metagross, talonflame, absol, zweilous, zapdos, wobbuffet, whimsicott, volcanion, vanillite, altaria, alakazam, seismitoad`",
            inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["p", "summary"])
    async def profile(self, ctx):

        prefix = server_prefix(ctx)

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Profile",
            description="Check your or someone's profile of the provided generation",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)

        em.add_field(
            name="Syntax",
            value=f"`{prefix}profile <generation> <user>`\n\n*Generation can be 6 or 7*\n*Mention the user you wanna check*\n*It will show your profile by default if no user is mentioned.*",
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

        prefix = server_prefix(ctx)

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Add_streak",
            description="Add elite streak by one of the provided generation and mentioned user.",
            colour=discord.Colour.green())

        em.set_thumbnail(url=self.client.user.avatar_url)

        em.add_field(
            name="Needed Roles",
            value="<@&761487391147950111>, <@&776871326371020830>, <@&761514056439562240>",
            inline=False)

        em.add_field(
            name="Syntax",
            value=f"`{prefix}add_streak <generation> <user>`\n\n*Generation can be 6 or 7*\n*The user to whom the streak to be added*",
            inline=False)
        em.add_field(name="Aliases", value="`add_streak` , `as`", inline=False)

        em.add_field(name="Usage",
                     value=f"`{prefix}add_streak 6 @Sayan`",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["ab"])
    async def add_badge(self, ctx):

        prefix = server_prefix(ctx)

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Add_badge",
            description="Add given badge to the mentioned user of the provided generation.",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)

        em.add_field(
            name="Needed Roles",
            value="<@&761488015829762048>, <@&776871326371020830>, <@&761514056439562240>",
            inline=False)

        em.add_field(
            name="Syntax",
            value=f"`{prefix}add_badge <generation> <user> <badge>`\n\n*Generation can be 6 or 7*\n*The user to whom the badge to be added*\n*Badge which to be added in text format.*",
            inline=False)

        em.add_field(name="Aliases", value="`add_badge` , `ab`", inline=False)

        em.add_field(name="Usage",
                     value=f"`{prefix}add_badge 6 @Sayan grass`",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["s", "sp", "swap_pokemon", "swap_pool", "change"])
    async def swap(self, ctx):

        prefix = server_prefix(ctx)

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Swap",
            description="Swap one of Pokémon from pool of the given generation before starting of League",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)

        em.add_field(name="Channel Specific Command.",
                     value="<#764672011087642645>")

        em.add_field(
            name="Syntax",
            value=f"`{prefix}swap <generation> <prev Pokémon> <new Pokémon>`\n\n*Generation can be 6 or 7*\n*Pokémon to be swapped*\n*Pokémon with whom to be swapped.*",
            inline=False)

        em.add_field(
            name="Aliases",
            value="`s` , `swap` , `sp` , `swap_pokemon` , `swap_pool` , `change`",
            inline=False)

        em.add_field(name="Usage",
                     value=f"`{prefix}swap 6 alakazam gengar`",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["pl", "pokemon"])
    async def pool(self, ctx):

        prefix = server_prefix(ctx)

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Pool",
            description="See your or anyone's currently registered pool of 12 Pokémon of the provided generation.",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)

        em.add_field(
            name="Syntax",
            value=f"`{prefix}pool <generation> <user>`\n\n*Generation can be 6 or 7*\n*Mention the user you wanna check*\n*It will show your pool by default if no user is mentioned.*",
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
    async def moderator(self, ctx):

        # prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Moderator Commands",
            colour=discord.Colour.green())
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(name="Change-Prefix", value="Change the Server Prefix of the Bot to a new one.")

        help_embed.add_field(name="Kick", value="Kick the Member out of the Server.")

        help_embed.add_field(name="Ban", value="Ban the Member from the Server.")

        help_embed.add_field(name="Unban", value="Unban the Member from the Server.")

        help_embed.add_field(name="Mute", value="Mute the Member for specific or non-specific time.")

        help_embed.add_field(name="Unmute", value="Unmute the Member previously Muted.")

        help_embed.add_field(name="Clear", value="Delete specified number of messages.")

        await ctx.send(embed=help_embed)

    @help.command(aliases=["hof"])
    async def hall_of_fame(self, ctx):

        prefix = server_prefix(ctx)

        if ctx.channel.name == "📝registration":
            return

        em = discord.Embed(
            title="Hall_of_fame",
            description="See the Hall of Fame of all the Champions formed in our server.",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)

        em.add_field(name="Syntax", value=f"`{prefix}hof`", inline=False)

        em.add_field(name="Aliases",
                     value="`hof` , `hall_of_fame`",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(aliases=["champ", "nc"])
    async def champion(self, ctx):

        prefix = server_prefix(ctx)

        em = discord.Embed(
            title="Champion",
            description="Command to make the mentioned user champion of the given generation",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)

        em.add_field(
            name="Needed Roles",
            value="<@&767742527818039317>, <@&776871326371020830>, <@&761514056439562240>",
            inline=False)

        em.add_field(
            name="Syntax",
            value=f"`{prefix}champ <generation> <user>`\n\n*Generation can be 6 or 7*\n*Mention the New Champion*",
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

        prefix = server_prefix(ctx)

        em = discord.Embed(
            title="Reset_streak",
            description="Reset the elite streak of the mention user of the generation and check if challenger had 4 elite streak to increase endured matches of the current champion by 1.",
            colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)

        em.add_field(
            name="Needed Roles",
            value="<@&767742527818039317>, <@&776871326371020830>, <@&761514056439562240>",
            inline=False)

        em.add_field(
            name="Syntax",
            value=f"`{prefix}res <generation> <user>`\n\n*Generation can be 6 or 7*\n*Mention the user whose streak to be reseted.*",
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

        prefix = server_prefix(ctx)

        em = discord.Embed(title="Elite_pool",
                           description="See the elite pool if available",
                           colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)

        em.add_field(
            name="Syntax",
            value=f"`{prefix}epl <generation> <user>`\n\n*Generation can be 6 or 7*\n*Mention the user you wanna check*\n*It will show your pool by default if no user is mentioned.*",
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

        prefix = server_prefix(ctx)

        em = discord.Embed(title="Elite_team",
                           description="Submit the elite team of a member.",
                           colour=discord.Colour.green())

        em.set_thumbnail(url=self.client.user.avatar_url)

        em.add_field(
            name="Needed Roles",
            value="<@&767743473116905474>, <@&761487391147950111>, <@&776871326371020830>, <@&761514056439562240>",
            inline=False)

        em.add_field(
            name="Syntax",
            value=f"`{prefix}et <generation> <user> <team>`\n\n*Generation can be 6 or 7*\n*Mention the user whose pool to be submitted*\n*User's used team in elite battle*",
            inline=False)

        em.add_field(name="Aliases",
                     value="`elite_team` , `et` , `ep`",
                     inline=False)

        em.add_field(
            name="Usage",
            value=f"`{prefix}et 6 @Sayan  Dragonite, Excadrill, Ferrothorn, Zapdos, Pinsir, Keldeo-resolute`",
            inline=False)

        await ctx.send(embed=em)

    @help.command()
    async def game(self, ctx):

        prefix = server_prefix(ctx)

        em = discord.Embed(title="Game", description="", colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)

        em.add_field(name=f"{prefix}GG", value="A basic guessing text based game.", inline=False)

        em.add_field(name=f"{prefix}tic-tac-toe", value=f"Play Tic-Tac-Toe with another member. Aliases: `{prefix}ttt`",
                     inline=False)
                     
        em.add_field(name=f"{prefix}rock-paper-scissors",
                     value=f"Play Rock-Paper-Scissors with the Bot. Aliases: `{prefix}rps`", inline=False)

        em.add_field(name=f"{prefix}trivia",
                     value=f"Get a random MCQ type question. Aliases: `{prefix}quiz`", inline=False)

        em.add_field(name=f"{prefix}gamelb",
                     value=f"Check the server's Leaderboard of Trivia. Use `{prefix}gamelb global` to see global Leaderboard.", inline=False)

        await ctx.send(embed=em)

    # @help.command(aliases=["phl"])
    # async def league(self, ctx):

    #     prefix = server_prefix(ctx)

    #     help_embed1 = discord.Embed(
    #         title="League Commands",
    #         description=f"If you need more information about a specific command, type `{prefix}help <command>` or `{prefix}h <command>`",
    #         colour=discord.Colour.green())
    #     help_embed1.set_footer(text="Page 1 of 2")
    #     help_embed1.set_thumbnail(url=self.client.user.avatar_url)

    #     help_embed2 = discord.Embed(
    #         title="League Commands",
    #         description=f"If you need more information about a specific command, type `{prefix}help <command>` or `{prefix}h <command>`",
    #         colour=discord.Colour.green())
    #     help_embed2.set_footer(text="Page 2 of 2")
    #     help_embed2.set_thumbnail(url=self.client.user.avatar_url)

    #     help_embed1.set_thumbnail(url=self.client.user.avatar_url)

    #     help_embed1.add_field(name="Register",
    #                           value="The registration command.")

    #     help_embed1.add_field(
    #         name="Swap",
    #         value="Swap one of your Pokémon of the desired generation before league starts")

    #     # help_embed1.add_field(name="Reset", value="Claim your reset token and swap 6 of your Pokémon Pool.")

    #     help_embed1.add_field(
    #         name="Profile",
    #         value="Check profile of provided generation and user.")

    #     help_embed1.add_field(
    #         name="Pool",
    #         value="See your or someone's current registered pool of the current generation.")

    #     # help_embed1.add_field(name="Check_team", value="Check if the battling team of the member mentioned is valid or not.", inline=False)

    #     help_embed1.add_field(
    #         name="Add_badge",
    #         value="Add defined badge of the provided generation to the mentioned user.")

    #     help_embed1.add_field(
    #         name="Elite_pool",
    #         value="Command to see and check the elite pool of a challenger.")

    #     help_embed1.add_field(
    #         name="Elite_team",
    #         value="Command to submit the elite team of the challenger.")

    #     help_embed2.add_field(
    #         name="Add_streak",
    #         value="Increase elite streak of the provided generation and mentioned user by one.")

    #     help_embed2.add_field(
    #         name="Reset_streak",
    #         value="Reset the elite streak if the member and if streak was 4, increase champion endurance by 1.")

    #     help_embed2.add_field(
    #         name="Champion",
    #         value="Make new champion and update hall of fame.")

    #     help_embed2.add_field(
    #         name="Hall_of_fame",
    #         value="See the Hall of Fame of all the champions.")

    #     help_embed2.add_field(
    #         name="Swap_close",
    #         value="Stops the Pokémon swappable option available earlier.")

    #     help_embed2.add_field(
    #         name="Restart_league",
    #         value="Erases the data of the Current league.")

    #     msg = await ctx.send(embed=help_embed1)

    #     await msg.add_reaction("◀️")
    #     await msg.add_reaction("▶️")

    #     def check(reaction, user):
    #         return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

    #     pages = 2
    #     cur_page = 1

    #     while True:
    #         try:
    #             reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)

    #             if str(reaction.emoji) == "▶️" and cur_page != pages:
    #                 cur_page += 1
    #                 await msg.edit(embed=help_embed2)
    #                 await msg.remove_reaction(reaction, user)

    #             elif str(reaction.emoji) == "◀️" and cur_page > 1:
    #                 cur_page -= 1
    #                 await msg.edit(embed=help_embed1)
    #                 await msg.remove_reaction(reaction, user)

    #             else:
    #                 await msg.remove_reaction(reaction, user)
    #         except asyncio.TimeoutError:
    #             await msg.clear_reaction("▶️")
    #             await msg.clear_reaction("◀️")

    # @help.command()
    # async def music(self, ctx):

    #     prefix = server_prefix(ctx)

    #     help_embed = discord.Embed(
    #         title="Music Commands", colour=discord.Colour.green())
    #     help_embed.set_thumbnail(url=self.client.user.avatar_url)

    #     help_embed.add_field(name="Join", value="Summons the bot to a voice channel.")

    #     help_embed.add_field(name="Leave", value="Clears the queue and leaves the voice channel.")

    #     help_embed.add_field(name="Play", value="Plays a song.")

    #     help_embed.add_field(name="Pause", value="Pauses the currently playing song.")

    #     help_embed.add_field(name="Resume", value="Resumes a currently paused song.")

    #     help_embed.add_field(name="Now", value="Displays the currently playing song.")

    #     help_embed.add_field(name="Stop", value="Stops playing song and clears the queue.")

    #     help_embed.add_field(name="Skip", value="Vote to skip a song.")

    #     help_embed.add_field(name="Queue", value="Shows the player's queue.")

    #     help_embed.add_field(name="Shuffle", value="Shuffles the queue")

    #     help_embed.add_field(name="Remove", value="Removes a song from the queue at a given index.")

    #     help_embed.add_field(name="Loop", value="Loops the currently playing song.")

    #     await ctx.send(embed=help_embed)

    @help.command()
    async def misc(self, ctx):

        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Misc Commands", colour=discord.Colour.green())
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(name="avatar", value="See the Avatar or Profile Picture of the desired Member.")

        help_embed.add_field(name="ID", value="Get the Snowflake ID of the desired Member.")

        help_embed.add_field(name="Icon", value="Get the server Icon.")

        help_embed.add_field(name="translate", value=f"Translate the passed sentence to desired Language. use `{prefix}help translate` for more info.")

        help_embed.add_field(name="Search", value="Search for the passed word in Web.")

        help_embed.add_field(name="Dictionary", value="Search for the passed word in Dictionary.")

        help_embed.add_field(name="Snipe", value="Snipe for the last deleted message from the channel.")

        help_embed.add_field(name="Invite", value="Get an Invite Link to add the Bot to your server.")

        await ctx.send(embed=help_embed)

    @help.command()
    async def fun(self, ctx):

        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Fun Commands", colour=discord.Colour.green())
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(name="Roll", value="Roll Dices.")

        help_embed.add_field(name="Toss", value="Flip a Coin.")

        help_embed.add_field(name="Urban", value="Search for the passed word in Urban Dictionary.")

        help_embed.add_field(name=f"{prefix}8Pool",
                     value="Play 8Pool. See your Fortune or take advice.", inline=False)

        help_embed.add_field(name="Poll", value=f"Create a Poll. Use `{prefix}help poll` for more info.")

        help_embed.add_field(name="Show_Poll", value="Shows result of a previously created Poll.")

        await ctx.send(embed=help_embed)

    @help.command()
    async def poll(self, ctx):

        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Poll Command",
            description="Create a Poll for members to vote, upto 20 Options.", colour=discord.Colour.green())
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(name="Usage:", value=f"`{prefix}poll <Question> // <Option1>,<Option2>,<Option3>...`", inline=False)

        help_embed.add_field(name="Alter:", value=f"`{prefix}Show_Poll <poll message link>/<poll message ID>` to see the result of a previously created Poll.")

        await ctx.send(embed=help_embed)


    @help.command(aliases=["t"])
    async def translate(self, ctx):

        raw_flags = {
            "🇮🇳": "Hindi",
            "🇺🇸": "English",
            "🇬🇧": "English",
            "🇪🇸": "Spanish",
            "🇯🇵": "Japanese",
            "🇧🇩": "Bangla",
            "🇫🇷": "French",
            "🇩🇪": "German",
            "🇰🇵": "Korean",
            "🇳🇵": "Nepali",
            "🇵🇭": "Filipino"
        }

        flag = ""

        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Translate Command",
            description=f"Translate the passed text to the desired language.\nOr react with Country Flags to translate to the country's Language\nAvailable Flag Languages:" , colour=discord.Colour.green())
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        for i in raw_flags:
            flag += f"{i} : {raw_flags[i]}\n"
            help_embed.add_field(name=f"{i}", value=f"{raw_flags[i]}")

        # lang = ""

        # for i in LANGUAGES:
        #     if lang == "":
        #         lang += f"{i}: {LANGUAGES[i]}"
        #     else:
        #         lang += f", {i}: {LANGUAGES[i]}"


        # help_embed.add_field(name="Languages", value=lang, inline=False)

        help_embed.add_field(name="Aliases:", value=f"`{prefix}t` , `{prefix}translate`", inline=False)


        await ctx.send(embed=help_embed)

    @help.command()
    async def pokedex(self, ctx):

        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Pokedex Commands", colour=discord.Colour.green())
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(name="dex", value="Get Information of a Pokémon.")

        help_embed.add_field(name="move", value="Get Information of a Move.")

        help_embed.add_field(name="item", value="Get Information of an Item.")

        help_embed.add_field(name="ability", value=f"Get Information of an Ability.")

        help_embed.add_field(name="nature", value=f"Get Information of a Nature.")

        help_embed.add_field(name="data", value=f"Get Information of a Pokémon, ability, move, item, or nature.")

        help_embed.add_field(name="learn", value=f"Get Information of a Pokémon Learnset, add optional move to show how that Pokémon learns that move.")

        help_embed.add_field(name="filter", value=f"Search Pokémon based on user-inputted parameters. Use `{prefix}help filter` for more information.")

        await ctx.send(embed=help_embed)

    @help.command()
    async def badge(self, ctx):

        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Badge System Commands", colour=discord.Colour.green())
        help_embed.set_thumbnail(url=self.client.user.avatar_url)
        help_embed.set_footer(text=f"Argument in {{}} are Optional argument and in [] are required.")

        help_embed.add_field(name=f"{prefix}badges {{user}}", value="View your current Gym Badges (or someone else's) in the server.")

        help_embed.add_field(name=f"{prefix}gyms", value="View all the Gym Leaders of the server.")

        help_embed.add_field(name=f"{prefix}glrole [role]", value="Add a Gym Leader role for Gym Leader commands.")

        help_embed.add_field(name=f"{prefix}elrole [role]", value="Add a Elite role for Elite commands.")

        help_embed.add_field(name=f"{prefix}badgen [badge name] [badge emoji]", value="Add a new badge for the server.")

        help_embed.add_field(name=f"{prefix}leaderadd [user] [badge]", value="Add a Gym Leader. Need to add badge first.")

        help_embed.add_field(name=f"{prefix}leaderremove [user] [badge]", value="Remove a Gym Leader.")

        help_embed.add_field(name=f"{prefix}award [user] {{badge}}", value="Award a Gym Badge to a challenger.")

        help_embed.add_field(name=f"{prefix}revoke [user] {{badge}}", value="Revoke a Gym Badge from a challenger.")

        help_embed.add_field(name=f"{prefix}streaka [user]", value="Add a Elite Streak to a challenger.")

        help_embed.add_field(name=f"{prefix}streakr [user]", value="Remove all Elite Streak from a challenger.")

        help_embed.add_field(name=f"{prefix}badgereset", value=f"Erase all badges from all Users in the given server.")

        await ctx.send(embed=help_embed)

    @help.command()
    async def filter(self, ctx):

        # prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="filter Command",
            description=f"Search Pokémon based on user-inputted parameters. Availible parameters are:" , colour=discord.Colour.green())
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(name="hp/hitpoints", value="Eg: hp=100 or hp>100 or hp<100")
        help_embed.add_field(name="atk/attack", value="Eg: atk=100 or atk>100 or atk<100")
        help_embed.add_field(name="def/defense", value="Eg: def=100 or def>100 or def<100")
        help_embed.add_field(name="spa/specialattack", value="Eg: spa=100 or spa>100 or spa<100")
        help_embed.add_field(name="spd/speicaldefense", value="Eg: spd=100 or spd>100 or spd<100")
        help_embed.add_field(name="spe/speed", value="Eg: spe=100 or spe>100 or spe<100")

        help_embed.add_field(name="ability", value="Eg: ability=flash fire")
        help_embed.add_field(name="move", value="Eg: move=lavaplume")
        help_embed.add_field(name="type", value="Eg: type=fire")
        
        help_embed.set_footer(text="For multiple value in type or move use parameter multiple times or separated by a ; Eg: type=fire;steel")

        await ctx.send(embed=help_embed)

def setup(client):
    client.add_cog(Help(client))
