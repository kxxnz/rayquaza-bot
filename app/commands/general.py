import discord
from discord.ext import commands


class ComandosGerais(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.command(name="ping")
    async def ping(self, contexto: commands.Context) -> None:
        latencia = round(self.bot.latency * 1000)  # Converter para milissegundos
        
        await contexto.send(f"Pong! Latência: {latencia}ms")
        
    @commands.command(name="sobre")
    async def sobre(self, contexto: commands.Context) -> None:
        embed = discord.Embed(
            title="Rayquaza",
            description=("Bot para automações e integrações com microserviços."),
            color=discord.Color.green(),
        )
        
        await contexto.send(embed=embed)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ComandosGerais(bot))