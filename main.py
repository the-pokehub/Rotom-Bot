import discord
from discord.ext import commands, tasks
import os
import keep_alive
from itertools import cycle
from replit import db
from bprofanity import profanity
import asyncio
import string
import datetime
import json
import time
# import random
# import pymongo, dns

# mongoKey = os.environ.get("mongoDB")
# mclient = pymongo.MongoClient(mongoKey)  


save = db["mod"]


def get_prefix(client, message):

    if isinstance(message.channel, discord.channel.DMChannel):
        return "."
        
    guild = db["prefixes"]
    ret = guild.get(str(message.guild.id), ".")

    if str(message.guild.id) not in guild:
        guild[str(message.guild.id)] = "."

        db["prefixes"] = guild

    return ret


prefix = get_prefix
# filter = get_filter

# current_title = str(save["current_league"])
current_title = "Smeargle Fling Moody Tour"
intents = discord.Intents.all()

presence = cycle([
    discord.Activity(type=discord.ActivityType.listening, name=".help"),
    discord.Activity(type=discord.ActivityType.watching, name="The Pokéhub")
])

client = commands.Bot(command_prefix=prefix,
                    intents=intents,
                    case_insensitive=True)


dbs = ['league_prof7', 'gen7', 'hall_of_fame', 'league_prof6', 'gen6', 'mod']

@client.event
async def on_ready():
    change_presence.start()
    del_snipe.start()

    client.remove_command("help")

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")
    
    data = {}
    data2 = {}

    with open(sni, "w") as bd:
        json.dump(data, bd) 

    with open(esni, "w") as bd2:
        json.dump(data2, bd2)

    print(f"Bot is Ready.\nLogged in as {client.user.name}\n-----------------------")
    version = discord.__version__.replace(" ", "")
    print("discord.py Version: v" + version)


@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.channel.id == 884745067607228456:
        return

    # if message.content.lower == "<@783598148039868426> hello" or message.content.lower == "<@!783598148039868426> hello":

    #     await message.channel.send(f"Hello {message.author.mention}.\nMy prefix for this server is {prefix}")

    if client.user.mentioned_in(message):
        if "hello" in message.content.lower():
            await message.channel.send(f"Hello {message.author.mention}.\nMy prefix for this server is `{get_prefix(client, message)}`")

    profanity_check_msg = message.content.translate(
        str.maketrans('', '', string.punctuation))

    def replaceDoubleCharacters(string):
        lastLetter, replacedString = "", ""
        for letter in string:
            if letter != lastLetter:
                replacedString += letter
            lastLetter = letter
        return replacedString

    if profanity.contains_profanity(profanity_check_msg) or profanity.contains_profanity(replaceDoubleCharacters(profanity_check_msg)):
        # if message.author.id == 549415697726439434:
        #     return

        if message.guild.id == 676777139776913408:

            if message.channel.id == 882939775177355304:
                pass

            elif not message.author.bot:

                try:
                    await message.delete()
                except discord.errors.NotFound:
                    pass

                embed = discord.Embed(
                    description=
                    f"**{message.author.mention} you are not allowed to say that.**",
                    colour=discord.Colour.red())

                msg = await message.channel.send(embed=embed)

                em = discord.Embed(
                    title="Deleted Message",
                    description=
                    f"From {message.author.mention} in <#{message.channel.id}>",
                    colour=discord.Colour.red())

                em.add_field(name="Message", value=message.content)
                em.timestamp = datetime.datetime.utcnow()

                channel = client.get_channel(836139191666343966)
                await channel.send(embed=em)

                await asyncio.sleep(10)
                try:
                    await msg.delete()
                except discord.errors.NotFound:
                    pass

    if message.channel.id == 775388498919948299:
        if "you just advanced to level 15!" in message.content:
            member_id = ''.join(filter(lambda i: i.isdigit(), message.content))

            mem = await message.guild.fetch_member(int(member_id[:-2]))
            role = discord.utils.get(message.guild.roles,
                                    name="advanced-trainers")

            await mem.add_roles(role)

        if "you just advanced to level 1!" in message.content:
            member_id = ''.join(filter(lambda i: i.isdigit(), message.content))

            mem = await message.guild.fetch_member(int(member_id[:-1]))
            role = discord.utils.get(message.guild.roles, name="trainers")

            if role not in mem.roles:
        
                await mem.add_roles(role)
                
    pfx = get_prefix(client, message).lower()

    if message.content.lower().startswith(pfx):
        message.content = message.content[:len(pfx)].lower() + message.content[len(pfx):]

    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    prefixes = db["prefixes"]
    prefixes[str(guild.id)] = "."
    db["prefixes"] = prefixes


@client.event
async def on_guild_leave(guild):
    prefixes = db["prefixes"]
    del prefixes[str(guild.id)]
    db["prefixes"] = prefixes


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, discord.errors.NotFound):
        pass
    else:
        try:
            msg = await ctx.send('{}'.format(str(error)))
            await asyncio.sleep(5)
            await msg.delete()
        except:
            pass


# snipe_message_author = {}
# snipe_message_content = {}
# esnipe_message_author = {}
# esnipe_message_content = {}
# esnipe_message_link = {}

sni = "snipe/snipe.json"
esni = "snipe/esnipe.json"

@client.event
async def on_message_delete(message):

    with open(sni, "r") as bd:
        data = json.load(bd)

    if message.attachments:
        attach = str(message.attachments[0])
    else:
        attach = None

    data[str(message.channel.id)] = {
        "author": str(message.author),
        "content": message.content,
        "attachment": attach    
    }

    with open(sni, "w") as bd:
        json.dump(data, bd)
    

@client.event
async def on_message_edit(before, after):

    with open(esni, "r") as bd:
        data = json.load(bd)

    data[str(before.channel.id)] = {
        "author": str(before.author),
        "content": before.content,
        "link": before.jump_url    
    }

    with open(esni, "w") as bd:
        json.dump(data, bd)



@client.command()
async def snipe(ctx):
    channel = ctx.channel

    with open(sni, "r") as bd:
        data = json.load(bd)

    try:

        message = data[str(channel.id)]

        profanity_check_msg = message['content'].translate(
        str.maketrans('', '', string.punctuation))

        def replaceDoubleCharacters(string):
            lastLetter, replacedString = "", ""
            for letter in string:
                if letter != lastLetter:
                    replacedString += letter
                lastLetter = letter
            return replacedString

        if profanity.contains_profanity(profanity_check_msg) or profanity.contains_profanity(replaceDoubleCharacters(profanity_check_msg)):
            return await ctx.send("Deleted message contains words which is not allowed.")

        snipeEmbed = discord.Embed(title=f"Last Deleted message in #{channel.name}", description = f"{message['content']}")

        snipeEmbed.set_footer(text=f"Message sent by {message['author']}")

        if message['attachment']:
            snipeEmbed.set_image(url=message['attachment'])

        await ctx.send(embed = snipeEmbed)

    except:
        await ctx.send(f"There are no deleted messages in {channel.mention}")


@client.command(aliases=['es', "edit-snipe", "esnipe"])
async def edit_snipe(ctx):
    channel = ctx.channel 

    with open(esni, "r") as bd:
        data = json.load(bd)

    try:
        cont = data[str(channel.id)]
        snipeEmbed = discord.Embed(title=f"Last Edited message in #{channel.name}", description = f"{cont['content']}\n\n[*__Message__*]({cont['link']})")

        snipeEmbed.set_footer(text=f"Message edited by {cont['author']}")
        await ctx.send(embed = snipeEmbed)
    except:
        await ctx.send(f"There are no edited messages in {channel.mention}")



@client.command()
@commands.is_owner()
async def reload(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.unload_extension(f"cogs.{filename[:-3]}")
            client.load_extension(f"cogs.{filename[:-3]}")

    await ctx.send("Extensions has been reloaded.")


@tasks.loop(seconds=10)
async def change_presence():
    await client.change_presence(activity=next(presence))


@tasks.loop(minutes=5)
async def del_snipe():

    data = {}
    data2 = {}

    with open(sni, "w") as bd:
        json.dump(data, bd) 

    with open(esni, "w") as bd2:
        json.dump(data2, bd2) 


keep_alive.keep_alive()
client.run(os.environ.get("TOKEN"))

# Rate Limit Fix: "kill 1"
