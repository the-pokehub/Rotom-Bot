import discord
from discord.ext import commands
# from PyDictionary import PyDictionary
from googletrans import Translator, LANGUAGES
# translatorG = Translator()


def trans(text, src="auto", dest='en'):

    translator = Translator()
    translated = translator.translate(text, src=src, dest=dest)
    return translated


# def trans(txt, src="auto", dest="en"):

#     lated = translatorG.translate(txt, src=src, dest=dest)
#     return lated
#     pass

# dictionary = PyDictionary()


class Trans(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        # return

        msgID = payload.message_id
        emoji = payload.emoji
        channel = self.client.get_channel(payload.channel_id)
        try:
            msg = await channel.fetch_message(msgID)
        except Exception:
            pass

        emoji_list = {
            "🇮🇳": "hi",
            "🇬🇧": "en",
            "🇪🇸": "spanish",
            "🇯🇵": "japanese",
            "🇧🇩": "bangla",
            "🇫🇷": "french",
            "🇩🇪": "german",
            "🇰🇵": "korean",
            "🇳🇵": "nepali",
            "🇵🇭": "filipino",
            "🇺🇸": "en"
        }

        if str(emoji) in emoji_list:
            for r in msg.reactions:
                if r.count > 1:
                    return

            dest = emoji_list[str(emoji)]
            src = "auto"
            got = trans(msg.content, src, dest)

            em = discord.Embed(title="Translated",
                               color=discord.Color.orange())

            em.add_field(name="Original Text", value=msg.content, inline=False)
            em.add_field(name="Translated Text", value=got.text, inline=False)

            try:
                src_lang = LANGUAGES[got.src].capitalize()
            except KeyError:
                src_lang = got.src
            try:
                dest_lang = LANGUAGES[got.dest].capitalize()
            except KeyError:
                dest_lang = got.dest

            em.add_field(name="Source Language", value=src_lang, inline=True)
            em.add_field(name="Destination Language",
                         value=dest_lang,
                         inline=True)

            await msg.reply(embed=em, mention_author=False)

    @commands.hybrid_command(name="id")
    async def _id(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        await ctx.send(f"{member.id}")

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx):
        await ctx.send("Pong! Response Time: **{}ms**".format(
            int(self.client.latency * 1000)))

    @commands.hybrid_command(name="icon")
    async def icon(self, ctx):
        "Get icon of the server."

        em = discord.Embed(title=f"{ctx.guild.name}'s Icon")
        em.set_image(url=ctx.guild.icon.url)
        em.set_footer(text=f"Requested by {ctx.author}",
                      icon_url=ctx.author.display_avatar)

        await ctx.send(embed=em)

    @commands.hybrid_command(name="translate", aliases=["t"])
    async def transC(self, ctx, *, text, src="auto", dest="en"):
        "Translate from Source to Destination."

        to_trans = text.strip()
        got = trans(to_trans, src, dest)

        em = discord.Embed(title="Translated", color=discord.Color.orange())

        em.add_field(name="Original Text", value=to_trans, inline=False)
        em.add_field(name="Translated Text", value=got.text, inline=False)

        try:
            src_lang = LANGUAGES[got.src].capitalize()
        except KeyError:
            src_lang = got.src
        try:
            dest_lang = LANGUAGES[got.dest].capitalize()
        except KeyError:
            dest_lang = got.dest

        em.add_field(name="Source Language", value=src_lang, inline=True)
        em.add_field(name="Destination Language", value=dest_lang, inline=True)

        await ctx.send(embed=em)

    # @commands.hybrid_command(name="dictionary", aliases=["meaning"])
    # async def dict(self, ctx, *, word):

    #     "Find word meaning."

    #     mean = dictionary.meaning(word, disable_errors=True)

    #     if mean:
    #         em = discord.Embed(title=f"Meaning of {word.capitalize()}", colour=discord.Colour.green())

    #         for i in mean:
    #             em.add_field(name=i, value="\n".join(mean[i]), inline=False)

    #         syono = dictionary.synonym(word)
    #         ayono = dictionary.antonym(word)

    #         if syono:
    #             em.add_field(name="Synonyms:", value=", ".join(syono))

    #         if ayono:
    #             em.add_field(name="Antonyms:", value=", ".join(ayono))

    #     else:
    #         em = discord.Embed(title="❌Error Nothing Found!", colour=discord.Colour.green())

    #     await ctx.send(embed=em)


async def setup(client):
    await client.add_cog(Trans(client))
