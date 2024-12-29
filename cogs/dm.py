import discord as discord
from discord.ext import commands
from PIL import Image
from io import BytesIO


def mkDict(name1, name2):

    filler = "loves"

    d = {}

    for i in name1.lower():

        count = 0

        for j in name1.lower():
            if i == j:
                count += 1
        for k in name2.lower():
            if i == k:
                count += 1
        for n in filler:
            if i == n:
                count += 1

        d[i] = count

    for i in filler:

        if i in d:
            continue

        count = 0

        for j in name1.lower():
            if i == j:
                count += 1
        for k in name2.lower():
            if i == k:
                count += 1
        for n in filler:
            if i == n:
                count += 1

        d[i] = count

    for i in name2.lower():

        if i in d:
            continue

        count = 0

        for j in name1.lower():
            if i == j:
                count += 1
        for k in name2.lower():
            if i == k:
                count += 1
        for n in filler:
            if i == n:
                count += 1

        d[i] = count

    ret = ""

    for i in d:
        ret += str(d[i])

    # return d
    # print(ret)
    return ret


def make(got, half, length):

    half1 = []
    half2 = []
    mid = 0

    if length % 2 == 0:
        for i in got[:half]:
            half1.append(int(i))

        for j in got[half:]:
            half2.append(int(j))

    else:
        for i in got[:half]:
            half1.append(int(i))

        for j in got[half + 1:]:
            half2.append(int(j))

        mid: int = int(got[half])

    return half1, half2[::-1], mid


def calc(name1, name2):

    got = mkDict(name1, name2)

    l: int = len(got)
    half = int(l / 2)

    half1, half2, mid = make(got, half, l)
    new: str = ""

    for i in range(len(half1)):
        new += str(half1[i] + half2[i])

    if mid != 0:
        new += str(mid)

    newL: int = len(new)
    newH = int(newL / 2)

    def rec(_string, _half, _length):

        nH1, nH2, nM = make(_string, _half, _length)

        fin: str = ""
        for i in range(len(nH1)):
            fin += str(nH1[i] + nH2[i])

        if nM != 0:
            fin += str(nM)

        nL = len(fin)
        nH = int(nL / 2)
        if nL > 2:
            _got = rec(fin, nH, nL)
        else:
            return fin

        return _got

    if newL > 2:
        ans = rec(new, newH, newL)
    else:
        ans = new

    return ans


class DM(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="dmu")
    async def _dm(self, ctx, member: discord.Member, *, text):

        await member.send(text)

        await ctx.send(f"DMed {member.mention}", ephemeral=True)

    @commands.hybrid_command(name="ship", aliases=['rel'])
    async def ship(self, ctx, mem1: discord.Member, mem2: discord.Member = None):
        "Ship yourself/someone with any member."

        emojis = {
            "FL": "<:BarLeft:1065987058285428817>",
            "FM": "<:BarMiddle:1065987230377709568>",
            "FR": "<:BarRight:1065987253622546442>",
            "EL": "<:EmptyLeft:1065982622020411483>",
            "EM": "<:EmptyMiddle:1065982510741340300>",
            "ER": "<:EmptyRight:1065982515640287302>",
            "HL": "<:HalfLeft:1065982520010735647>",
            "HM": "<:HalfMiddle:1065982524607701042>",
            "HR": "<:HalfRight:1065982528990744686>"
        }

        if not mem2:
            mem2 = ctx.author

        background = Image.open("bg.jpg")
        asset1 = mem1.avatar
        asset2 = mem2.avatar
        data1 = BytesIO(await asset1.read())
        data2 = BytesIO(await asset2.read())
        pfp1 = Image.open(data1).resize((128, 128))
        pfp2 = Image.open(data2).resize((128, 128))

        background.paste(pfp1, (80, 69))
        background.paste(pfp2, (357, 69))
        background.save("ship.jpg")

        File = discord.File("ship.jpg")

        got = calc(str(mem1.name), str(mem2.name))
        tot = int(int(got) / 100 * 20)
        des = f"You two got {got}%\n"

        if int(got) > 5:
            des += emojis["FL"]

        else:
            des += emojis["HL"]

        if int(got) > 95:
            des += emojis["FM"] * (tot - 2)

            if int(got) < 98:
                des += emojis["HR"]
            else:
                des += emojis["FR"]

        else:
            des += emojis["FM"] * (tot - 1) + emojis["EM"] * (19 - tot) + emojis["ER"]

        em = discord.Embed(title=f"{mem1.name} and {mem2.name}", description=des)

        em.set_image(url="attachment://ship.jpg")

        await ctx.send(file=File, embed=em)

    @commands.command()
    async def role(self, ctx):

        roles = await ctx.guild.fetch_roles()
        send = ""
        lst = []

        for i in roles:
            send += f"{i.mention}, {i.id}\n"
            if len(send) > 1700:
                lst.append(send)
                send = ""

        lst.append(send)

        for msgs in lst:
            await ctx.send(msgs)


async def setup(client):
    await client.add_cog(DM(client))
