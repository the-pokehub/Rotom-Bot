import discord
from discord.ext import commands, tasks
import os
import keep_alive
from itertools import cycle
from replit import db
from better_profanity import profanity
import asyncio
import string
import datetime
import json

profanity.load_censor_words_from_file("swear_words.txt", whitelist_words=["gayder"])

save = db["mod"]



def get_prefix(client, message):
    prefixes = db["prefixes"]

    return str(prefixes[str(message.guild.id)])


prefix = get_prefix

current_title = str(save["current_league"])
intents = discord.Intents.all()

presence = cycle([
    discord.Activity(type=discord.ActivityType.listening, name=".help"),
    discord.Activity(type=discord.ActivityType.watching, name="Citra Pokéhub"),
    discord.Activity(type=discord.ActivityType.playing, name=current_title)
])

client = commands.Bot(command_prefix=prefix,
                      intents=intents,
                      case_insensitive=True)


@client.event
async def on_ready():
    change_presence.start()

    print(
        f"Bot is Ready.\nLogged in as {client.user.name}\n---------------------"
    )

    client.remove_command("help")

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

    version = discord.__version__.replace(" ", "")
    print("discord.py Version: v" + version)



@client.event
async def on_message(message):
    if message.author == client.user:
        return

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

        # if message.guild.id != 676777139776913408:
        #     return

        if not message.author.bot:

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

    nick_msg = profanity_check_msg.replace(" ", "")

    if "iamback" in nick_msg.lower() or "iamback" in replaceDoubleCharacters(nick_msg.lower()) or "imback" in nick_msg.lower() or "imback" in replaceDoubleCharacters(nick_msg.lower()):
        user = message.author
        if user != message.guild.owner:    
            await user.edit(nick="Back")

    if message.channel.id == 780981187317465119:
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

    # if message.channel.id == 818452656670375978:
    #     msg = message.content.lower()

    #     if "gen" in msg:

    #         gen6 = db["tour"]["gen6"]
    #         gen7 = db["tour"]["gen7"]

    #         n = msg.split("gen")

    #         if len(n) > 3:
    #             pass
    #         else:
    #             if "6" in n[1]:
    #                 gen6.append(message.author.mention)
    #             if "7" in n[1]:
    #                 gen7.append(message.author.mention)

    #             if len(n) == 3:
    #                 if "6" in n[2]:
    #                     gen6.append(message.author.mention)
    #                 if "7" in n[2]:
    #                     gen7.append(message.author.mention)

    #         db["tour"]["gen6"] = gen6
    #         db["tour"]["gen7"] = gen7

    # if message.author.id == 763666468222664744:
    #     emoji = "🐐"
    #     try:
    #         await message.add_reaction(emoji)
    #     except discord.errors.NotFound:
    #         pass

    # if message.channel.name == "💭opinions-and-requests":
    #     emoji1 = "<a:thumbs_up:796407963459780628>"
    #     emoji2 = "<a:thumbs_down:796407964033351800>"
    #     try:
    #         await message.add_reaction(emoji1)
    #         await message.add_reaction(emoji2)
    #     except discord.errors.NotFound:
    #         pass

    # try:
    #     if message.mentions[0] == client.user:
    #         prefixes = db["prefixes"]
    #         server_prefix = str(prefixes[str(message.guild.id)])
    #         await message.channel.send(f"My prefix for this server is `{server_prefix}`")
    # except IndexError:
    #     pass

    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    prefixes = db["prefixes"]
    prefixes[str(guild.id)] = "."
    db["prefixes"] = prefixes


@client.event
async def on_guild_leave(guild):
    prefixes = db["prefixes"]
    prefixes.pop(str(guild.id))
    db["prefixes"] = prefixes


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send('{}'.format(str(error)))


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


keep_alive.keep_alive()
client.run(os.environ.get("TOKEN"))
