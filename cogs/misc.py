import discord
from discord.ext import commands
import googletrans
from googletrans import Translator
from better_profanity import profanity
from googlesearch import search

translator = Translator()

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def av(self, ctx, *, member: discord.Member = None):

        if member is None:
            member = ctx.author

        em = discord.Embed(title=f"{member}'s Avatar")
        em.set_image(url=member.avatar_url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=em)

    @commands.command(aliases=["id"])
    async def _id(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        await ctx.send(f"{member.id}")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong! Response Time: **{}ms**".format(
            int(self.client.latency * 1000)))

    @commands.command()
    async def icon(self, ctx):

        em = discord.Embed(title=f"{ctx.guild.name}'s Icon")
        em.set_image(url=ctx.guild.icon_url)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=em)

    @commands.command(aliases=["t", "translate"])
    async def trans(self, ctx, *, text):

        if text == "--lang" or text == "--languages" or text == "--language":
            languages = googletrans.LANGUAGES
            await ctx.send(languages)

        elif "--" in text:
            text = text.split("--")
            if len(text) == 3:
                gtranslated = translator.translate(text[0], src=text[1].replace(" ", ""), dest=text[2].replace(" ", ""))
                if profanity.contains_profanity(gtranslated.text):
                    await ctx.send("You cannot use banned words!")
                    return

                await ctx.send(gtranslated.text)
            else:
                gtranslated = translator.translate(text[0], src=text[1].replace(" ", ""))
                if profanity.contains_profanity(gtranslated.text):
                    await ctx.send("You cannot use banned words!")
                    return
                await ctx.send(gtranslated.text)

        elif text.isnumeric():
            msg = await ctx.fetch_message(int(text))
            gtranslated = translator.translate(msg.content)
            if profanity.contains_profanity(gtranslated.text):
                await ctx.send("You cannot use banned words!")
                return
            await ctx.send(f"{msg.content}\n{gtranslated.text}")

        else:
            gtranslated = translator.translate(text)
            if profanity.contains_profanity(gtranslated.text):
                await ctx.send("You cannot use banned words!")
                return
            try:
                await ctx.send(f"{gtranslated.text}\nLanguage Detected: {googletrans.LANGUAGES[gtranslated.src].capitalize()}")
            except KeyError:
                await ctx.send(f"{gtranslated.text}\nLanguage Detected: Error in Detection...")

    @commands.command()
    async def dance(self, ctx):
        await ctx.send("<a:dance1:807167808164331531>\n<a:dance2:807167807757746177>\n<a:dance3:807167807804014602>\n<a:dance4:807167807904940073>")    

    @commands.command()
    async def say(self, ctx, *, txt):

        await ctx.message.delete()

        if profanity.contains_profanity(txt):
            await ctx.send("You cannot use banned words!")
            return

        if "--" in txt:
            txt = txt.split("--")
            channel = self.client.get_channel(int(txt[1]))
            await channel.send(txt[0])
        else:
            channel = ctx.channel
            await channel.send(txt)

    @commands.command(aliases=["search", "query"])
    async def google(self, ctx, *, query):

        async with ctx.typing():
            results =  search(query, tld="com", num=1, stop=1)
            for i in results:
                await ctx.send(i)
            return

        
def setup(client):
    client.add_cog(Misc(client))
