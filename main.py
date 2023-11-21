import discord
import settings
from discord.ext import commands

logging = settings.logging.getLogger("bot")

def main():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix = "!", intents = intents)


    @bot.event
    async def on_ready():
        logging.info(f"Se ha iniciado sesión correctamente como: {bot.user}")

        for cog_file in settings.COG_DIR.glob("*.py"):
            if cog_file != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")

    @bot.command()
    async def unload(ctx, cog: str):
        await bot.unload_extension(f"cogs.{cog.lower()}")
        await ctx.send(f"Se ha desactivado {cog.lower()} correctamente")

    @bot.command()
    async def load(ctx, cog: str):
        await bot.load_extension(f"cogs.{cog.lower()}")
        await ctx.send(f"Se ha cargado {cog.lower()} correctamente")

    @bot.command()
    async def reload(ctx, cog: str):
        await bot.reload_extension(f"cogs.{cog.lower()}")
        await ctx.send(f"Se ha recargado {cog.lower()} correctamente")

    
    bot.run(settings.TOKEN, root_logger = True)


if __name__ == "__main__":
    main()