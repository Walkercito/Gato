import discord
import settings
from claude import Claude
from discord.ext import commands

class GenerateResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cookie = settings.COOKIE
        self.claude = Claude(self.cookie)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if "claude" in message.content.lower():
            prompt = message.content 

            async with message.channel.typing():
                try:
                    response = self.generate_response(prompt)
                    await message.channel.send(response)

                except Exception as e:
                    await message.channel.send(f"Ocurrió un error al generar la respuesta: {e}")

    def generate_response(self, prompt):
        try:
            response = self.claude.get_answer(prompt)
            return response
        except Exception as e:
            return f"Ocurrió un error: {e}"
        
    @commands.command()
    async def new(self, ctx):
        self.claude.create_new_conversation()
        await ctx.send('Listo')


async def setup(bot):
    await bot.add_cog(GenerateResponse(bot))