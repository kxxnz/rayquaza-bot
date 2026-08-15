import logging

import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class EventosMembros(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, membro: discord.Member) -> None:
        logger.info(
            "Membro entrou | usuario=%s | usuario_id=%s | servidor=%s", membro, membro.id, membro.guild.name)

        try:
            await membro.send(
                f"Seja bem-vindo ao servidor {membro.guild.name}, "
                f"{membro.mention}!"
            )
        except discord.Forbidden:
            logger.warning("Nao foi possivel enviar mensagem privada | usuario=%s | usuario_id=%s", membro, membro.id,)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EventosMembros(bot))