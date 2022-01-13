import discord
from discord.ext import commands
from replit import db
import asyncio


def server_prefix(message):
    """
    get bot prefix from database and set bot prefix for guild/server

    :param message: message sent in a server channel
    :return: bot prefix
    """
    if isinstance(message.message.channel, discord.channel.DMChannel):
        return "."

    prefixes = db["prefixes"]
    s_prefix = prefixes[str(message.guild.id)]

    return s_prefix


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["h"])
    async def help(self, ctx):
        """
        display help menu in embed

        :param self: Help class
        :param ctx: Discord.py command context
        """
        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Commands",
            description=f"If you need more information about a specific category, type `{prefix}help <category>` or `{prefix}h <category>`",
            colour=discord.Colour.green(),
        )

        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        # help_embed.add_field(name="🔨 Moderator", value=f"`{prefix}help mod`")

        help_embed.add_field(
            name="📛Badge System", value=f"`{prefix}help badge`", inline=False
        )

        help_embed.add_field(
            name="🎴 Pokedex", value=f"`{prefix}help pokedex`", inline=False
        )

        help_embed.add_field(name="🎮 Game", value=f"`{prefix}help game`", inline=False)

        help_embed.add_field(name="🎪 Fun", value=f"`{prefix}help fun`", inline=False)

        help_embed.add_field(name="🎶 Music", value=f"`{prefix}help music`")

        help_embed.add_field(name="🎉 Misc", value=f"`{prefix}help misc`", inline=False)

        help_embed.set_footer(
            text=f"Use {prefix}prefix [new_prefix] to change Bot's Prefix."
        )

        await ctx.send(embed=help_embed)

    @help.command()
    async def game(self, ctx):
        """
        display help menu for game command in embed

        :param self: Help class
        :param ctx: Discord.py command context
        """
        prefix = server_prefix(ctx)

        em = discord.Embed(title="Game", description="", colour=discord.Colour.green())
        em.set_thumbnail(url=self.client.user.avatar_url)

        em.add_field(
            name=f"{prefix}GG", value="A basic guessing text based game.", inline=False
        )

        em.add_field(
            name=f"{prefix}tic-tac-toe",
            value=f"Play Tic-Tac-Toe with another member. Aliases: `{prefix}ttt`",
            inline=False,
        )

        em.add_field(
            name=f"{prefix}rock-paper-scissors",
            value=f"Play Rock-Paper-Scissors with the Bot. Aliases: `{prefix}rps`",
            inline=False,
        )

        await ctx.send(embed=em)

    @help.command()
    async def music(self, ctx):
        """
        display help menu for music command in embed

        :param self: Help class
        :param ctx: Discord.py command context
        """
        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Music Commands", colour=discord.Colour.green()
        )
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(
            name="Join",
            value="Summons the bot to a voice channel. If no channel was specified, it joins your channel.",
        )

        help_embed.add_field(
            name="Leave", value="Clears the queue and leaves the voice channel."
        )

        help_embed.add_field(
            name="Play",
            value="Plays a song. If there are songs in the queue, this will be queued until the other songs finished playing.",
        )

        help_embed.add_field(name="Pause", value="Pauses the currently playing song.")

        help_embed.add_field(name="Resume", value="Resumes a currently paused song.")

        help_embed.add_field(name="Now", value="Displays the currently playing song.")

        help_embed.add_field(
            name="Stop", value="Stops playing song and clears the queue."
        )

        help_embed.add_field(
            name="Skip",
            value="Vote to skip a song. The requester can automatically skip. 3 skip votes are needed for the song to be skipped.",
        )

        help_embed.add_field(
            name="Queue",
            value="Shows the player's queue. You can optionally specify the page to show. Each page contains 10 elements.",
        )

        help_embed.add_field(name="Shuffle", value="Shuffles the queue")

        help_embed.add_field(
            name="Remove", value="Removes a song from the queue at a given index."
        )

        help_embed.add_field(
            name="Loop",
            value="Loops the currently playing song. Use this command again to unloop the song.",
        )

        await ctx.send(embed=help_embed)

    @help.command()
    async def misc(self, ctx):
        """
        display help menu for misc command in embed

        :param self: Help class
        :param ctx: Discord.py command context
        """
        prefix = server_prefix(ctx)

        help_embed = discord.Embed(title="Misc Commands", colour=discord.Colour.green())
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(
            name="avatar",
            value="See the Avatar or Profile Picture of the desired Member.",
        )

        help_embed.add_field(
            name="ID", value="Get the Snowflake ID of the desired Member."
        )

        help_embed.add_field(name="Icon", value="Get the server Icon.")

        help_embed.add_field(
            name="translate",
            value=f"Translate the passed sentence to desired Language. use `{prefix}help translate` for more info.",
        )

        help_embed.add_field(name="Search", value="Search for the passed word in Web.")

        help_embed.add_field(
            name="Dictionary", value="Search for the passed word in Dictionary."
        )

        help_embed.add_field(
            name="Snipe", value="Snipe for the last deleted message from the channel."
        )

        help_embed.add_field(
            name="serverinfo", value="Get some informations about the server."
        )

        help_embed.add_field(
            name="say",
            value="Make Bot say something for you. `Bot needs manage_messages and manage_webhooks permission for this.`",
        )

        help_embed.add_field(
            name="Invite", value="Get an Invite Link to add the Bot to your server."
        )

        await ctx.send(embed=help_embed)

    @help.command()
    async def fun(self, ctx):
        """
        display help menu for fun command in embed

        :param self: Help class
        :param ctx: Discord.py command context
        """
        prefix = server_prefix(ctx)

        help_embed = discord.Embed(title="Fun Commands", colour=discord.Colour.green())
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(name="Roll", value="Roll Dices.")

        help_embed.add_field(name="Toss", value="Flip a Coin.")

        help_embed.add_field(
            name="Urban", value="Search for the passed word in Urban Dictionary."
        )

        help_embed.add_field(
            name=f"{prefix}8Pool",
            value="Play 8Pool. See your Fortune or take advice.",
            inline=True,
        )

        help_embed.add_field(
            name="Poll", value=f"Create a Poll. Use `{prefix}help poll` for more info."
        )

        help_embed.add_field(
            name="Show_Poll", value="Shows result of a previously created Poll."
        )

        await ctx.send(embed=help_embed)

    @help.command()
    async def poll(self, ctx):
        """
        display help menu for poll feature in embed

        :param self: Help class
        :param ctx: Discord.py command context
        """
        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Poll Command",
            description="Create a Poll for members to vote, upto 20 Options.",
            colour=discord.Colour.green(),
        )
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(
            name="Usage:",
            value=f"`{prefix}poll <Question> // <Option1>,<Option2>,<Option3>...`",
            inline=False,
        )

        help_embed.add_field(
            name="Alter:",
            value=f"`{prefix}Show_Poll <poll message link>/<poll message ID>` to see the result of a previously created Poll.",
        )

        await ctx.send(embed=help_embed)

    @help.command(aliases=["t"])
    async def translate(self, ctx):
        """
        display help menu for translate command in embed

        :param self: Help class
        :param ctx: Discord.py command context
        """
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
            "🇵🇭": "Filipino",
        }

        flag = ""

        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Translate Command",
            description=f"Translate the passed text to the desired language.\nOr react with Country Flags to translate to the country's Language\nAvailable Flag Languages:",
            colour=discord.Colour.green(),
        )
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

        help_embed.add_field(
            name="Aliases:", value=f"`{prefix}t` , `{prefix}translate`", inline=False
        )

        await ctx.send(embed=help_embed)

    @help.command()
    async def pokedex(self, ctx):
        """
        display help menu for pokedex command in embed

        :param self: Help class
        :param ctx: Discord.py command context
        """
        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Pokedex Commands", colour=discord.Colour.green()
        )
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(name="dex", value="Get Information of a Pokémon.")

        help_embed.add_field(name="move", value="Get Information of a Move.")

        help_embed.add_field(name="item", value="Get Information of an Item.")

        help_embed.add_field(name="ability", value=f"Get Information of an Ability.")

        help_embed.add_field(name="nature", value=f"Get Information of a Nature.")

        help_embed.add_field(
            name="data",
            value=f"Get Information of a Pokémon, ability, move, item, or nature.",
        )

        help_embed.add_field(
            name="learn",
            value=f"Get Information of a Pokémon Learnset, add optional move to show how that Pokémon learns that move.",
        )

        help_embed.add_field(
            name="filter",
            value=f"Search Pokémon based on user-inputted parameters. Use `{prefix}help filter` for more information.",
        )

        await ctx.send(embed=help_embed)

    @help.command()
    async def badge(self, ctx):
        """
        display help menu for badge command in embed

        :param self: Help class
        :param ctx: Discord.py command context
        """
        prefix = server_prefix(ctx)

        help_embed = discord.Embed(
            title="Badge System Commands", colour=discord.Colour.green()
        )
        help_embed.set_thumbnail(url=self.client.user.avatar_url)
        help_embed.set_footer(
            text=f"Argument in {{}} are Optional argument and in [] are required."
        )

        help_embed.add_field(
            name=f"{prefix}badges {{user}}",
            value="View your current Gym Badges (or someone else's) in the server.",
        )

        help_embed.add_field(
            name=f"{prefix}gyms", value="View all the Gym Leaders of the server."
        )

        help_embed.add_field(
            name=f"{prefix}sbadges", value="View all the Badges of the server."
        )

        help_embed.add_field(
            name=f"{prefix}glrole [role]",
            value="Add a Gym Leader role for Gym Leader commands.",
        )

        help_embed.add_field(
            name=f"{prefix}elrole [role]", value="Add a Elite role for Elite commands."
        )

        help_embed.add_field(
            name=f"{prefix}badgen [badge name] [badge emoji]",
            value="Add a new badge for the server.",
        )

        help_embed.add_field(
            name=f"{prefix}leaderadd [user] [badge]",
            value="Add a Gym Leader. Need to add badge first.",
        )

        help_embed.add_field(
            name=f"{prefix}leaderremove [user] [badge]", value="Remove a Gym Leader."
        )

        help_embed.add_field(
            name=f"{prefix}award [user] {{badge}}",
            value="Award a Gym Badge to a challenger.",
        )

        help_embed.add_field(
            name=f"{prefix}revoke [user] {{badge}}",
            value="Revoke a Gym Badge from a challenger.",
        )

        help_embed.add_field(
            name=f"{prefix}badgelb", value=f"Check the server's Leaderboard of Badges."
        )

        help_embed.add_field(
            name=f"{prefix}streaka [user]", value="Add a Elite Streak to a challenger."
        )

        help_embed.add_field(
            name=f"{prefix}streakr [user]",
            value="Remove all Elite Streak from a challenger.",
        )

        help_embed.add_field(
            name=f"{prefix}badgereset",
            value=f"Erase all badges from all Users in the given server.",
        )

        await ctx.send(embed=help_embed)

    @help.command()
    async def filter(self, ctx):
        """
        display help menu for pokemon filter command in embed

        :param self: Help class
        :param ctx: Discord.py command context
        """
        help_embed = discord.Embed(
            title="filter Command",
            description=f"Search Pokémon based on user-inputted parameters. Availible parameters are:",
            colour=discord.Colour.green(),
        )
        help_embed.set_thumbnail(url=self.client.user.avatar_url)

        help_embed.add_field(
            name="hp/hitpoints", value="Eg: hp=100 or hp>100 or hp<100"
        )
        help_embed.add_field(
            name="atk/attack", value="Eg: atk=100 or atk>100 or atk<100"
        )
        help_embed.add_field(
            name="def/defense", value="Eg: def=100 or def>100 or def<100"
        )
        help_embed.add_field(
            name="spa/specialattack", value="Eg: spa=100 or spa>100 or spa<100"
        )
        help_embed.add_field(
            name="spd/speicaldefense", value="Eg: spd=100 or spd>100 or spd<100"
        )
        help_embed.add_field(
            name="spe/speed", value="Eg: spe=100 or spe>100 or spe<100"
        )

        help_embed.add_field(name="ability", value="Eg: ability=flash fire")
        help_embed.add_field(name="move", value="Eg: move=lavaplume")
        help_embed.add_field(name="type", value="Eg: type=fire")

        help_embed.set_footer(
            text="For multiple value in type or move use parameter multiple times or separated by a ; Eg: type=fire;steel"
        )

        await ctx.send(embed=help_embed)


def setup(client):
    """
    Add Help extension/cog to client

    :param client: Discord.py bot client
    """
    client.add_cog(Help(client))
