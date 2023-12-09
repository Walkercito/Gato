import discord, requests, os
from bardapi import BardCookies
from discord.ext import commands

class BardResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cookie = {
            "__Secure-1PSID": "dwhlrLY0kJrd_kbHsIPdHEOBBQKt1vcrbh-L6a0OjKSnqw1Co9h8ieKnntKtgy_R8L24QQ.",
            "__Secure-1PSIDTS": "sidts-CjIBPVxjStb8Pcd-DbAR7LWsqbD-9_Be5EAV7UcKrFIBDpnhqID3cf9M8mMhGPC6JfxMsRAA",
            "__Secure-1PSIDCC":"ACA-OxPK5YV46lKG6gH62eSlssMFWvmObUQ28qwYAhmHp73NgLbfvT_A2JLG-tbfR-WxupaZRmw"
        }
        self.bard = BardCookies(cookie_dict = self.cookie)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if "bard" in message.content.lower():
            prompt = message.content 

            async with message.channel.typing():
                if message.attachments:
                    try:
                        attatchment_url = message.attachments[0]
                        attatchment_url = requests.get(attatchment_url.url)
                        response = self.generate_image_response(prompt, attatchment_url)
                        await message.channel.send(response)

                    except Exception as e:
                        await message.channel.send(f"Ocurrió un error al generar la respuesta: {e}")
                else:
                    try:
                        response = self.generate_response(prompt)
                        await message.channel.send(response)

                    except Exception as e:
                        await message.channel.send(f"Ocurrió un error al generar la respuesta: {e}")

    def generate_response(self, prompt):
        try:
            response = self.bard.get_answer(prompt)['content']
            return response
        except Exception as e:
            return f"Ocurrió un error: {e}"


    def generate_image_response(self, prompt, photo):
        try:
            photo = open("imagen.jpg", 'rb').read()
            response = self.bard.ask_about_image(prompt, photo)
            try:
                os.remove("imagen.jpg")
            except Exception:
                pass
            return response['content']
        except Exception as e:
            return f"Ocurrió un error: {e}"


async def setup(bot):
    await bot.add_cog(BardResponse(bot))