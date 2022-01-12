import discord
from discord.ext import commands
import asyncio

class Battler(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # listen battler ping and send pinger message if someone messages in channel
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.client.user:
            return

        def check(ms):
            reply = str(ms.content.lower()).replace(' ', '')
            is_battle_reply = 'ok' in reply or 'me' in reply or 'come' in reply or 'want' in reply or 'sd' in reply or 'ican' in reply

            return is_battle_reply and ms.channel == message.channel


        battler_id = 836091181662339102
        battling_stadium_id = 836091911642152980
        mention_ids = [mention.id for mention in message.role_mentions]
        
        if message.channel.id == battling_stadium_id and battler_id in mention_ids:

            try:
                msg = await self.client.wait_for("message", check=check, timeout=900)
                                                 
                em = discord.Embed(
                title = f"{msg.author} accepts your challenge!",
                description = f"**Head over to #{message.channel} in {message.guild} to schedule your battle with {msg.author}.**",
                colour=discord.Color.orange())

                await message.author.send(embed=em)

            except asyncio.TimeoutError:
                return

        return

            
def setup(client):
    client.add_cog(Battler(client))