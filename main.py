import discord
from discord.ext import commands, tasks
import os
import asyncio
import json
import datetime
from dotenv import load_dotenv

load_dotenv()

# def get_prefix(client, message):

#     if isinstance(message.channel, discord.channel.DMChannel):
#         return "."

#     guild = db["prefixes"]
#     ret = guild.get(str(message.guild.id), ".")

#     if str(message.guild.id) not in guild:
#         guild[str(message.guild.id)] = "."

#         db["prefixes"] = guild

#     return ret

# prefix = get_prefix
prefix = "."

intents = discord.Intents.all()

client = commands.Bot(command_prefix=prefix,
                      intents=intents,
                      case_insensitive=True)

unload = [
    "afk", "tour", "game", "logger", "owner"
]


@client.event
async def on_ready():
    del_snipe.start()

    print(
        f"Bot is Ready.\nLogged in as {client.user}\n---------------------"
    )

    client.remove_command("help")
    # db["grunt_timers"] = {}

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            if filename[:-3] in unload:
                print(f"{filename[:-3]} not loaded.")
                continue
            await client.load_extension(f"cogs.{filename[:-3]}")
            # print(f"{filename[:-3]} loaded.")

    version = discord.__version__.replace(" ", "")
    print("discord.py Version: v" + version)

    g = await client.fetch_guild(676777139776913408)

    invites = await g.invites()

    inv = {}

    for i in invites:
        inv[i.code] = i.uses

    # db["invites"] = inv
    # print("Invite data loaded!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # pfx = get_prefix(client, message).lower()
    pfx = "."

    if message.channel.id in [761502109459677185, 856187354536214578]:
        if message.author.id == 559426966151757824:
            await message.delete()

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

    if message.content.lower().startswith(pfx):
        message.content = message.content[:len(pfx)].lower(
        ) + message.content[len(pfx):]

    await client.process_commands(message)


# @client.event
# async def on_guild_join(guild):
#     prefixes = db["prefixes"]
#     prefixes[str(guild.id)] = "."
#     db["prefixes"] = prefixes

# @client.event
# async def on_guild_leave(guild):
#     prefixes = db["prefixes"]
#     del prefixes[str(guild.id)]
#     db["prefixes"] = prefixes


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
        except Exception:
            pass


@client.command()
async def reload(ctx):
    if ctx.author.id not in [549415697726439434, 154248794215546880]:
        return

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            if filename[:-3] in unload:
                await ctx.send(f"{filename[:-3]} not loaded.")
                continue
            await client.unload_extension(f"cogs.{filename[:-3]}")
            await client.load_extension(f"cogs.{filename[:-3]}")

    await ctx.send("Extensions has been reloaded.")


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
        "attachment": attach,
        "time": datetime.datetime.now(datetime.timezone.utc).timestamp()
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
        "link": before.jump_url,
        "time": datetime.datetime.now(datetime.timezone.utc).timestamp()
    }

    with open(esni, "w") as bd:
        json.dump(data, bd)


@client.command()
async def snipe(ctx):

    if ctx.channel.id == 861952254072586240:
        return

    channel = ctx.channel

    with open(sni, "r") as bd:
        data = json.load(bd)

    try:

        message = data[str(channel.id)]

        if "discord.gg" in message['content']:
            return await ctx.send("<:uhh:880305186827014195> ")

        if message['content'].count(":") > 11:
            return await ctx.send("<:uhh:880305186827014195> ")

        snipeEmbed = discord.Embed(
            title=f"Last Deleted message in #{channel.name}",
            description=f"{message['content']}")

        snipeEmbed.set_footer(text=f"Message sent by {message['author']}")

        if message['attachment']:
            snipeEmbed.set_image(url=message['attachment'])

        await ctx.send(embed=snipeEmbed)

    except Exception:
        await ctx.send(f"There are no deleted messages in {channel.mention}")


@client.command(aliases=['es', "edit-snipe", "esnipe"])
async def edit_snipe(ctx):
    channel = ctx.channel

    with open(esni, "r") as bd:
        data = json.load(bd)

    try:
        cont = data[str(channel.id)]
        snipeEmbed = discord.Embed(
            title=f"Last Edited message in #{channel.name}",
            description=f"{cont['content']}\n\n[*__Message__*]({cont['link']})"
        )

        snipeEmbed.set_footer(text=f"Message edited by {cont['author']}")
        await ctx.send(embed=snipeEmbed)
    except Exception:
        await ctx.send(f"There are no edited messages in {channel.mention}")


@tasks.loop(minutes=5)
async def del_snipe():

    datad = {}
    datad2 = {}

    with open(sni, "r") as bd:
        data = json.load(bd)

    with open(esni, "r") as bd2:
        data2 = json.load(bd2)

    for i in data:
        t1 = data[i]["time"]
        t2 = datetime.datetime.now(datetime.timezone.utc).timestamp()

        td = t2 - t1

        if td < 60:
            datad[i] = data[i]

    for i in data2:
        t1 = data2[i]["time"]
        t2 = datetime.datetime.now(datetime.timezone.utc).timestamp()

        td = t2 - t1

        if td < 60:
            datad[i] = data2[i]

    with open(sni, "w") as bd:
        json.dump(datad, bd)

    with open(esni, "w") as bd2:
        json.dump(datad2, bd2)


@client.command()
@commands.guild_only()
async def sync(ctx,
               guilds: commands.Greedy[discord.Object],
               spec=None) -> None:
    """
    .sync -> global sync
    .sync ~ -> sync current guild
    .sync * -> copies all global app commands to current guild and syncs
    .sync ^ -> clears all commands from the current guild target and syncs (removes guild commands)
    .sync id_1 id_2 -> syncs guilds with id 1 and 2
    """
    async with ctx.typing():
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


try:
    client.run(os.getenv("TOKEN"))
except discord.errors.HTTPException:
    pass
