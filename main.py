import discord
from discord.ext import commands, tasks
import os
import keep_alive
import json
from itertools import cycle

with open("mod.json", "r") as mod_data:
    save = json.load(mod_data)

prefix = str(save["prefix"])

current_title = str(save["current_league"])
intents = discord.Intents.all()

presence = cycle([
    discord.Activity(type=discord.ActivityType.listening, name=".help | .h"),
    discord.Activity(type=discord.ActivityType.watching, name="Citra Pokéhub"),
    discord.Activity(type=discord.ActivityType.playing, name=current_title)
])

client = commands.Bot(command_prefix=prefix,
                      intents=intents,
                      case_insensitive=True)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send(
            "Use command in Server...\nhttps://discord.gg/n5zdSC6Ftb")
        return

    # if message.channel.name == "💭opinions-and-requests":
    #     emoji1 = "<a:thumbs_up:796407963459780628>"
    #     emoji2 = "<a:thumbs_down:796407964033351800>"
    #     await message.add_reaction(emoji1)
    #     await message.add_reaction(emoji2)

    # if message.channel.name == "📝challengers-registration":
    #     channel = message.channel
    #     await channel.purge(limit=1)

    await client.process_commands(message)


@client.event
async def on_ready():

    print(
        f"Bot is Ready.\nLogged in as {client.user.name}\n---------------------"
    )

    version = discord.__version__.replace(" ", "")
    print("discord.py Version: v" + version)

    client.remove_command("help")

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

    change_presence.start()
    json_entry.start()


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send(f"{str(error).capitalize()}")


@client.command()
async def reload(ctx):
    if ctx.author.id != 549415697726439434:
        await ctx.send(f"{ctx.author.mention} you cannot use this.")
        return

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
