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
    "type": "Type:"
}

i_fields = {
    "itemUser": "Item User:",
    "num": "Number:",
    "fling": "Fling Power",
    "naturalGift": "Natural Gift:",
    "zMoveFrom": "Base Move:"
}

genData = {"1":'gen1', "2":'gen2', "3":'gen3', "4":'gen4', "5":'gen5'}


def get_data(dat, find):

    ret = None
    add = None

    dat = dat.split()
    with open(dat[0], "r") as load:
        data = json.load(load)

    if find == "random":
        found = random.choice(list(data[dat[1]].keys()))
        add = "No 1 specified, I found a random 1 for you."
        ret = data[dat[1]][found]
        return add, ret

    find1 = find.translate(
        str.maketrans('', '', string.punctuation))

    find1 = find1.replace(" ", "")

    for get in data[dat[1]]:
        if get == find1:
            ret = data[dat[1]][get]
            return add, ret

    match = difflib.get_close_matches(find1, data[dat[1]], 1)

    best = None

    if match:
        best = match[0]


    if best:
        ret = data[dat[1]][best]
        add  = f"No 1 {find} found did u mean {ret['name'].capitalize()}?"
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

    
    async def get_poke(self, ctx, poke):

        add, got = get_data(dex, poke)

        if poke:
            color = got['color']

            spID = got['name'].replace(" ", "")
            spID = spID.replace("’", "")
            spID = spID.lower()
            if spID == "darmanitan-galar-zen":
                spID = "darmanitan-galarzen"

            if "sprite" in got:
                SPRITE_URL = got["sprite"]
            else:
                SPRITE_URL = f"https://play.pokemonshowdown.com/sprites/ani/{spID}.gif"

            em = discord.Embed(
            title=got['name'],
            # description=f"",
            colour=colors[color])

            for field in fields:
                if field in got:

                    if type(got[field]) == list:
                        val = ""
                        for i in got[field]:
                            val += f"{i}\n"
                        em.add_field(name=fields[field], value=val)
                        
                    elif type(got[field]) == dict:

                        k = list(got[field].keys())
                        v = list(got[field].values())

                        val = ""

                        if field == "genderRatio":
                            for i in range(len(k)):
                                val += f"**{k[i].upper()}** - {float(v[i])*100}%\n"

                            em.add_field(name=fields[field], value=val)
                        else:
                            for i in range(len(k)):
                                val += f"**{k[i].upper()}** - {v[i]}\n"
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

                    if type(got[field]) == list:
                        val = ""
                        for i in got[field]:
                            val += f"{i}\n"
                            em.add_field(name=i_fields[field], value=val)

                    elif type(got[field]) == dict:

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
            await ctx.send(add.replace("1", "Nature"))


    def get_sprite(self, mon, flags = None):

        add, got = get_data(dex, mon)

        if got:

            if "sprite" in got:
                url = got["sprite"]
                return url

            add = ""
            end = ".png"
            afd = "no"
            gen = "no"
            flagGen = ""
            base_url = "https://play.pokemonshowdown.com/sprites/"
            spiID = got['name'].replace(" ", "")
            spID = spiID.replace("’", "")
            spID = spID.lower()
            if spID == "darmanitan-galar-zen":
                spID = "darmanitan-galarzen"


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
                                gen ="yes"

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
                return ret
        
        else:
            return f"No Pokemon {mon} found."


    @commands.command()
    async def dex(self, ctx, *, poke: str = None):

        if poke is None:
            poke = "random"

        await self.get_poke(ctx, poke.lower())

    @commands.command()
    async def ability(self, ctx, *, abi: str = None):

        if abi is None:
            abi = "random"

        await self.get_ab(ctx, abi.lower())

    @commands.command()
    async def move(self, ctx, *, move: str = None):

        if move is None:
            move = "random"

        await self.get_move(ctx, move.lower())

    @commands.command()
    async def item(self, ctx, *, item: str = None):

        if item is None:
            item = "random"

        await self.get_item(ctx, item.lower())

    @commands.command()
    async def nature(self, ctx, *, natu: str = None):

        if natu is None:
            natu = "random"

        await self.get_na(ctx, natu.lower())

    @commands.command()
    async def sprite(self, ctx, pokemon, *, flags = None):

        sp = self.get_sprite(pokemon.lower(), flags)
        
        await ctx.send(sp)

    @commands.command(aliases=["weak"])
    async def weakness(self, ctx, type1, type2 = None):
        if type2 is None:
            p = await self.weak(ctx, type1, "None")
        else:
            p = await self.weak(ctx, type1, type2)
        
        await ctx.send(embed=p)


def setup(client):
    client.add_cog(PkDex(client))
