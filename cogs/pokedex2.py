"""
learnset, filter
TODO: coverage, calculator(opt), hiddenpower(opt)
"""

import json
import string
import difflib
from discord.ext import commands
from functools import reduce

Names = {
    "E": "egg",
    "D": "dream world",
    "S": "event",
    "L": "level up",
    "M": "TM, HM or TR",
    "T": "tutor",
    "X": "egg, traded back",
    "Y": " event, traded back",
    "V": "VC transfer"
}

learnset_dat = "data/learnsets.json"
ability_dat = "data/abilities.json Abilities"
move_dat = "data/moves.json Moves"
dex_dat = "data/pokedex.json Pokedex"


def get_data(dat, find):

    dat = dat.split()

    with open(dat[0], "r") as load:
        data = json.load(load)

    with open("data/aliases.json", "r") as ala:
        lit = json.load(ala)

    find1 = find.translate(
        str.maketrans('', '', string.punctuation))

    if find1 in data[dat[1]]:
        return find1

    if find1 in lit[dat[1]]:
        mod = lit[dat[1]][find1]
        return mod

    match = difflib.get_close_matches(find1, data[dat[1]], 1)

    if match:
        return match[0]

    return None


def get_name(dat, find):

    dat = dat.split()
    with open(dat[0], "r") as load:
        data = json.load(load)

    if find in data[dat[1]]:
        return data[dat[1]][find]["name"]


def get_set(mon, move):

    title = ""

    with open("data/pokedex.json", "r") as load:
        data = json.load(load)

    with open("data/aliases.json", "r") as ala:
        lit = json.load(ala)

    find = mon.translate(
        str.maketrans('', '', string.punctuation))

    find = find.replace(" ", "")

    if find in data["Pokedex"]:
        ret = find

    if find in lit["Pokedex"]:
        mod = lit["Pokedex"][find]
        ret = mod

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

        with open("data/pokedex.json", "r") as load:
            data = json.load(load)

        with open(learnset_dat, "r") as d:
            data1 = json.load(d)

        if a in data["Pokedex"]:
            if "baseSpecies" in data["Pokedex"][a]:
                mon = data["Pokedex"][a]["baseSpecies"].lower()

                for m in data1["Learnsets"][mon]["learnset"]:
                    output += m.capitalize() + ", "

            else:
                if "learnset" in data1["Learnsets"][a]:
                    for m in data1["Learnsets"][a]["learnset"]:
                        output += m.capitalize() + ", "

        return output

    def mov_dat(a, b):

        with open(learnset_dat, "r") as d:
            data = json.load(d)

        ss = ""

        try:

            for i in data["Learnsets"][a]["learnset"][b]:
                gen = int(i[0])
                mtype = i[1]
                if mtype == "L":
                    lvl = i[2:]
                    ss += f"Gen{gen}:\n\t{Names[mtype]} ({lvl})\n"
                else:
                    ss += f"Gen{gen}:\n\t{Names[mtype]}\n"
        except KeyError:
            return "1 Cannot Learn 2"

        return ss

    def vgc22mov(a):

        with open(learnset_dat, "r") as d:
            data = json.load(d)

        sent = ""

        for i in data["Learnsets"][a]["learnset"]:
            for j in data["Learnsets"][a]["learnset"][i]:
                if j.startswith("8"):
                    sent += i.capitalize() + ", "
                    break

        return sent

    mn = get_name(dex_dat, ret)

    if move == "None":
        display = all_moves(ret)
        title = f"{mn}'s Learnset:"

    elif move.lower() == "vgc":
        title = f"{mn}'s VGC22 Learnset: "
        display = vgc22mov(ret)

    else:

        with open("data/moves.json", "r") as load:
            data = json.load(load)

        with open("data/aliases.json", "r") as ala:
            lit = json.load(ala)

        mov = move.translate(
            str.maketrans('', '', string.punctuation))

        mov = mov.replace(" ", "")

        if mov in data["Moves"]:
            ret1 = mov

        if find in lit["Moves"]:
            mod = lit["Moves"][find]
            ret = mod

        else:

            match1 = difflib.get_close_matches(mov, data["Moves"], 1)

            best1 = None

            if match1:
                best1 = match1[0]
            else:
                b = all_moves(ret)
                title = f"{mn}'s Learnset:"
                return title, b, f"No Move {move} found."

            if best1:
                ret1 = best1

        display = mov_dat(ret, ret1)

        mv = get_name(move_dat, ret1)

        if "Cannot Learn" in display:
            display = display.replace("1", mn)
            display = display.replace("2", mv)
            return None, None, display

        title = f"{mn} can learn {mv} in:"

    return title, display, None


stats = ["hp", "hitpoints", "atk", "attack", "def", "defense", "spa", "specialattack", "spd", "specialdefense", "spe", "speed"]

equal = ["move", "type", "ability"]

equal_var = equal + stats

stat_dict = {
    "hp": "hp",
    "hitpoints": "hp",
    "atk": "atk",
    "attack": "atk",
    "def": "def",
    "defense": "def",
    "spa": "spa",
    "specialattack": "spa",
    "spd": "spd",
    "specialdefense": "spd",
    "spe": "spe",
    "speed": "spe"
}


def filter(flags):

    args = {}
    found = []

    def process_args(arg):

        if "=" in arg:
            arg = arg.split("=")
            if arg[0] in equal_var:
                if arg[0] in args:
                    if arg[0] not in stats:
                        a = args[arg[0]]
                        a += ";" + arg[1]
                        args[arg[0]] = a
                else:
                    if arg[0] in stats:
                        get = stat_dict[arg[0]]
                        args[get] = arg[1]
                    else:
                        args[arg[0]] = arg[1]

        elif "<" in arg:
            arg = arg.split("<")
            if arg[0] in stats:
                get = stat_dict[arg[0]]
                check = arg[1]
                if check[0] == "=":
                    check.replace("=", "")
                arg[1] = check
                args[get] = arg[1] + "-"

        elif ">" in arg:
            arg = arg.split(">")
            if arg[0] in stats:
                get = stat_dict[arg[0]]
                check = arg[1]
                if check[0] == "=":
                    check.replace("=", "")
                arg[1] = check
                args[get] = arg[1] + "+"

    def modify():
        for i in args:
            if i == "move":
                check = args[i].split(";")
                for j in range(len(check)):
                    gg = get_data(move_dat, check[j])
                    if gg is not None:
                        check[j] = gg
                    else:
                        args[1] += " (Not Found)"
            if i == "ability":
                check = args[i].split(";")
                for j in range(len(check)):
                    gg = get_data(ability_dat, check[j])
                    if gg is not None:
                        check[j] = gg
                    else:
                        args[1] += " (Not Found)"

    def process(para, val):

        if para == "move":
            file = ["data/learnsets.json", "Learnsets"]
            with open("data/pokedex.json", "r") as bdata:
                data1 = json.load(bdata)
                data2 = data1["Pokedex"]
        else:
            file = ["data/pokedex.json", "Pokedex"]

        with open(file[0], "r") as bdata:
            opFile = json.load(bdata)

        data = opFile[file[1]]

        if para in stat_dict:
            ab = []
            if val[-1] == "+":
                for i in data:
                    if data[i]["baseStats"][para] >= int(val[:-1]):
                        if "tier" in data[i]:
                            if "CAP" not in data[i]["tier"]:
                                ab.append(data[i]["name"])
                        else:
                            ab.append(data[i]["name"])

            elif val[-1] == "-":
                for i in data:
                    if data[i]["baseStats"][para] <= int(val[:-1]):
                        if "tier" in data[i]:
                            if "CAP" not in data[i]["tier"]:
                                ab.append(data[i]["name"])
                        else:
                            ab.append(data[i]["name"])

            else:
                for i in data:
                    if data[i]["baseStats"][para] == int(val):
                        if "tier" in data[i]:
                            if "CAP" not in data[i]["tier"]:
                                ab.append(data[i]["name"])
                        else:
                            ab.append(data[i]["name"])

            found.append(ab)

        val = val.split(";")

        if para == "ability":
            ab = []
            for value in val:
                for i in data:
                    for j in data[i]["abilities"]:
                        check = data[i]["abilities"][j].lower()
                        check = check.replace(" ", "")
                        if check == value:
                            if "tier" in data[i]:
                                if "CAP" not in data[i]["tier"]:
                                    ab.append(data[i]["name"])
                            else:
                                ab.append(data[i]["name"])

                found.append(ab)
                ab = []

        if para == "type":
            ab = []
            for value in val:
                for i in data:
                    for j in data[i]["types"]:
                        if j.lower() == value:
                            if "tier" in data[i]:
                                if "CAP" not in data[i]["tier"]:
                                    ab.append(data[i]["name"])
                            else:
                                ab.append(data[i]["name"])

                found.append(ab)
                ab = []

        if para == "move":
            ab = []
            for value in val:
                for i in data:
                    if "learnset" in data[i]:
                        if value in data[i]["learnset"]:
                            if "tier" in data[i]:
                                if "CAP" not in data2[i]["tier"]:
                                    ab.append(data2[i]["name"])
                            else:
                                ab.append(data2[i]["name"])

                found.append(ab)
                ab = []

    if "," in flags:
        flags = flags.split(",")
        for i in flags:
            process_args(i)
    else:
        process_args(flags)

    # print(args)

    modify()

    for i in args:
        process(i, args[i])

    send = list(reduce(lambda i, j: i & j, (set(x) for x in found)))

    return send, args


class PkDex2(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="learnset", aliases=["learn"])
    async def learnset(self, ctx, mon, *, get: str = None):

        "Get learnset of a pokemon"

        if ctx.channel.id == 884745067607228456:
            return

        if get is None:
            get = "None"
        else:
            get = get.lower()

        get = get.replace(" ", "")

        title, des, add = get_set(mon.lower(), get)

        if title:

            des_l = des.split(", ")
            dm = "```" + title + "\n"
            dm_list = []
            flag = False
            for i in des_l:
                if i == "":
                    continue
                dm += i + ", "
                if len(dm) >= 1500:
                    dm += "```"
                    flag = True
                    dm_list.append(dm)
                    dm = "```"

            dm += "```"

            if flag:
                dm_list.append(dm)

                for i in dm_list:
                    try:
                        await ctx.author.send(i)

                    except Exception:
                        return await ctx.send("Looks like you have closed DM")

                return await ctx.send("I have send you response via DM.")

            else:

                if add:
                    send = add + dm
                    return await ctx.send(send)
                else:
                    return await ctx.send(dm)

        else:
            return await ctx.send(add)

    @commands.hybrid_command(name="filter")
    async def filter(
        self, ctx,
        get: str = "",
        # move: str = "",
        # ability: str = "",
        # type: str = "",
    ):

        if ctx.channel.id == 884745067607228456:
            return

        get = get.replace(" ", "")

        got, para = filter(get.lower())

        length = len(para)

        send = "```"

        for i in para:
            a = para[i]
            if a[-1] == "+":
                a = a.replace("+", "")
                send += f"\n{i.capitalize()} > {a}"
            elif a[-1] == "-":
                a = a.replace("-", "")
                send += f"\n{i.capitalize()} = {a}"
            else:
                send += f"\n{i.capitalize()} = {a.capitalize()}"

        send += "\n\n--------------------------------------------\n\n"

        if got != []:
            send += f"Pokemon that satisfies {length} Parameter(s):\n"

            dm_list = []
            flag = False
            for i in got:
                if i == "":
                    continue
                send += i + ", "
                if len(send) >= 1500:
                    send += "```"
                    flag = True
                    dm_list.append(send)
                    send = "```"

            send += "```"

            if flag:

                dm_list.append(send)

                for i in dm_list:
                    try:
                        await ctx.author.send(i)
                    except Exception:
                        return await ctx.send("Looks like you have closed DM")

                return await ctx.send("I have send you response via DM.")

            else:
                return await ctx.send(send)

        else:
            send = f"No Pokemon Satisfies these {length} Parameters."

        await ctx.send(send)

    @commands.hybrid_command(name="vgc")
    async def vgc(self, ctx, a):

        gg = get_data(dex_dat, a)

        with open(learnset_dat, "r") as d:
            data = json.load(d)

        sent = ""

        for i in data["Learnsets"][gg]["learnset"]:
            for j in data["Learnsets"][gg]["learnset"][i]:
                if j.startswith("8"):
                    sent += i.capitalize() + ", "
                    break

        if sent != "":

            await ctx.send(f"```Moves learn by {gg.capitalize()} for VGC22 are:\n{sent}  ```")

        else:

            await ctx.send(f"{gg.capitalize()} cannot be used in VGC22")


async def setup(client):
    await client.add_cog(PkDex2(client))
