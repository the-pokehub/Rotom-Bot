import discord
import googletrans
from discord.ext import commands
from googletrans import Translator
from better_profanity import profanity
from googlesearch import search
from PyDictionary import PyDictionary

dictionary = PyDictionary()

translator = Translator()
profanity.load_censor_words_from_file("swear_words.txt")


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

        src = "auto"
        dest = "en"
        det = False

        if "--" in text:
            text = text.split("--")
            if len(text) == 3:
                src = text[1].replace(" ", "")
                dest = text[2].replace(" ", "")

            else:
                src = text[1].replace(" ", "")
                dest = "en"

            to_trans = text[0]

        else:
            to_trans = text
            det = True

        to_trans = to_trans.strip()

        if det:

            if to_trans.isnumeric():
                msg = await ctx.fetch_message(int(to_trans))
                gtranslated = translator.translate(msg.content, src=src, dest=dest)
                if profanity.contains_profanity(gtranslated.text):
                    await ctx.send("You cannot use banned words!")
                    return

                try:
                    await ctx.send(
                        f"{gtranslated.text}\nLanguage Detected: {googletrans.LANGUAGES[gtranslated.src].capitalize()}")
                except KeyError:
                    await ctx.send(f"{gtranslated.text}\nLanguage Detected: Error in Detection...")

            else:
                gtranslated = translator.translate(to_trans, src=src, dest=dest)
                if profanity.contains_profanity(gtranslated.text):
                    await ctx.send("You cannot use banned words!")
                    return

                try:
                    await ctx.send(
                        f"{gtranslated.text}\nLanguage Detected: {googletrans.LANGUAGES[gtranslated.src].capitalize()}")
                except KeyError:
                    await ctx.send(f"{gtranslated.text}\nLanguage Detected: Error in Detection...")
        else:

            if to_trans.isnumeric():
                msg = await ctx.fetch_message(int(to_trans))
                gtranslated = translator.translate(msg.content, src=src, dest=dest)
                if profanity.contains_profanity(gtranslated.text):
                    await ctx.send("You cannot use banned words!")
                    return

                await ctx.send(f"{msg.content}\n{gtranslated.text}")

            else:
                gtranslated = translator.translate(to_trans, src=src, dest=dest)
                if profanity.contains_profanity(gtranslated.text):
                    await ctx.send("You cannot use banned words!")
                    return

                await ctx.send(f"{gtranslated.text}")

    @commands.command()
    async def dance(self, ctx):
        await ctx.send(
            "<a:dance1:807167808164331531>\n<a:dance2:807167807757746177>\n<a:dance3:807167807804014602>\n<a:dance4:807167807904940073>")

    @commands.command()
    async def say(self, ctx, *, txt=None):

        if txt is None:
            return

        try:
            await ctx.message.delete()
        except discord.errors.NotFound:
            pass

        if profanity.contains_profanity(txt):
            await ctx.send("You cannot use banned words!")
            return

        if "--" in txt:
            txt = txt.split("--")
            channel = self.client.get_channel(int(txt[1]))
            txt = txt[0]
        else:
            channel = ctx.channel

        send = " "
        emoj = ""
        emo = False

        if ":" in txt:
            txt = txt.split(":")
            for name in txt:
                emo = False
                for emoji in ctx.guild.emojis:
                    if name == emoji.name:
                        t = str(emoji)
                        emoj = emoji.id
                        send += t
                        emo = True

                if not emo:
                    if ">" in name:
                        name = name.replace(">", "")
                        if name.isnumeric():
                            if int(name) == int(emoj):
                                continue

                    if "<" in name[-2:]:
                        if "<a" in name:
                            name = name.replace("<a", "")
                        else:
                            name = name[:-1]
                            another_name = name.replace(" ","")
                            if another_name.isnumeric():
                                if int(name) == int(emoj):
                                    continue
                    send += name
                
        else:
            send = txt
                
        await channel.send(send)

    @commands.command(aliases=["search", "query"])
    async def google(self, ctx, *, query):

        async with ctx.typing():
            results = search(query, tld="com", num=1, stop=1)
            for i in results:
                await ctx.send(i)
            return

    @commands.command()
    async def invite(self, ctx):

        em = discord.Embed(description="[**__Here's the link to invite the bot 😉__**](https://discord.com/api/oauth2/authorize?client_id=783598148039868426&permissions=8&scope=bot)",
                           colour=discord.Colour.green())

        await ctx.send(embed=em)

    @commands.command(aliases=["meaning", "dictionary"])
    async def dict(self, ctx, *, word):

        mean = dictionary.meaning(word, disable_errors=True)

        if mean:
            em = discord.Embed(title=f"Meaning of {word.capitalize()}", colour=discord.Colour.green())

            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/819090822884491274/820149994572218368/dictionary.jpg")

            for i in mean:
                em.add_field(name=i, value="\n".join(mean[i]), inline=False)

            syono = dictionary.synonym(word)
            ayono = dictionary.antonym(word)

            if syono:
                em.add_field(name="Synonyms:", value=", ".join(syono))

            if ayono:
                em.add_field(name="Antonyms:", value=", ".join(ayono))

        else:
            em = discord.Embed(title="❌Error Nothing Found!", colour=discord.Colour.green())

        await ctx.send(embed=em)

    @commands.command()
    async def bump(self, ctx):

        em = discord.Embed(description="[**__Here's the link to bump our server 😉__**](https://discordservers.com/server/676777139776913408/bump)", colour=discord.Colour.green())

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Misc(client))
