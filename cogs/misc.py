import discord
import googletrans
from discord.ext import tasks, commands
from googletrans import Translator
from better_profanity import profanity
from googlesearch import search
from PyDictionary import PyDictionary
import datetime
from bs4 import BeautifulSoup
import requests


dictionary = PyDictionary()

translator = Translator()
profanity.load_censor_words_from_file("swear_words.txt")


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        msgID = payload.message_id
        emoji = payload.emoji
        channel = self.client.get_channel(payload.channel_id)
        msg = await channel.fetch_message(msgID)
        users_list = []

        emoji_list = {
            "🇮🇳": "hi",
            "🇬🇧": "en",
            "🇪🇸": "Spanish",
            "🇯🇵": "japanese",
            "🇧🇩": "bangla",
            "🇫🇷": "french",
            "🇩🇪": "genman",
            "🇰🇵": "korean",
            "🇳🇵": "nepali",
            "🇵🇭": "filipino",
            "🇺🇸": "en"
        }

        if str(emoji) in emoji_list:
            for r in msg.reactions:
                if str(r) in emoji_list:
                    users = await r.users().flatten()
                    users_list.extend(users)

            if len(users_list) > 1:
                return

            dest = emoji_list[str(emoji)]
            src = "auto"
            gtranslated = translator.translate(msg.content, src=src, dest=dest)
            if profanity.contains_profanity(gtranslated.text):
                return

            try:
                await msg.reply(
                    f"{gtranslated.text}\nLanguage Detected: {googletrans.LANGUAGES[gtranslated.src].capitalize()}", mention_author=False)
            except KeyError:
                pass

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

    @commands.command()
    async def banner(self, ctx):
        em = discord.Embed(title=f"{ctx.guild.name}'s Banner")
        em.set_image(url=ctx.guild.banner_url)
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

    # @commands.command()
    # async def say(self, ctx, *, txt=None):

    #     if txt is None:
    #         return

    #     try:
    #         await ctx.message.delete()
    #     except discord.errors.NotFound:
    #         pass

    #     if profanity.contains_profanity(txt):
    #         await ctx.send("You cannot use banned words!")
    #         return

    #     if "--" in txt:
    #         txt = txt.split("--")
    #         channel = self.client.get_channel(int(txt[1]))
    #         txt = txt[0]
    #     else:
    #         channel = ctx.channel

    #     send = " "
    #     emoj = 0
    #     emo = False

    #     if ":" in txt:
    #         txt = txt.split(":")
    #         for name in txt:

    #             emoji = discord.utils.get(self.client.emojis, name = name)

    #             if emoji:
    #                 t = str(emoji)
    #                 emoj = emoji.id
    #                 send += t

    #             if not emoji:
    #                 name = name.replace(" ", "")
    #                 if ">" in name:
    #                     name = name.replace(">", "")
    #                     if name.isnumeric():
    #                         if int(name) == int(emoj):
    #                             name = ""
    #                         else:
    #                             if len(name) == 18:
    #                                name = ""

    #                 if "<" in name[-2:]:
    #                     if "<a" in name:
    #                         name = name.replace("<a", "")
    #                     else:
    #                         name = name[:-1]
    #                         another_name = name.replace(" ", "")
    #                         if another_name.isnumeric():
    #                             if int(name) == int(emoj):
    #                                 name = ""
    #                             else:
    #                                 if len(name) == 18:
    #                                     name = ""
                    
    #                 send += name

    #     else:
    #         send = txt

    #     if ctx.author.guild_permissions.mention_everyone:
    #         allowed_mentions=discord.AllowedMentions(everyone=True, roles=True)
    #     else:
    #         allowed_mentions=discord.AllowedMentions(everyone=False, roles=False)

    #     webhooks = await channel.webhooks()
    #     webhook = discord.utils.get(webhooks, name = "Rotom Bot")
    #     if webhook is None:
    #         webhook = await channel.create_webhook(name = "Rotom Bot")

    #     await webhook.send(send, username = ctx.author.name, avatar_url = ctx.author.avatar_url, allowed_mentions=allowed_mentions)


    @commands.command(aliases=["search", "query"])
    async def google(self, ctx, *, query):

        def gsearch(query_raw):

            des = ""

            r = search(query_raw, stop=10)
            for i in r:
                url = i

                try:
                    reqs = requests.get(url)
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.TooManyRedirects:
                    pass
                except requests.exceptions.RequestException:
                    pass

                soup = BeautifulSoup(reqs.text, 'html.parser')

                for title in soup.find_all('title'):
                    tit = title.get_text()
                    if tit == "":
                        txt = f"__{i}__\n"
                    else:
                        txt = f"[__{tit}__]({i})\n"
                    des += txt
                    break

            return des

        async with ctx.typing():

            result = gsearch(query)

            em = discord.Embed(title=f"Search Results for {query.capitalize()}", description=result)

            await ctx.send(embed=em)

    @commands.command()
    async def invite(self, ctx):

        em = discord.Embed(
            description="[**__Here's the link to invite the bot 😉__**](https://discord.com/api/oauth2/authorize?client_id=783598148039868426&permissions=8&scope=bot)",
            colour=discord.Colour.green())

        await ctx.send(embed=em)

    @commands.command(aliases=["meaning", "dictionary"])
    async def dict(self, ctx, *, word):

        mean = dictionary.meaning(word, disable_errors=True)

        if mean:
            em = discord.Embed(title=f"Meaning of {word.capitalize()}", colour=discord.Colour.green())

            # em.set_thumbnail(
            #     url="https://cdn.discordapp.com/attachments/819090822884491274/820149994572218368/dictionary.jpg")

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

        em = discord.Embed(
            description="[**__Here's the link to bump our server 😉__**](https://discordservers.com/server/676777139776913408/bump)",
            colour=discord.Colour.green())

        await ctx.send(embed=em)

    @tasks.loop(seconds=60)
    async def wishBirthday(ctx):
        timenow = datetime.datetime.now()
        timenow = str(timenow)[:-10]
        if timenow == '2021-04-09 13:00':
            channel = ctx.get_channel(761502109459677185)
            await channel.send(
                'Happy Birthday Mia! I remembered your birthday! Have a blast today! :partying_face: :partying_face: :partying_face:')
        if timenow == '2021-04-09 23:00':
            channel = ctx.get_channel(761502109459677185)
            await channel.send(
                'Happy Birthday Infernape! I remembered your birthday! Have a blast today! :partying_face: :partying_face: :partying_face:')
        if timenow[14:] == '00':
            print(timenow)


def setup(client):
    Misc.wishBirthday.start(client)
    client.add_cog(Misc(client))
