import discord
from discord.ext import commands
import asyncio
from replit import db


class Game(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def loading(self, ctx, time: int):
        loadingList = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
        msg = await ctx.send(f"Loading...\n{loadingList[0]}")
        try:
            for i in range(1, len(loadingList)):
                # await asyncio.sleep(time)
                await msg.edit(content=f"Loading...\n{loadingList[i]}")
            await msg.delete()
        except discord.errors.NotFound:
            pass

    @commands.group(invoke_without_command=True,
                    case_insensitive=True)
    async def coc(self, ctx):

        unite = db["coc"]

        num = 0
        sendLst = []
        desc = ""

        for i in unite:
            try:
                mem = await ctx.guild.fetch_member(int(i))
                desc += f"{mem.mention} **Name:** {unite[i]['name'] }, **Player Tag:** {unite[i]['id']}\n"
                num += 1

                if num >= 20:
                    sendLst.append(desc)
                    desc = ""
                    num = 0
            except Exception:
                pass

        sendLst.append(desc)

        page = 0

        em1 = discord.Embed(title="Clash of Clans IDs",
                            colour=0x8452ff,
                            description=sendLst[page])
        # em1.set_thumbnail(url="https://cdn.discordapp.com/attachments/847509607185383494/894968904219263016/PULOGO-SQ.png")
        em1.set_footer(text=f"Page {page+1} out of {len(sendLst)}")

        msg = await ctx.send(embed=em1)
        await msg.add_reaction("◀️")
        await msg.add_reaction("▶️")

        async def editEM(page):

            em2 = discord.Embed(title="Clash of Clans IDs",
                                colour=0x8452ff,
                                description=sendLst[page])
            em2.set_footer(text=f"Page {page+1} out of {len(sendLst)}")
            # em2.set_thumbnail(url="https://cdn.discordapp.com/attachments/847509607185383494/894968904219263016/PULOGO-SQ.png")
            await msg.edit(embed=em2)

            await msg.remove_reaction("◀️", ctx.author)
            await msg.remove_reaction("▶️", ctx.author)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["▶️", "◀️"]

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=30)

                if str(reaction.emoji) == "▶️":
                    if page + 2 > len(sendLst):
                        await msg.remove_reaction("▶️", ctx.author)
                        continue
                    else:
                        page += 1

                elif str(reaction.emoji) == "◀️":
                    if page - 1 < 0:
                        await msg.remove_reaction("◀️", ctx.author)
                        continue
                    else:
                        page -= 1

                await editEM(page)

            except asyncio.TimeoutError:
                return await msg.clear_reactions()

    @coc.command()
    async def add(self, ctx, *, info):

        if ctx.guild.id != 676777139776913408:
            return

        if "--" in info:
            if not ctx.author.guild_permissions.manage_guild:
                return await ctx.send("You cannot add data of Other Member. Ask a Moderator to do it.")

            info = info.split("--")
            text = info[0]
            mem = self.client.get_user(int(info[1].replace(" ", "")))

        else:
            mem = ctx.author
            text = info

        txt = text.split(",")
        name = txt[0]
        id = txt[1].replace(" ", "")
        if not id.startswith("#"):
            return await ctx.send("Wrong Player Tag.")

        unite = db["coc"]

        unite[str(mem.id)] = {"id": id, "name": name}
        db["unite"] = unite

        return await ctx.send(f"Added {mem.mention} with Name: {name} and Tag: {id}!")

    @coc.command()
    async def remove(self, ctx, *, mem: discord.Member):

        if ctx.guild.id != 676777139776913408:
            return

        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.send("You don't have permission to use this command.")

        unite = db["coc"]
        if str(mem.id) in unite:
            del unite[str(mem.id)]
        else:
            return ctx.send(f"{mem} was not registered.")

        await ctx.send(f"{mem}'s Data removed.")


async def setup(client):
    await client.add_cog(Game(client))
