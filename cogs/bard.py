import discord, requests, os
from bardapi import BardCookies
from discord.ext import commands

class BardResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cookie = {
            "__Secure-1PSID": "eghlrCxjL3KeVXIsSZ_zS62q0bZywO9-9LyYR-K4uIUabfkWNijAtGr53gc7EhUR2b2U6A.",
            "__Secure-1PSIDTS": "sidts-CjEBPVxjSllcseH4L9_qU2PBEJ8YY8SJngEOySzElBAt5agTI_NBfcy43w7G8PwPyM43EAA",
            "__Secure-1PSIDCC":"ABTWhQGrScVEpeuURt-VKyRjbAvWPYQsyCbsSlVy4XUs_U1RfSSGL77q1mhBb1PfvfMuy2aYEIg"
        }
        self.bard = BardCookies(cookie_dict = self.cookie)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if "gato" in message.content.lower():
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