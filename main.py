import discord
from discord.ext import commands, tasks
from replit import db
import os
import keep_alive
from itertools import cycle
from bprofanity import profanity
import asyncio
import string
import datetime
import json

# import pymongo, dns

# mongoKey = os.environ.get("mongoDB")
# mclient = pymongo.MongoClient(mongoKey)

save = db["mod"]


def get_prefix(client, message):
    """
    get bot prefix from database and set bot prefix for guild/server

    :param client: Discord.py client
    :param message: message sent in a server channel
    :return: bot prefix
    """
    if isinstance(message.channel, discord.channel.DMChannel):
        return "."

    guilds = db["prefixes"]
    guild_id = str(message.guild.id)
    prefix = guilds.get(guild_id, ".")

    # if guild id not found in guilds list, set bot prefix to . and update database
    if guild_id not in guilds:
        guilds[guild_id] = "."
        db["prefixes"] = guilds

    return prefix


# initialize bot
prefix = get_prefix
current_title = "Smeargle Fling Moody Tour"
intents = discord.Intents.all()

presence = cycle(
    [
        discord.Activity(type=discord.ActivityType.listening, name=".help"),
        discord.Activity(type=discord.ActivityType.watching, name="The Pokéhub"),
    ]
)

client = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True)
dbs = ["league_prof7", "gen7", "hall_of_fame", "league_prof6", "gen6", "mod"]


sni_json = "snipe/snipe.json"
esni_json = "snipe/esnipe.json"


@client.event
async def on_ready():
    """set up bot after login into discord servers successful"""
    change_presence.start()
    del_snipe.start()

    client.remove_command("help")

    # load cogs from directories
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

    # clear snipe and edit snipe json files
    with open(sni_json, "w") as snipe_file:
        json.dump({}, snipe_file)

    with open(esni_json, "w") as esnipe_file:
        json.dump({}, esnipe_file)

    print(f"Bot is Ready.\nLogged in as {client.user.name}\n-----------------------")
    version = discord.__version__.replace(" ", "")
    print("discord.py Version: v" + version)


def replace_double_characters(str):
    """
    replace double characters in string

    :param str: message string
    :return: new message string
    """
    prev_letter, new_str = "", ""
    for char in str:
        if char != prev_letter:
            new_str += char
        prev_letter = char
    return new_str


@client.event
async def on_message(message):
    """
    execute function whenever someone sends a message

    :param message: message string
    """
    if message.author == client.user:
        return

    # ignore message if message is in Myuu channel
    if message.channel.id == 884745067607228456:
        return

    # when someone pings bot
    if client.user.mentioned_in(message):
        if "hello" in message.content.lower():
            await message.channel.send(
                f"Hello {message.author.mention}.\nMy prefix for this server is `{get_prefix(client, message)}`"
            )

    # check profanity in message
    # remove all punctuation from message
    profanity_check_msg = message.content.translate(
        str.maketrans("", "", string.punctuation)
    )

    if profanity.contains_profanity(
        profanity_check_msg
    ) or profanity.contains_profanity(replace_double_characters(profanity_check_msg)):

        # profanity checks only work in Pokehub server
        if message.guild.id == 676777139776913408:

            # ignore profanity in Genshin channel
            if message.channel.id == 882939775177355304:
                pass

            # ignore profanity if message is sent by a bot
            elif not message.author.bot:

                try:
                    await message.delete()
                except discord.errors.NotFound:
                    pass

                embed = discord.Embed(
                    description=f"**{message.author.mention} you are not allowed to say that.**",
                    colour=discord.Colour.red(),
                )

                msg = await message.channel.send(embed=embed)

                em = discord.Embed(
                    title="Deleted Message",
                    description=f"From {message.author.mention} in <#{message.channel.id}>",
                    colour=discord.Colour.red(),
                )

                em.add_field(name="Message", value=message.content)
                em.timestamp = datetime.datetime.utcnow()

                channel = client.get_channel(836139191666343966)
                await channel.send(embed=em)

                await asyncio.sleep(10)
                try:
                    await msg.delete()
                except discord.errors.NotFound:
                    pass

    # give trainers and advanced trainers role when they hit lv1 and lv15 respectively
    if message.channel.id == 775388498919948299:
        if "you just advanced to level 15!" in message.content:
            member_id = "".join(filter(lambda i: i.isdigit(), message.content))

            mem = await message.guild.fetch_member(int(member_id[:-2]))
            role = discord.utils.get(message.guild.roles, name="advanced-trainers")

            await mem.add_roles(role)

        if "you just advanced to level 1!" in message.content:
            member_id = "".join(filter(lambda i: i.isdigit(), message.content))

            mem = await message.guild.fetch_member(int(member_id[:-1]))
            role = discord.utils.get(message.guild.roles, name="trainers")

            if role not in mem.roles:

                await mem.add_roles(role)

    pfx = get_prefix(client, message).lower()

    if message.content.lower().startswith(pfx):
        message.content = (
            message.content[: len(pfx)].lower() + message.content[len(pfx) :]
        )

    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    """
    add guild id to db whenever bot joins a new server/guild

    :param guild: guild/server object
    """
    prefixes = db["prefixes"]
    prefixes[str(guild.id)] = "."
    db["prefixes"] = prefixes


@client.event
async def on_guild_leave(guild):
    """
    remove guild id from db whenever bot leaves a server/guild

    :param guild: guild/server object
    """
    prefixes = db["prefixes"]
    del prefixes[str(guild.id)]
    db["prefixes"] = prefixes


@client.event
async def on_command_error(ctx, error):
    """
    send error as message is bot command produces an error

    :param ctx: discord.py command context
    :param error: discord.py error object
    """
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, discord.errors.NotFound):
        pass
    else:
        try:
            msg = await ctx.send("{}".format(str(error)))
            await asyncio.sleep(5)
            await msg.delete()
        except:
            pass


@client.event
async def on_message_delete(message):
    """
    add message to snipe store whenever a message is deleted

    :param message: deleted message string
    """
    with open(sni_json, "r") as snipe_file:
        data = json.load(snipe_file)

    if message.attachments:
        attach = str(message.attachments[0])
    else:
        attach = None

    data[str(message.channel.id)] = {
        "author": str(message.author),
        "content": message.content,
        "attachment": attach,
        "time": datetime.datetime.timestamp(datetime.datetime.utcnow()),
    }

    with open(sni_json, "w") as snipe_file:
        json.dump(data, snipe_file)


@client.event
async def on_message_edit(before, after):
    """
    add message to edited snipe store whenever a message is edited

    :param before: message before edit
    :param after: message after edit
    """
    with open(esni_json, "r") as esnipe_file:
        data = json.load(esnipe_file)

    profanity_check_msg = after.content.translate(
        str.maketrans("", "", string.punctuation)
    )

    # check for profanity on edited message
    if profanity.contains_profanity(
        profanity_check_msg
    ) or profanity.contains_profanity(replace_double_characters(profanity_check_msg)):
        try:
            await after.delete()

            embed = discord.Embed(
                description=f"**{after.author.mention} you are not allowed to say that.**",
                colour=discord.Colour.red(),
            )

            msg = await after.channel.send(embed=embed)

            em = discord.Embed(
                title="Deleted Message",
                description=f"From {after.author.mention} in <#{after.channel.id}>",
                colour=discord.Colour.red(),
            )

            em.add_field(name="Message", value=after.content)
            em.timestamp = datetime.datetime.utcnow()

            channel = client.get_channel(836139191666343966)
            await channel.send(embed=em)

            await asyncio.sleep(10)
            await msg.delete()

        except:
            pass

    data[str(before.channel.id)] = {
        "author": str(before.author),
        "content": before.content,
        "link": before.jump_url,
        "time": datetime.datetime.timestamp(datetime.datetime.utcnow()),
    }

    with open(esni_json, "w") as esnipe_file:
        json.dump(data, esnipe_file)


@client.command()
async def snipe(ctx):
    """
    display message that has just been deleted recently

    :param ctx: discord.py command context
    """
    # dont snipe if message is in registration channel
    if ctx.channel.id == 861952254072586240:
        return

    channel = ctx.channel

    with open(sni_json, "r") as snipe_file:
        data = json.load(snipe_file)

    try:
        message = data[str(channel.id)]

        profanity_check_msg = message["content"].translate(
            str.maketrans("", "", string.punctuation)
        )

        # check for profanity in sniped message
        if profanity.contains_profanity(
            profanity_check_msg
        ) or profanity.contains_profanity(
            replace_double_characters(profanity_check_msg)
        ):
            return await ctx.send(
                "Deleted message contains words which is not allowed."
            )

        # send Mike Wazowski emoji if message contains "discord.gg" or contains more than 5 emojis
        elif "discord.gg" in message["content"]:
            return await ctx.send("<:uhh:880305186827014195> ")

        if message["content"].count(":") > 11:
            return await ctx.send("<:uhh:880305186827014195> ")

        snipeEmbed = discord.Embed(
            title=f"Last Deleted message in #{channel.name}",
            description=f"{message['content']}",
        )

        snipeEmbed.set_footer(text=f"Message sent by {message['author']}")

        if message["attachment"]:
            snipeEmbed.set_image(url=message["attachment"])

        await ctx.send(embed=snipeEmbed)

    except:
        await ctx.send(f"There are no deleted messages in {channel.mention}")


@client.command(aliases=["es", "edit-snipe", "esnipe"])
async def edit_snipe(ctx):
    """
    display message that has just been edited recently

    :param ctx: discord.py command context
    """
    channel = ctx.channel

    with open(esni_json, "r") as esnipe_file:
        data = json.load(esnipe_file)

    try:
        cont = data[str(channel.id)]
        snipeEmbed = discord.Embed(
            title=f"Last Edited message in #{channel.name}",
            description=f"{cont['content']}\n\n[*__Message__*]({cont['link']})",
        )

        snipeEmbed.set_footer(text=f"Message edited by {cont['author']}")
        await ctx.send(embed=snipeEmbed)
    except:
        await ctx.send(f"There are no edited messages in {channel.mention}")


@client.command()
@commands.is_owner()
async def reload(ctx):
    """
    reload bot cogs/extensions

    :param ctx: discord.py command context
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.unload_extension(f"cogs.{filename[:-3]}")
            client.load_extension(f"cogs.{filename[:-3]}")

    await ctx.send("Extensions has been reloaded.")


@tasks.loop(seconds=10)
async def change_presence():
    """change bot sidebar status every 10 seconds"""
    await client.change_presence(activity=next(presence))


@tasks.loop(minutes=5)
async def del_snipe():
    """clear sniped and edited sniped messages from stores after 1 minute"""
    datad = {}
    datad2 = {}

    with open(sni_json, "r") as snipe_file:
        data = json.load(snipe_file)

    with open(esni_json, "r") as esnipe_file:
        data2 = json.load(esnipe_file)

    for i in data:
        t1 = data[i]["time"]
        t2 = datetime.datetime.timestamp(datetime.datetime.utcnow())

        if t2 - t1 < 60:
            datad[i] = data[i]

    for i in data2:
        t1 = data2[i]["time"]
        t2 = datetime.datetime.timestamp(datetime.datetime.utcnow())

        if t2 - t1 < 60:
            datad[i] = data2[i]

    with open(sni_json, "w") as snipe_file:
        json.dump(datad, snipe_file)

    with open(esni_json, "w") as esnipe_file:
        json.dump(datad2, esnipe_file)


keep_alive.keep_alive()
client.run(os.environ.get("TOKEN"))

# Rate Limit Fix: "kill 1"
