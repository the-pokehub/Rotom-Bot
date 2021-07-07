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
from trivia import trivia
import random


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

profanity.load_censor_words_from_file("swear_words.txt", whitelist_words=["gayder"])

save = db["mod"]


def get_prefix(client, message):
    if not message.guild:
        return "."
    
    guild = db["guild"]
    try:
        ret = str(guild[str(message.guild.id)]["prefix"])
    except AttributeError:
        ret = "."
    
    return ret
    


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
    del_snipe.start()

    print(
        f"Bot is Ready.\nLogged in as {client.user.name}\n---------------------"
    )

    client.remove_command("help")

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

    version = discord.__version__.replace(" ", "")
    print("discord.py Version: v" + version)

    # with open("trivia.json", "r") as b:
    #     lb = json.load(b)
        
    # lb["770846450896470046"] = dict(sorted(lb["770846450896470046"].items(), key=lambda item: item[1]))

    # with open("trivia.json", "w") as b:
    #     json.dump(lb, b, indent=4)


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

        if message.guild.id != 676777139776913408:
            return

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
    prefixes = db["guild"]
    prefixes[str(guild.id)] = {}
    prefixes[str(guild.id)]["prefix"] = "."
    db["guild"] = prefixes


@client.event
async def on_guild_leave(guild):
    prefixes = db["guild"]
    del prefixes[str(guild.id)]
    db["prefixes"] = prefixes


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send('{}'.format(str(error)))

# @client.event
# async def on_raw_reaction_add(payload):

#     pass

snipe_message_author = {}
snipe_message_content = {}
 

@client.event
async def on_message_delete(message):

    global snipe_message_author
    global snipe_message_content

    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content


@client.command()
async def snipe(ctx):
    channel = ctx.channel 
    try:
        snipeEmbed = discord.Embed(title=f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
        snipeEmbed.set_footer(text=f"Deleted by {snipe_message_author[channel.id]}")
        await ctx.send(embed = snipeEmbed)
    except:
        await ctx.send(f"There are no deleted messages in #{channel.name}")


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


keep_alive.keep_alive()
client.run(os.environ.get("TOKEN"))
