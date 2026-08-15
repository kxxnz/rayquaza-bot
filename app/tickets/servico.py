import logging
import re

import discord
from discord.ext import commands

from app.config import configuracoes


logger = logging.getLogger(__name__)


class ServicoTickets:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def criar_ticket(
        self,
        interaction: discord.Interaction,
    ) -> tuple[discord.TextChannel | None, bool]:
        servidor = interaction.guild
        usuario = interaction.user

        if servidor is None:
            return None, False

        categoria = servidor.get_channel(
            configuracoes.ticket_category_id
        )

        if not isinstance(categoria, discord.CategoryChannel):
            logger.error(
                "Categoria de tickets não encontrada "
                "| categoria_id=%s",
                configuracoes.ticket_category_id,
            )
            return None, False

        ticket_existente = self.buscar_ticket_existente(
            categoria,
            usuario.id,
        )

        if ticket_existente:
            return ticket_existente, False

        nome_usuario = self.normalizar_nome(usuario.display_name)

        permissoes = {
            servidor.default_role: discord.PermissionOverwrite(
                view_channel=False,
            ),
            usuario: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
            ),
        }

        if servidor.me is not None:
            permissoes[servidor.me] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_channels=True,
            )

        try:
            canal = await categoria.create_text_channel(
                name=f"ticket-{nome_usuario}",
                topic=f"ticket_usuario_id={usuario.id}",
                overwrites=permissoes,
                reason=f"Ticket criado por {usuario} ({usuario.id})",
            )
        except discord.Forbidden:
            logger.exception(
                "Bot sem permissão para criar ticket "
                "| usuario=%s | usuario_id=%s | categoria=%s",
                usuario,
                usuario.id,
                categoria.name,
            )
            return None, False
        except discord.HTTPException:
            logger.exception(
                "Erro do Discord ao criar ticket "
                "| usuario=%s | usuario_id=%s",
                usuario,
                usuario.id,
            )
            return None, False

        logger.info(
            "Ticket criado | canal=%s | usuario=%s | "
            "usuario_id=%s | servidor=%s",
            canal.name,
            usuario,
            usuario.id,
            servidor.name,
        )

        return canal, True

    def buscar_ticket_existente(
        self,
        categoria: discord.CategoryChannel,
        usuario_id: int,
    ) -> discord.TextChannel | None:
        topico = f"ticket_usuario_id={usuario_id}"

        return discord.utils.find(
            lambda canal: canal.topic == topico,
            categoria.text_channels,
        )

    def normalizar_nome(self, nome: str) -> str:
        nome = nome.lower().strip()
        nome = re.sub(r"[^a-z0-9-]", "-", nome)
        nome = re.sub(r"-+", "-", nome)
        nome = nome.strip("-")

        return nome[:50] or "usuario"