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
from trivia import trivia
import random
import time
# import pymongo, dns

mongoKey = os.environ.get("mongoDB")

# mclient = pymongo.MongoClient(mongoKey)

async def ques():
    
    questions = await trivia.question(amount=1, quizType='multiple')

    q = questions[0]["question"]
    ans = questions[0]["incorrect_answers"]
    cor = questions[0]["correct_answer"]
    category = questions[0]["category"]
    difficulty = questions[0]["difficulty"]

    ans.append(cor)

    random.shuffle(ans)

    des = "Options:\n"
    num = ["a", "b", "c", "d"]
    for ele in range(len(ans)):
        des += f"{num[ele]}) {ans[ele]}\n"

    return q, ans, cor, category, difficulty, des  


save = db["mod"]


def get_prefix(client, message):

    time.sleep(0.01)

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
    discord.Activity(type=discord.ActivityType.watching, name="Citra Pokéhub")
])

client = commands.Bot(command_prefix=prefix,
                    intents=intents,
                    case_insensitive=True)


dbs = ['league_prof7', 'gen7', 'hall_of_fame', 'league_prof6', 'gen6', 'mod']

@client.event
async def on_ready():
    change_presence.start()
    del_snipe.start()
    del_esnipe.start()

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

        if message.guild.id == 676777139776913408:

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
        await ctx.send('{}'.format(str(error)))


snipe_message_author = {}
snipe_message_content = {}
esnipe_message_author = {}
esnipe_message_content = {}
esnipe_message_link = {}



@client.event
async def on_message_delete(message):

    global snipe_message_author
    global snipe_message_content

    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content

@client.event
async def on_message_edit(before, after):

    global esnipe_message_author
    global esnipe_message_content
    global esnipe_message_link

    esnipe_message_author[before.channel.id] = before.author
    esnipe_message_content[before.channel.id] = before.content
    esnipe_message_link[before.channel.id] = before.jump_url



@client.command()
async def snipe(ctx):
    channel = ctx.channel

    try:

        message = snipe_message_content[channel.id]

        profanity_check_msg = message.translate(
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
            
        snipeEmbed = discord.Embed(title=f"Last Deleted message in #{channel.name}", description = f"{snipe_message_content[channel.id]}")

        snipeEmbed.set_footer(text=f"Message sent by {snipe_message_author[channel.id]}")
        await ctx.send(embed = snipeEmbed)
    except:
        await ctx.send(f"There are no deleted messages in {channel.mention}")


@client.command(aliases=['es', "edit-snipe", "esnipe"])
async def edit_snipe(ctx):
    channel = ctx.channel 
    try:
        cont = esnipe_message_content[channel.id]
        snipeEmbed = discord.Embed(title=f"Last Edited message in #{channel.name}", description = f"{cont}\n\n[*__Message__*]({esnipe_message_link[channel.id]})")

        snipeEmbed.set_footer(text=f"Message edited by {esnipe_message_author[channel.id]}")
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


@client.command(aliases=["trivia"])
@commands.cooldown(1, 20, commands.BucketType.user)
async def quiz(ctx):

    q, ans, cor, category, difficulty, des = await ques()
    
    em = discord.Embed(title=q, description=f"{des}")

    em.add_field(name="Category:", value=f"{category}", inline=True)
    em.add_field(name="Difficulty", value=f"{difficulty.capitalize()}", inline=True)

    em.set_author(name=f"Question for {ctx.author}",icon_url=ctx.author.avatar_url)

    time = ""

    if difficulty.lower() == "easy":
        time = 10
    elif difficulty.lower() == "medium":
        time = 15
    elif difficulty.lower() == "hard":
        time = 20

    em.set_footer(text=f"You have {time} seconds to answer the question.")

    msg = await ctx.send(embed=em)

    A = "🇦"
    B = "🇧"
    C = "🇨"
    D = "🇩"
    choose = ""

    await msg.add_reaction(A)
    await msg.add_reaction(B)
    await msg.add_reaction(C)
    await msg.add_reaction(D)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["🇦", "🇧", "🇨", "🇩"]

    # print(cor)

    try:
        reaction, user = await client.wait_for("reaction_add", check=check, timeout=time)

        if str(reaction.emoji) == "🇦":
            choose = ans[0]

        elif str(reaction.emoji) == "🇧":
            choose = ans[1]

        elif str(reaction.emoji) == "🇨":
            choose = ans[2]

        elif str(reaction.emoji) == "🇩":
            choose = ans[3]

    except asyncio.TimeoutError:
        await msg.clear_reactions()

        des = "Options:\n"
        num = ["a", "b", "c", "d"]
        for ele in range(len(ans)):
            if ans[ele] != cor:
                des += f"{num[ele]}) ~~{ans[ele]}~~\n"
            else:
                des += f"{num[ele]}) **{ans[ele]}**\n"

        em = discord.Embed(title=q, description=f"{des}", color=discord.Color.orange())

        em.add_field(name="Category:", value=f"{category}", inline=True)
        em.add_field(name="Difficulty", value=f"{difficulty.capitalize()}", inline=True)

        em.set_author(name=f"{ctx.author}, You didn't answered in time.",icon_url=ctx.author.avatar_url)

        await msg.edit(embed=em)
        
        return

    await msg.clear_reactions()

    if choose == cor:
        # await ctx.reply("Correct!")
        corr = True
    else:
        # await ctx.reply(f"The right answer was: {cor}")
        corr = False

    if corr:

        des = "Options:\n"
        num = ["a", "b", "c", "d"]
        for ele in range(len(ans)):
            if ans[ele] != cor:
                des += f"{num[ele]}) ~~{ans[ele]}~~\n"
            else:
                des += f"{num[ele]}) **{ans[ele]}**\n"

        em = discord.Embed(title=q, description=f"{des}", color=discord.Color.green())

        em.add_field(name="Category:", value=f"{category}", inline=True)
        em.add_field(name="Difficulty", value=f"{difficulty.capitalize()}", inline=True)

        em.set_author(name=f"{ctx.author}, You're Correct!",icon_url=ctx.author.avatar_url)

        await msg.edit(embed=em)

        lb = db["trivia"]
        
        # if str(ctx.guild.id) not in lb:
        #     lb[str(ctx.guild.id)] = {}

        if str(ctx.author.id) not in lb:
            lb[str(ctx.author.id)] = 1
        else:
            lb[str(ctx.author.id)] += 1

        lb = dict(sorted(lb.items(), key = lambda kv:kv[1], reverse = True))

        db["trivia"] = lb

    else:
        des = "Options:\n"
        num = ["a", "b", "c", "d"]
        for ele in range(len(ans)):
            if ans[ele] != cor:
                des += f"{num[ele]}) ~~{ans[ele]}~~\n"
            else:
                des += f"{num[ele]}) **{ans[ele]}**\n"

        em = discord.Embed(title=q, description=f"{des}", color=discord.Color.red())

        em.add_field(name="Category:", value=f"{category}", inline=True)
        em.add_field(name="Difficulty", value=f"{difficulty.capitalize()}", inline=True)

        em.set_author(name=f"{ctx.author}, That's Not Right.",icon_url=ctx.author.avatar_url)

        await msg.edit(embed=em)


@tasks.loop(seconds=10)
async def change_presence():
    await client.change_presence(activity=next(presence))


@tasks.loop(minutes=30)
async def del_snipe():

    global snipe_message_author
    global snipe_message_content

    snipe_message_author = {}
    snipe_message_content = {}

@tasks.loop(minutes=30)
async def del_esnipe():

    global esnipe_message_author
    global esnipe_message_content
    global esnipe_message_link

    esnipe_message_author = {}
    esnipe_message_content = {}
    esnipe_message_link = {}


keep_alive.keep_alive()
client.run(os.environ.get("TOKEN"))

# Rate Limit Fix: "kill 1"
