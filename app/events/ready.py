import logging

from discord.ext import commands


logger = logging.getLogger(__name__)


class EventosReady(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if self.bot.user is None:
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

    @commands.Cog.listener()
    async def on_command(self, contexto: commands.Context) -> None:
        comando = (contexto.command.qualified_name if contexto.command else "desconhecido")
        servidor = contexto.guild.name if contexto.guild else "Mensagem direta"
        canal = getattr(contexto.channel, "name", "desconhecido")

        logger.info(
            "Comando iniciado | comando=%s | usuario=%s | "
            "usuario_id=%s | servidor=%s | canal=%s",
            comando,
            contexto.author,
            contexto.author.id,
            servidor,
            canal,
        )

    @commands.Cog.listener()
    async def on_command_completion(self, contexto: commands.Context,) -> None:
        comando = (contexto.command.qualified_name if contexto.command else "desconhecido")
        servidor = contexto.guild.name if contexto.guild else "Mensagem direta"
        canal = getattr(contexto.channel, "name", "desconhecido")

        logger.info(
            "Comando concluido | comando=%s | usuario=%s | "
            "usuario_id=%s | servidor=%s | canal=%s",
            comando,
            contexto.author,
            contexto.author.id,
            servidor,
            canal,
        )

    @commands.Cog.listener()
    async def on_command_error(self, contexto: commands.Context,erro: commands.CommandError,) -> None:
        if isinstance(erro, commands.CommandNotFound):
            logger.warning("Comando inexistente | usuario=%s | mensagem=%s", contexto.author,contexto.message.content,)
            return

        comando = (contexto.command.qualified_name if contexto.command else "desconhecido")
        servidor = contexto.guild.name if contexto.guild else "Mensagem direta"
        canal = getattr(contexto.channel, "name", "desconhecido")

        logger.error(
            "Erro no comando | comando=%s | usuario=%s | "
            "usuario_id=%s | servidor=%s | canal=%s | erro=%s",
            comando,
            contexto.author,
            contexto.author.id,
            servidor,
            canal,
            erro,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EventosReady(bot))