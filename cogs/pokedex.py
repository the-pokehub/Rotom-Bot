"""
ability
data
dex
item
move
nature
sprite
weakness
"""


import difflib
import random
import json
import discord
from discord.ext import commands
import string
import requests

dex = "data/pokedex.json Pokedex"
ability = "data/abilities.json Abilities"
move = "data/moves.json Moves"
item = "data/items.json Items"
nature = "data/natures.json Natures"
weakness = "data/typechart.json"
all = "data/data.json"

colors = {
    "Green": discord.Color.green(),
    "Red": discord.Color.red(),
    "Black": discord.Color.darker_gray(),
    "Blue": discord.Color.blue(),
    "White": discord.Color.lighter_grey(),
    "Brown": discord.Color.dark_purple(),
    "Yellow": discord.Color.orange(),
    "Purple": discord.Color.purple(),
    "Pink": discord.Color.magenta(),
    "Gray": discord.Color.light_gray()
}

fields = {
    "num": "Number:",
    "baseSpecies": "Base Species:",
    "types": "Types:",
    "genderRatio": "Gender Ratio:",
    "baseStats": "Base Stats:",
    "abilities": "Abilities:",
    "heightm": "Height(in m):",
    "weightkg": "Weight(in kg)",
    "tier": "Tier:",
    "prevo": "Previous Evo:",
    "evos": "Next Evo:",
    "evoType": "Evo Type:",
    "evoCondition": "Evo Condition:",
    "evoLevel": "Evo Level:",
    "evoItem": "Evo Item:",
    "eggGroups": "Egg Groups:",
    "otherFormes": "Alt Forms:",
    "canGigantamax": "G-Max Move:",
    "requiredItem": "Alt Forme Item:",
    "requiredMove": "Required Move:"
}

m_fields = {
    "accuracy": "Accuracy:",
    "basePower": "Base Power:",
    "category": "Category:",
    "pp": "PP:",
    "priority": "Priority:",
    "isZ": "Z-Stone:",
    "type": "Type:",
    "contestType": "Contest Type:"
}

i_fields = {
    "itemUser": "Item User:",
    "num": "Number:",
    "fling": "Fling Power",
    "naturalGift": "Natural Gift:",
    "zMoveFrom": "Base Move:"
}

genData = {"1": 'gen1', "2": 'gen2', "3": 'gen3', "4": 'gen4', "5": 'gen5'}


def get_data(dat, find):

    ret = None
    add = None

    dat = dat.split()

    with open(dat[0], "r") as load:
        data = json.load(load)

    with open("data/aliases.json", "r") as ala:
        lit = json.load(ala)

    if find == "random":
        found = random.choice(list(data[dat[1]].keys()))
        add = "No 1 specified, I found a random 1 for you."
        ret = data[dat[1]][found]
        return add, ret

    find1 = find.translate(
        str.maketrans('', '', string.punctuation))

    find1 = find1.replace(" ", "")

    if find1 in data[dat[1]]:
        ret = data[dat[1]][find1]
        return add, ret

    if find1 in lit[dat[1]]:
        mod = lit[dat[1]][find1]
        ret = data[dat[1]][mod]
        # add = f"No 1 {find} found did u mean {ret['name'].capitalize()}?"
        return add, ret

    match = difflib.get_close_matches(find1, data[dat[1]], 1)

    best = None

    if match:
        best = match[0]

    if best:
        ret = data[dat[1]][best]
        add = f"No 1 {find} found did u mean {ret['name'].capitalize()}?"
        return add, ret

    add = "No 1 Found"
    return add, ret


class PkDex(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def weak(self, ctx, type1, type2):

        with open(weakness, "r") as w:
            data = json.load(w)

        _000 = ""
        _025 = ""
        _050 = ""
        _100 = ""
        _200 = ""
        _400 = ""

        if type1.capitalize() not in data["TypeChart"]:
            add, got = get_data(dex, type1)
            if got:
                types = got["types"]
                title = got["name"] + " " + str(got["types"])
                color = colors[got['color']]
            else:
                return discord.Embed(title=add)

        else:
            if type2 != "None":
                types = [type1.capitalize(), type2.capitalize()]
            else:
                types = [type1.capitalize()]

            title = types
            x = random.choice(list(colors.keys()))
            color = colors[x]

        if len(types) > 1:

            a = data["TypeChart"][types[0]]["damageTaken"]
            b = data["TypeChart"][types[1]]["damageTaken"]

            for i in a:
                if i in b:

                    effective = float(a[i]) * float(b[i])

                    if effective == 0:
                        _000 += i + ", "

                    elif effective == 0.25:
                        _025 += i + ", "

                    elif effective == 0.5:
                        _050 += i + ", "

                    elif effective == 1.0:
                        _100 += i + ", "

                    elif effective == 2.0:
                        _200 += i + ", "

                    elif effective == 4.0:
                        _400 = i + ", "

        else:
            a = data["TypeChart"][types[0]]["damageTaken"]
            for i in a:
                effective = a[i]

                if effective == 0:
                    _000 += i + ", "

                elif effective == 0.25:
                    _025 += i + ", "

                elif effective == 0.5:
                    _050 += i + ", "

                elif effective == 1.0:
                    _100 += i + ", "

                elif effective == 2.0:
                    _200 += i + ", "

                elif effective == 4.0:
                    _400 = i + ", "

        form = f"x0.00: {_000}\nx0.25: {_025}\nx0.50: {_050}\nx1.00: {_100}\nx2.00: {_200}\nx4.00: {_400}"

        em = discord.Embed(
            title=title,
            description=form,
            colour=color)

        return em

    def get_spid(self, mon: dict):

        spe = mon["name"].replace(" ", "")

        spID = spe.replace("’", "").lower()

        if spID == "darmanitan-galar-zen":
            spID = "darmanitan-galarzen"

        if "o-o" in spID:
            if spID != "kommo-o-totem":
                spID = spID.replace("o-o", "oo")

        if spID.endswith("-star"):
            spID = spID.replace("-star", "star")

        if "striped" in spID:
            spID = spID.replace("-striped", "striped")

        if "pom-pom" in spID:
            spID = spID.replace("pom-pom", "pompom")

        if "dusk-mane" in spID:
            spID = spID.replace("-mane", "mane")

        if "dawn-wing" in spID:
            spID = spID.replace("-wing", "wing")

        if "low-key" in spID:
            if "gmax" in spID:
                spID = spID.replace("low-key", "")
            else:
                spID = spID.replace("low-key", "lowkey")

        if "urshifu" in spID:
            if "gmax" in spID:
                spID = spID.replace("-gmax", "")

            if "rapid" in spID:
                spID = spID.replace("-strike", "strike")

        if "mega-x" in spID:
            spID = spID.replace("mega-x", "megax")

        if "mega-y" in spID:
            spID = spID.replace("mega-y", "megay")

        return spID

    async def get_poke(self, ctx, poke):
        add, got = get_data(dex, poke)

        if poke:
            color = got.get('color', 'default_color')  # Provide a default color if missing

            spID = self.get_spid(got)

            SPRITE_URL = got.get("sprite", f"https://play.pokemonshowdown.com/sprites/ani/{spID}.gif")

            em = discord.Embed(
                title=got.get('name', 'Unknown'),
                colour=colors.get(color, discord.Color.default())  # Provide a default color if missing
            )

            for field in fields:
                if field in got:
                    if isinstance(got[field], list):
                        val = "\n".join(got[field])
                        em.add_field(name=fields[field], value=val)
                    elif isinstance(got[field], dict):
                        if field == "genderRatio":
                            val = "\n".join([f"**{k.upper()}** - {float(v) * 100:.1f}%" for k, v in got[field].items()])
                        else:
                            val = "\n".join([f"**{k.upper()}** - {v}" for k, v in got[field].items()])
                        em.add_field(name=fields[field], value=val)
                    else:
                        em.add_field(name=fields[field], value=got[field])

            em.set_thumbnail(url=SPRITE_URL)

            if add:
                await ctx.send(add.replace("1", "Pokemon"), embed=em)
            else:
                await ctx.send(embed=em)
        else:
            await ctx.send(add.replace("1", "Pokemon"))


    async def get_ab(self, ctx, abi):

        add, got = get_data(ability, abi)

        if got:

            em = discord.Embed(
                title=got['name'],
                description=got['desc']
            )

            em.add_field(name="Rating:", value=got['rating'])

            em.add_field(name="Number:", value=got['num'])

            if add:
                await ctx.send(add.replace("1", "Ability"), embed=em)

            else:
                await ctx.send(embed=em)
        else:
            await ctx.send(add.replace("1", "Ability"))

    async def get_move(self, ctx, mov):

        add, got = get_data(move, mov)

        if got:

            em = discord.Embed(
                title=got['name'],
                description=got['desc']
            )

            for field in m_fields:
                if field in got:

                    em.add_field(name=m_fields[field], value=got[field])

            if add:
                await ctx.send(add.replace("1", "Move"), embed=em)
            else:
                await ctx.send(embed=em)
        else:
            await ctx.send(add.replace("1", "Move"))

    async def get_item(self, ctx, itm):

        add, got = get_data(item, itm)

        if got:

            em = discord.Embed(
                title=got['name'],
                description=got['desc']
            )

            for field in i_fields:
                if field in got:

                    if isinstance(got, list):
                        val = ""
                        for i in got[field]:
                            val += f"{i}\n"
                            em.add_field(name=i_fields[field], value=val)

                    elif isinstance(got, list):

                        k = list(got[field].keys())
                        v = list(got[field].values())

                        val = ""

                        for i in range(len(k)):
                            val += f"**{k[i].upper()}** - {v[i]}\n"
                        em.add_field(name=i_fields[field], value=val)

                    else:
                        em.add_field(name=i_fields[field], value=got[field])

            if add:
                await ctx.send(add.replace("1", "Item"), embed=em)

            else:
                await ctx.send(embed=em)
        else:
            await ctx.send(add.replace("1", "Item"))

    async def get_na(self, ctx, nat):

        add, got = get_data(nature, nat)

        if add:
            add = add.replace("1", "Nature")

        if got:

            if "plus" in got or "minus" in got:
                send = f"```{got['name']}:          +{got['plus']}          -{got['minus']}```"
            else:
                send = f"```{got['name']}\nNoob Stat```"

            if add:
                await ctx.send(f"{add}\n{send}")
            else:
                await ctx.send(send)
        else:
            await ctx.send(add)

    def get_sprite(self, mon, flags=None):

        add, got = get_data(dex, mon)

        if got:

            if "forme" in got:
                if "Hisui" in got["forme"]:
                    return "Sprites are not updated for Hisuian Pokémons."

            hisui = ["Wyrdeer", "Kleavor", "Ursaluna", "Basculegion", "Sneasler", "Overqwil", "Enamorus", "Enamorus-Therian"]

            if got["name"] in hisui:
                return "Sprites are not updated for Hisuian Pokémons."

            if "sprite" in got:
                url = got["sprite"]
                return url

            add = ""
            end = ".png"
            afd = "no"
            gen = "no"
            flagGen = ""
            base_url = "https://play.pokemonshowdown.com/sprites/"

            spID = self.get_spid(got)

            def formUrl(ending, adding):

                order = ["ani", "afd", "gen", "-back", "-shiny"]
                final = ""

                for names in order:
                    if names in adding:
                        if names == "gen":
                            gen_num = ""
                            for num in adding:
                                if num.isnumeric():
                                    gen_num = num
                                    break
                            if int(gen_num) < 9:
                                final += f"gen{gen_num}"
                        else:
                            final += names

                url = f"{base_url}{final}/{spID}{ending}"

                response = requests.get(url)

                if response.status_code == 404:
                    return None
                else:
                    return url

            try:
                if got['tier'] == "CAP":
                    check = True
                else:
                    check = False
            except KeyError:
                check = False

            if check:
                add += "gen5"
                end = ".png"
                if flags is not None:
                    if "gen" in flags:
                        gen_num = ""
                        for num in flags:
                            if num.isnumeric():
                                gen_num = num
                                break
                        if int(gen_num) < 9:
                            r = f"gen{gen_num}"
                        else:
                            r = "gen"
                        flags = flags.replace(r, "")

            elif not flags:
                add += "ani"
                end = ".gif"

            else:
                flags = flags.lower()
                flags = flags.replace(" ", "")
                if "," in flags:
                    flags = flags.split(",")

                    for flag in flags:
                        if flag == "afd":
                            add += "afd"
                            end = ".png"
                            afd = "yes"

                    if afd == "yes":
                        for flag in flags:
                            if flag == "back":
                                add += "-back"

                            elif flag == "shiny":
                                add += "-shiny"

                    else:
                        for flag in flags:
                            if "gen" in flag:
                                flag = flag.replace("gen", "")
                                if flag.isnumeric() and int(flag) < 6:
                                    flagGen = int(flag)
                                    add += genData[flag]
                                if flag.isnumeric() and 5 < int(flag) < 9:
                                    add += ""
                                gen = "yes"

                                valid = formUrl(end, add)
                                if valid is None:
                                    return f"{got['name'].capitalize()} does not existed in this Generation."

                        if gen == "yes":
                            for flag in flags:
                                if flag == "back":
                                    add += "-back"

                                if flag == "shiny":
                                    if flagGen == 1:
                                        add += ""
                                    add += "-shiny"

                        else:
                            add += "ani"
                            end = ".gif"
                            for flag in flags:
                                if flag == "back":
                                    add += "-back"

                                if flag == "shiny":
                                    add += "-shiny"

                else:
                    if flags == "afd":
                        add += "afd"
                        end = ".png"

                    elif "gen" in flags:
                        flags = flags.replace("gen", "")
                        if flags.isnumeric() and int(flags) < 6:
                            add += genData[flags]
                            end = ".png"
                        if flags.isnumeric() and 5 < int(flags) < 9:
                            add += "ani"
                            end = ".gif"

                        valid = formUrl(end, add)
                        if valid is None:
                            return f"{got['name'].capitalize()} does not existed in Gen {flagGen}"

                    else:
                        add += "ani"
                        if flags == "back":
                            add += "-back"
                            end = ".gif"

                        if flags == "shiny":
                            add += "-shiny"
                            end = ".gif"

            valid = formUrl(end, add)
            if valid is not None:
                return valid
            else:
                ret = f"{base_url}ani/{spID}.gif"
                response = requests.get(ret)

                if response.status_code == 404:
                    print(ret)
                    return "The pokemon is of CAP with no sprite."
                else:
                    return url
                # return ret

        else:
            return f"No Pokemon {mon} found."

    async def data_cmd(self, ctx, find):

        with open(all, "r") as d:
            data = json.load(d)

        with open("data/aliases.json", "r") as ala:
            lit = json.load(ala)

        add = None
        ret = None
        best = None

        if find == "random":
            found = random.choice(list(data.keys()))
            add = "Nothing specified, I found a random data for you."
            ret = data[found]
            best = found

        else:
            find1 = find.translate(
                str.maketrans('', '', string.punctuation))

            find1 = find1.replace(" ", "")

            if find1 in data:
                ret = data[find1]
                best = find1

            elif find1 == "metronome":
                add = "Do you mean Metronome-Move or Metronome-Item?\nUse Metronome-M or Metronome-I"

            elif find1 in lit["Aliases"]:
                mod = lit["Aliases"][find1]
                ret = data[mod]
                best = mod

            else:
                match = difflib.get_close_matches(find1, data, 1)

                if match:
                    best = match[0]
                else:
                    add = "No data found"
                    # with open("data/aliases.json", "r") as ali:
                    #     lin = json.load(ali)

                    # if find1 in lin["Aliases"]:
                    #     pass

                if best:
                    ret = data[best]
                    if "-" in best:
                        best = best.split("-")
                        best = best[0]
                    add = f"No data {find} found did you mean {best.capitalize()}?"

        if add:
            await ctx.send(add)

        if ret:
            if ret == "Pokedex":
                await self.get_poke(ctx, best.lower())

            elif ret == "Abilities":
                await self.get_ab(ctx, best.lower())

            elif ret == "Moves":
                await self.get_move(ctx, best.lower())

            elif ret == "Items":
                await self.get_item(ctx, best.lower())

            elif ret == "Natures":
                await self.get_na(ctx, best.lower())

    @commands.hybrid_command(name="pokedex", aliases=["mon"])
    async def dex(self, ctx, *, poke: str = None):

        "Get information about a Pokemon"

        if ctx.channel.id == 884745067607228456:
            return

        if poke is None:
            poke = "random"

        await self.get_poke(ctx, poke.lower())

    @commands.hybrid_command(name="ability-dex")
    async def ability(self, ctx, *, abi: str = None):

        "Get information about an ability."

        if ctx.channel.id == 884745067607228456:
            return

        if abi is None:
            abi = "random"

        await self.get_ab(ctx, abi.lower())

    @commands.hybrid_command(name="move-dex")
    async def move(self, ctx, *, move: str = None):

        "Get information about a move."

        if ctx.channel.id == 884745067607228456:
            return

        if move is None:
            move = "random"

        await self.get_move(ctx, move.lower())

    @commands.hybrid_command(name="item-dex")
    async def item(self, ctx, *, item: str = None):

        "Get information about an Item."

        if ctx.channel.id == 884745067607228456:
            return

        if item is None:
            item = "random"

        await self.get_item(ctx, item.lower())

    @commands.hybrid_command(name="nature-dex")
    async def nature(self, ctx, *, natu: str = None):

        "Get information about a nature."

        if ctx.channel.id == 884745067607228456:
            return

        if natu is None:
            natu = "random"

        await self.get_na(ctx, natu.lower())

    @commands.hybrid_command(name="sprite")
    async def sprite(self, ctx, pokemon, *, flags=None):

        "Get the sprite of the pokemon."

        if ctx.channel.id == 884745067607228456:
            return

        sp = self.get_sprite(pokemon.lower(), flags)

        await ctx.send(sp)

    @commands.hybrid_command(name="weakness", aliases=["weak"])
    async def weakness(self, ctx, type1, type2=None):

        "Find weakness about a pokemon or type."

        if ctx.channel.id == 884745067607228456:
            return

        if type2 is None:
            p = await self.weak(ctx, type1, "None")
        else:
            p = await self.weak(ctx, type1, type2)

        await ctx.send(embed=p)

    @commands.hybrid_command(name="data", aliases=["dt"])
    async def data(self, ctx, *, get: str = None):

        "Get Information of a Pokémon, Ability, Move, Item, or Nature."

        if ctx.channel.id == 884745067607228456:
            return

        if get is None:
            get = "random"

        await self.data_cmd(ctx, get.lower())


async def setup(client):
    await client.add_cog(PkDex(client))
