import difflib
import random
import json
import discord
from discord.ext import commands
import string


dex = "data/pokedex.json Pokedex"
ability = "data/abilities.json Abilities"
move = "data/moves.json Moves"
item = "data/items.json Items"
nature = "data/natures.json Natures"

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
        add  = f"No 1 {find} found did u mean {best.capitalize()}?"
        ret = data[dat[1]][best]
        return add, ret

    
    add = "No 1 Found"
    return add, ret


class PkDex(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    async def get_poke(self, ctx, poke):

        add, got = get_data(dex, poke)

        if poke:
            color = got['color']

            spID = got['name'].replace(" ", "")

            if "sprite" in got:
                SPRITE_URL = got["sprite"]
            else:
                SPRITE_URL = f"https://play.pokemonshowdown.com/sprites/ani/{spID.lower()}.gif"

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

            spID = got['name'].replace(" ", "")
            add = ""
            base_url = "https://play.pokemonshowdown.com/sprites/"
            end = ".png"
            afd = "no"
            gen = "no"
            final = ""

            if flags:
                flags = flags.lower()

            if got['tier'] == "CAP":
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

            elif flags is None:
                add += "ani"
                end = ".gif"           

            else:
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
                                    add += genData[flag]
                                if flag.isnumeric() and 5 < int(flag) < 9:
                                    add += ""
                                gen ="yes"
                        
                        if gen == "yes":
                            for flag in flags:
                                if flag == "back":
                                    add += "-back"

                                if flag == "shiny":
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
                        print(flags)
                        if flags.isnumeric() and int(flags) < 6:
                            add += genData[flags]
                            end = ".png"
                        if flags.isnumeric() and 5 < int(flags) < 9:
                            add += "ani"
                            end = ".gif"

                    else:
                        add += "ani"
                        if flags == "back":
                            add += "-back"
                            end = ".gif"

                        if flags == "shiny":
                            add += "-shiny"
                            end = ".gif"

            order = ["ani", "afd", "gen", "-back", "-shiny"]

            for names in order:
                if names in add:
                    if names == "gen":
                        gen_num = ""
                        for num in add:
                            if num.isnumeric():
                                gen_num = num
                                break
                        if int(gen_num) < 9:
                            final += f"gen{gen_num}"
                    else:
                        final += names

            url = f"{base_url}{final}/{spID.lower()}{end}"

            return url
        
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


def setup(client):
    client.add_cog(PkDex(client))
