from discord.ext import commands


class EventosReady(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if not self.bot.user:
            return
        
        print(
            f"""
===================================
Rayquaza conectado com sucesso!
===================================
Usuario: {self.bot.user.name}
ID: {self.bot.user.id}
===================================
            """
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EventosReady(bot))