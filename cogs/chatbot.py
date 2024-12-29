import discord
from discord.ext import commands
from discord import app_commands
import httpx
from openai import OpenAI
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

name = "ai "
char_limit = 1800

client = OpenAI(
    base_url=os.getenv("api_base"),
    api_key=os.getenv("api"),
    http_client=httpx.Client(follow_redirects=True),
)

genai.configure(api_key=os.getenv("gemini_api"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


def gemini_ask(user):
    response = model.generate_content(user)
    return response.text


def aichat(ask):
    who = [
        "I am an AI language model created by Sayan, designed to assist and communicate with users through natural language processing. How may I assist you today?",
        "I am an AI language model created by Sayan, designed to assist and communicate with humans through natural language processing.",
    ]

    if len(ask) < 5:
        return "Ask a better question."

    if ask.lower() in ["who are you", "who are you?"]:
        return who[0]

    if "universal gay" in ask.lower():
        return "With all the information I am trained with, <@868018050945933382> is the universal gay."

    try:
        send = gemini_ask(ask)
    except Exception as e:
        print(e)
        return "Sorry, there is an internal issue with me at the moment. Contact Sayan to get me fixed asap."

    send = send.replace("As an AI language model,", "")

    def breakStr(message: str, max_length=1800):
        if len(message) <= max_length:
            return [message]

        parts = []
        while len(message) > max_length:
            break_point = max(
                message.rfind('\n', 0, max_length),
                message.rfind('. ', 0, max_length)
            )

            if break_point == -1:
                break_point = max_length

            parts.append(message[:break_point].strip())
            message = message[break_point:].strip()

        if message:
            parts.append(message)

        return parts

    if len(send) > char_limit:
        return breakStr(send)

    return send


def searchMov(name: str):
    name = name.replace(" ", ".").lower()
    url = f'intext:\"{name}\" (avi|mkv|mov|mp4|mpg|wmv|avchd|webm) -inurl:(jsp|pl|php|html|aspx|htm|cf|shtml) -inurl:(index_of|listen77|mp3raid|mp3toss|mp3drug|sirens|rocks|wallywashis) intitle:\"index.of./\"'
    return url


class Chatbot(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.guild is None:
            return

        if message.channel.id in [
            1052050303941365833, 770846450896470049,
            1065694309740990506, 901708512516784128
        ]:

            if message.content.lower().startswith(name.lower()):
                dm = False
                ask = message.content.lstrip("ai ").lower()

                if "dm me" in ask or "in dm" in ask:
                    dm = True
                    ask = ask.replace("dm me", "").replace("in dm", "")

                got = aichat(ask)

                if dm:
                    if isinstance(got, list):
                        await message.author.send(got[0])
                        for part in got[1:]:
                            await message.author.send(part)
                        return await message.reply("```Sent you in DM.```")

                    await message.author.send(got)
                    return await message.reply("```Sent you in DM.```")

                if isinstance(got, list):
                    await message.reply(got[0])
                    for part in got[1:]:
                        await message.channel.send(part)
                    return

                await message.reply(got)

    @commands.hybrid_command(name="ai-ask", aliases=["cb", "chatbot"])
    @app_commands.describe(personality="Coming Soon.")
    async def chatai(
        self,
        ctx,
        *,
        prompt,
        personality: discord.app_commands.Choice[int] = None
    ):
        "Chat or ask question with the chatbot."

        await ctx.defer()
        got = aichat(prompt)

        if isinstance(got, list):
            await ctx.reply(got[0])
            for part in got[1:]:
                await ctx.send(part)
            return

        await ctx.reply(got)

    @commands.hybrid_command(name="movie")
    async def movie(self, ctx, *, name):
        "Get link to download the searched movie."

        url = searchMov(name)
        await ctx.send(url)


async def setup(client):
    await client.add_cog(Chatbot(client))
