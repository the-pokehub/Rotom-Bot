import discord
from discord.ext import commands, tasks
import os
import keep_alive
import json
from itertools import cycle
from better_profanity import profanity


with open("mod.json", "r") as mod_data:
    save = json.load(mod_data)


def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


prefix = get_prefix

current_title = str(save["current_league"])
intents = discord.Intents.all()

presence = cycle([
    discord.Activity(type=discord.ActivityType.listening, name=".help"),
    discord.Activity(type=discord.ActivityType.watching, name="Citra Pokéhub"),
    discord.Activity(type=discord.ActivityType.playing, name=current_title)
])

client = commands.Bot(
    command_prefix=prefix, intents=intents, case_insensitive=True)


@client.event
async def on_ready():
    change_presence.start()
    json_entry.start()

    print(f"Bot is Ready.\nLogged in as {client.user.name}\n---------------------")

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

    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send(
            "Use command in Server...\nhttps://discord.gg/n5zdSC6Ftb")
        return


    if message.channel.id == 775388498919948299:
        if "you just advanced to level 15!" in message.content:
            member_id = ''.join(filter(lambda i: i.isdigit(), message.content))

            mem = await message.guild.fetch_member(int(member_id[:-2]))            
            role = discord.utils.get(message.guild.roles, name="advanced-trainers")

            await mem.add_roles(role)


    if message.channel.id == 809594017947975690:
        if "I'm MEE6 the Discord Bot!" in message.content:
            await message.channel.send("Hello")
        

    # if ":gengar:" in message.content:
    #     emoji = "🪥"
    #     try:
    #         await message.add_reaction(emoji)
    #     except discord.errors.NotFound:
    #         pass

    # if ":hehe:" in message.content:
    #     emoji = "🪥"
    #     try:
    #         await message.add_reaction(emoji)
    #     except discord.errors.NotFound:
    #         pass
    
    # if ":sutta:" in message.content:
    #     # emoji = "🚭"
    #     try:
    #         # await message.add_reaction(emoji)
    #         await message.delete()
    #     except discord.errors.NotFound:
    #         pass

    # if ":pepe_smoke:" in message.content:
    #     # emoji = "🚭"
    #     try:
    #         # await message.add_reaction(emoji)
    #         await message.delete()
    #     except discord.errors.NotFound:
    #         pass

    # if "🚬" in message.content:
    #     # emoji = "🚭"
    #     try:
    #         # await message.add_reaction(emoji)
    #         await message.delete()
    #     except discord.errors.NotFound:
    #         pass

    # if ":sed:" in message.content:
    #     emoji = "🚰"
    #     try:
    #         await message.add_reaction(emoji)
    #     except discord.errors.NotFound:
    #         pass

    # if ":is:" in message.content:
    #     emoji = "♥"
    #     try:
    #         await message.add_reaction(emoji)
    #     except discord.errors.NotFound:
    #         pass

    # if message.author.id == 763666468222664744:
    #     emoji = "🐐"
    #     try:
    #         await message.add_reaction(emoji)
    #     except discord.errors.NotFound:
    #         pass
    
    # if message.channel.name == "💭opinions-and-requests":
    #     emoji1 = "<a:thumbs_up:796407963459780628>"
    #     emoji2 = "<a:thumbs_down:796407964033351800>"
    #     await message.add_reaction(emoji1)
    #     await message.add_reaction(emoji2)

    # if message.channel.name == "📝registration":
    #     channel = message.channel
    #     await channel.purge(limit=1)

    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "."

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_leave(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@client.command()
@commands.has_permissions(manage_guild=True)
async def change_prefix(ctx, new_prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[(str(ctx.guild.id))] = new_prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f"Server Prefix has been change to {new_prefix}")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send(f"{str(error).capitalize()}")


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


@tasks.loop(seconds=5)
async def json_entry():

    for filename in os.listdir():
        if filename.endswith(".json"):
            file = open(filename, "r")
            file.read()
            file.close()


keep_alive.keep_alive()
client.run(os.environ.get("TOKEN"))
