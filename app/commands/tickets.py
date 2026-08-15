import logging

import discord
from discord.ext import commands

from app.config import configuracoes
from app.tickets.painel import PainelTickets


logger = logging.getLogger(__name__)


class ComandosTickets(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.command(name="painel-tickets")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def publicar_painel(self, contexto: commands.Context) -> None:
        if contexto.guild is None:
            return
        
        canal = contexto.guild.get_channel(configuracoes.ticket_panel_channel_id)
        
        if not isinstance(canal, discord.TextChannel):
            await contexto.reply("O canal do painel de tickets nao foi encontrado.", mention_author=False)
            return
        
        await canal.send(view=PainelTickets())
        
        await contexto.reply(f"Painel publicado em {canal.mention}", mention_author=False)
        
        logger.info("Painel de tickets publicado | usuario=%s | canal=%s", contexto.author, canal.name)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ComandosTickets(bot))