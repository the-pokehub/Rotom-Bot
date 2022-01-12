import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from replit import db
import difflib
import json
import string
import re


def get_data(find):

    dat = "data/pokedex.json Pokedex"
    dat = dat.split()
    
    with open(dat[0], "r") as load:
        data = json.load(load)

    with open("data/aliases.json", "r") as ala:
        lit = json.load(ala)

    find1 = find.translate(
        str.maketrans('', '', string.punctuation))

    find1 = find1.replace(" ", "")

    if find1 in data[dat[1]]:
        return find1

    if find1 in lit[dat[1]]:
        mod = lit[dat[1]][find1]
        return mod

    match = difflib.get_close_matches(find1, data[dat[1]], 1)

    best = None

    if match:
        best = match[0]

    if best:
        return best

    return None


def validate(user):
    try:
        r = requests.get(f"https://pokemonshowdown.com/users/{user}")

    except:
        return False

    soup = BeautifulSoup(r.content, features="html5lib")

    try:
        a = soup.find_all("div")[4]
    except:
        return False

    b = a.find("p").get_text()

    if "(Unregistered)" in b:
        return False
    else:
        return True


def evalu(url):

    r = requests.get(f"{url}.json")

    soup = BeautifulSoup(r.content, features="html5lib")

    a = soup.find("body")

    js = eval(a.get_text().replace("null", "None"))
    got = js["log"]

    rawTm = got.split("|clearpoke\n")[1]
    rawTm = rawTm.split("|teampreview\n")[0]

    rm = ["|", "poke", "item", ", F", ", M"]
    for i in rm:
        rawTm = rawTm.replace(i, "")

    p1 = []
    p2 = []

    tm = rawTm.split("\n")

    for i in tm:
        if "p1" in i:
            i = i.replace("p1", "")
            p1.append(get_data(i.lower()))
        elif "p2" in i:
            i = i.replace("p2", "")
            p2.append(get_data(i.lower()))

    pl1 = js["p1id"].lower()
    pl2 = js["p2id"].lower()

    team = {pl1: p1, pl2: p2}

    got = got.split("|win|")
    got = got[1].split("\n")
    winner = got[0].translate(str.maketrans('', '', string.punctuation)).lower().replace(" ", "")

    return team, winner


def won(replay):

    if "replay.pokemonshowdown.com" not in replay:
        return

    url = re.search("(?P<url>https?://[^\s]+)", replay).group("url")

    rep = evalu(url)

    if not rep:
        return None

    team = rep[0]
    winner = rep[1]

    tmlst = list(team.keys())
    pl1 = tmlst[0]
    pl2 = tmlst[1]
    # p1 = team[pl1]
    # p2 = team[pl2]

    # register = db["register"]
    sdid = db["sdid"]

    try:
        mem1 = sdid[pl1]
    except:
        return "id", pl1

    try:
        mem2 = sdid[pl2]
    except:
        return "id", pl2

    # pool1 = register[mem1]["pool"]
    # pool2 = register[mem2]["pool"]

    # for i in p1:
    #     if i not in pool1:
    #         return "pool", {i: mem1}

    # for i in p2:
    #     if i not in pool2:
    #         return "pool", {i, mem2}
    
    if winner == pl1:
        return mem1, mem2
    elif winner == pl2:
        return mem2, mem1
    else:
        print("error")


class Tour(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.client.user:
            return

        if message.channel.id == 798035217423925319 or message.channel.id == 847509607185383494 or message.channel.id == 770846450896470049:

            msg = won(message.content)
            if msg:
                if msg[0] == "pool":

                    await message.add_reaction("❌")
                    mon = list(msg[1].keys())[0]
                    mem = await self.client.fetch_user(int(msg[1][mon]))
                    await message.reply(f"{mon} not in pool of {mem}")

                elif msg[0] == "id":

                    await message.add_reaction("❌")
                    await message.reply(f"PSD ID {msg[1]} is not registered.")

                else:
                    await message.add_reaction("✅")
                    channel = self.client.get_channel(898820997501820958)
                    mem1 = await self.client.fetch_user(int(msg[0]))
                    mem2 = await self.client.fetch_user(int(msg[1]))

                    await channel.send(f"{mem1.mention} won against {mem2.mention}.")


        if message.channel.id == 861952254072586240 or message.channel.id == 847509607185383494 or message.channel.id == 770846450896470049:

            author = message.author
            if message.mentions:

                mentions = message.mentions
                if author not in mentions:
                    return

                msg = message.content

                for i in mentions:
                    msg = msg.replace(f"<@!{str(i.id)}>", "")
                    msg = msg.replace(f"<@{str(i.id)}>", "")

                id = validate(msg.replace(" ", ""))
                # print(msg)

                if not id:
                    await message.reply("You need a registered PSD ID to register.")

                else:

                    members = db["register"]
                    members[str(author.id)] = msg.replace(" ", "")
                    db["register"] =  members
                    await message.reply("You have been successfully registered.")
            

    # @commands.command(aliases=["r"])
    # async def register(self, ctx, *, text):

    #     if ctx.channel.id != 861952254072586240 and ctx.channel.id != 847509607185383494:
    #         return

    #     channel = self.client.get_channel(847509607185383494)
    #     send = ctx.message.content

    #     await ctx.message.delete()

    #     text = text.replace(" ", "").lower().split(",")
    #     sdid = text[0]
    #     char = text[1]
    #     pool = text[2:]

    #     members = db["register"]
    #     if str(ctx.author.id) in members:
    #         return await ctx.send("You have already registered.")

    #     val = validate(sdid)

    #     if not val:
    #         return await ctx.send("You need a registered PSD ID to register.")
    #     # else:
    #     #     await ctx.send("ID verificaion sucessfull.")

    #     with open("characters.json", "r") as cdata:
    #         data = json.load(cdata)

    #     if char not in data:
    #         return await ctx.send("The character you choosed is either not valid or misspelled.")

    #     mons = data[char]["mons"].split(", ")

    #     fpool = set()
    #     for i in pool:
    #         got = get_data(i)

    #         if not got:
    #             if i != "":
    #                 return await ctx.send(f"{i} is not valid.")

    #         fpool.add(got)

    #     tier = data[char]["tier"]

    #     if tier == "S":
    #         tot = 6
    #     elif tier == "A":
    #         tot = 8
    #     elif tier == "B":
    #         tot = 10
    #     else:
    #         tot = 12

    #     valid = set()

    #     for i in mons:
    #         for j in fpool:
    #             if i == j:
    #                 valid.add(j)

    #     not_valid = list(set(fpool).difference(valid))
    #     wrong = ", ".join(not_valid)

    #     if len(fpool) != len(valid):
    #         return await ctx.send(
    #             f"{wrong} is/are not in the pool of {char.capitalize()}."
    #         )
        
    #     if 6 > len(valid):
    #         return await ctx.send("You need pool of atleast 6.")

    #     if len(valid) > tot:
    #         return await ctx.send(f"You cannot have more than {tot} Pokémon in a {tier} tier Character.")
        
    #     members[str(ctx.author.id)] = {"pool": list(valid), "character": char, "sdid": sdid}

    #     db["register"] = members
    #     getcr = db["characters"]
    #     if char in getcr:
    #         if getcr[char] == 3:
    #             return await ctx.send("That character has already got it's maximum participants, choose another character.")
    #         else:
    #             mem = getcr[char]
    #             getcr[char] = mem + 1
    #     else:
    #         getcr[char] = 1
    #     db["characters"] = getcr

    #     await ctx.send("Your details have been saved.")
    #     await channel.send(send)

    # @commands.command()
    # async def replace(self, ctx, *, text):

    #     if ctx.channel.id != 861952254072586240 and ctx.channel.id != 847509607185383494:
    #         return

    #     channel = self.client.get_channel(847509607185383494)
    #     send = ctx.message.content

    #     await ctx.message.delete()

    #     text = text.replace(" ", "").lower().split(",")
    #     sdid = text[0]
    #     char = text[1]
    #     pool = text[2:]

    #     members = db["register"]
    #     if str(ctx.author.id) not in members:
    #         return await ctx.send("You have not registered yet.")

    #     val = validate(sdid)

    #     precr = members[str(ctx.author.id)]["character"]


    #     if not val:
    #         return await ctx.send("You need a registered PSD ID to register.")
    #     # else:
    #     #     await ctx.send("ID verificaion sucessfull.")

    #     with open("characters.json", "r") as cdata:
    #         data = json.load(cdata)

    #     if char not in data:
    #         return await ctx.send("The character you choosed is either not valid or misspelled.")

    #     mons = data[char]["mons"].split(", ")

    #     fpool = set()
    #     for i in pool:
    #         got = get_data(i)

    #         if not got:
    #             if i != "":
    #                 return await ctx.send(f"{i} is not valid.")

    #         fpool.add(got)

    #     tier = data[char]["tier"]

    #     if tier == "S":
    #         tot = 6
    #     elif tier == "A":
    #         tot = 8
    #     elif tier == "B":
    #         tot = 10
    #     else:
    #         tot = 12

    #     valid = set()

    #     for i in mons:
    #         for j in fpool:
    #             if i == j:
    #                 valid.add(j)

    #     not_valid = list(set(fpool).difference(valid))
    #     wrong = ", ".join(not_valid)

    #     if len(fpool) != len(valid):
    #         return await ctx.send(
    #             f"{wrong} is/are not in the pool of {char.capitalize()}."
    #         )
        
    #     if 6 > len(valid):
    #         return await ctx.send("You need pool of atleast 6.")

    #     if len(valid) > tot:
    #         return await ctx.send(f"You cannot have more than {tot} Pokémon in a {tier} tier Character.")
        
    #     members[str(ctx.author.id)] = {"pool": list(valid), "character": char, "sdid": sdid}

    #     db["register"] = members
    #     getcr = db["characters"]
    #     if char in getcr:
    #         if getcr[char] == 3:
    #             return await ctx.send("That character has already got it's maximum participants, choose another character.")
    #         else:
    #             mem = getcr[char]
    #             getcr[char] = mem + 1
    #     else:
    #         getcr[char] = 1

    #     _1 = getcr[precr]
    #     getcr[precr] = _1 - 1

    #     db["characters"] = getcr

    #     await ctx.send("Your details have been saved.")
    #     await channel.send(send)


    # @commands.command(aliases=["pl", "pokemon"])
    # async def pool(self, ctx, *, member: discord.Member = None):

    #     if not member:
    #         member = ctx.author

    #     data = db["register"]

    #     if str(member.id) not in data:
    #         return await ctx.send(f"{member} is not registered.")

    #     registered = data[str(member.id)]["pool"]
    #     registered_str = ""

    #     with open("data/pokedex.json", "r") as load:
    #         dex = json.load(load)

    #     for i in registered:
    #         mon = dex["Pokedex"][i]["name"]
    #         registered_str += mon + "\n"

    #     em = discord.Embed(title=f"{member}'s Pool:",
    #                         colour=discord.Colour.orange())   

    #     em.set_thumbnail(url=member.avatar_url)
    #     em.add_field(name="Character:", value=data[str(member.id)]["character"].capitalize())
    #     em.add_field(name="PSD ID:", value=data[str(member.id)]["sdid"])
    #     em.add_field(name="Pool:", value=registered_str, inline=False)
        
    #     await ctx.send(embed=em)

    @commands.command()
    async def participants(self, ctx):
        register = db["register"]

        desc = ""
        count = 0

        for i in register:
            try:
                mem = await ctx.guild.fetch_member(int(i))
                desc += f"{mem.mention}\n"
                # desc += f"{mem.mention} - {register[i]['character'].capitalize()}\n"
                count += 1
            except:
                pass

        em = discord.Embed(title="Ant Tour Participants:", description=desc, colour=discord.Colour.orange())

        em.add_field(name="Total Participants:", value=count)

        await ctx.send(embed=em)
        

    @commands.command()
    @commands.is_owner()
    async def formid(self, ctx):

        ids = {}
        register = db["register"]
        for i in register:
            sdid = register[i].translate(str.maketrans('', '', string.punctuation)).lower()
            sdid = sdid.replace(" ", "")
            register[i] = sdid
            ids[sdid] = i

        db['sdid'] = ids

        await ctx.send(ids)


def setup(client):
    client.add_cog(Tour(client))