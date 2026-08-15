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
        
    @commands.command(name="pfp")
    async def pfp (self, contexto: commands.Context, membro: discord.Member | None = None) -> None:
        usuario = membro or contexto.author
        avatar = usuario.display_avatar.replace(size=1024)
        
        embed = discord.Embed(title=f"Foto de perfil de {usuario.display_name}", color=discord.Color.green())
        
        embed.set_image(url=avatar.url)
        
        view = discord.ui.View()
        
        view.add_item(discord.ui.Button(label="Abrir ou baixar imagem",
                                        style=discord.ButtonStyle.link,
                                        url=avatar.url,
                                        emoji="📥"))

        await contexto.reply(embed=embed,
                             view=view,
                             mention_author=False)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ComandosGerais(bot))