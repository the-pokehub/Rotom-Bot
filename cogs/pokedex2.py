import json
import string
import difflib
import discord
from discord.ext import commands

Names = {
  "E": "egg",
  "D": "dream world",
  "S": "event",
  "L": "level up",
  "M": "TM, HM or TR",
  "T": "tutor",
  "X": "egg, traded back",
  "Y":" event, traded back",
  "V": "VC transfer"
}

learnset = "data/learnsets.json"

def get_set(mon, move):

    title = ""

    with open("data/pokedex.json", "r") as load:
        data = json.load(load)

    find = mon.translate(
        str.maketrans('', '', string.punctuation))

    find = find.replace(" ", "")

    if find in data["Pokedex"]:
        ret = find

    else:

        match = difflib.get_close_matches(find, data["Pokedex"], 1)

        best = None

        if match:
            best = match[0]
        else:
            return None, None, f"No Pokemon {mon} found."

        if best:
            ret = best


    def all_moves(a):
        output = ""

        with open(learnset, "r") as d:
            data = json.load(d)

        for m in data["Learnsets"][a]["learnset"]:
            output += m.capitalize() + ", "
        
        return output

    
    def mov_dat(a, b):

        with open(learnset, "r") as d:
            data = json.load(d)

        ss = ""

        for i in data["Learnsets"][a]["learnset"][b]:
            gen = int(i[0])
            mtype = i[1]
            if mtype == "L":
                lvl = i[2:]
                ss += f"Gen{gen}:\n\t{Names[mtype]} ({lvl})\n"
            else:
                ss += f"Gen{gen}:\n\t{Names[mtype]}\n"

        return ss


    if move == "None":
        display = all_moves(ret)
        title = f"{ret.capitalize()}'s Learnset:"

    else:
        with open("data/moves.json", "r") as load:
            data = json.load(load)

        mov = move.translate(
            str.maketrans('', '', string.punctuation))

        mov = mov.replace(" ", "")

        if mov in data["Moves"]:
            ret1 = mov

        else:

            match1 = difflib.get_close_matches(mov, data["Moves"], 1)

            best1 = None

            if match1:
                best1 = match1[0]
            else:
                b = all_moves(ret)
                title = f"{ret.capitalize()}'s Learnset:"
                return title, b, f"No Move {move} found."

            if best1:
                ret1 = best1

        display = mov_dat(ret, ret1)
        title = f"{ret.capitalize()} can learn {ret1.capitalize()} in:"

    return title, display, None


# while True:
#     user = input("Enter to search: ")
#     mon = user.lower()
#     move = input("Enter move: ")
#     move = move.lower()
#     if move == "":
#         move = "None"
#     print(get_set(mon, move))


class PkDex2(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["learn"])
    async def learnset(self, ctx, mon, get: str = None):

        if get is None:
            get = "None"
        else:
            get = get.lower()

        title, des, add = get_set(mon.lower(), get)
        
        if title:

            # if len(des) > 2000:
            des_l = des.split(", ")
            dm = "```" + title + "\n"
            dm_list = []
            l = False
            for i in des_l:
                if i == "":
                    continue
                dm += i + ", "
                if len(dm) >= 1970:
                    dm += "```"
                    l = True
                    dm_list.append(dm)
                    dm = "```"

            dm += "```"
            
            if l:
                await ctx.send("I have send you response via DM.")
                dm_list.append(dm)

                for i in dm_list:
                    await ctx.author.send(i)
                return

            else:
                # return await ctx.send(dm)

            # em = discord.Embed(title=title, description=des)

                if add:
                    send = add + dm
                    return await ctx.send(send)
                else:
                    return await ctx.send(dm)

        else:
            return await ctx.send(add)


def setup(client):
    client.add_cog(PkDex2(client))
