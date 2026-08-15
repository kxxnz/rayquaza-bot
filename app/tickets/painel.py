import logging

import discord

from app.tickets.servico import ServicoTickets


logger = logging.getLogger(__name__)


class BotaoCriarTicket(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(label="Criar ticket", style=discord.ButtonStyle.green, emoji="🎫", custom_id="tickets:criar")

    async def callback(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message("Os tickets só podem ser criados dentro do servidor.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True, thinking=True)

        servico = ServicoTickets(interaction.client)

        canal, criado = await servico.criar_ticket(interaction)

        if canal is None:
            await interaction.followup.send("Não foi possível criar o ticket. Verifique as permissões do bot.", ephemeral=True)
            return

        if not criado:
            await interaction.followup.send(f"Você já possui um ticket em aberto: {canal.mention}", ephemeral=True)
            return

        await canal.send(view=MensagemInicialTicket(interaction.user))

        await interaction.followup.send(f"Ticket criado com sucesso: {canal.mention}", ephemeral=True)


class PainelTickets(discord.ui.LayoutView):
    def __init__(self) -> None:
        super().__init__(timeout=None)

        container = discord.ui.Container(accent_color=discord.Color.green())

        container.add_item(
            discord.ui.TextDisplay(
                "# Central de atendimento\n"
                "Precisa falar com a equipe de suporte? "
                "Crie um ticket privado usando o botão abaixo."
            )
        )

        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))

        container.add_item(
            discord.ui.TextDisplay(
                "Antes de abrir o ticket:\n"
                "- Explique o problema com clareza.\n"
                "- Não compartilhe senhas ou tokens.\n"
                "- Evite criar mais de um ticket."
            )
        )

        botoes = discord.ui.ActionRow()
        botoes.add_item(BotaoCriarTicket())

        container.add_item(botoes)

        self.add_item(container)


class MensagemInicialTicket(discord.ui.LayoutView):
    def __init__(self, usuario: discord.User | discord.Member) -> None:
        super().__init__()

        container = discord.ui.Container(accent_color=discord.Color.green())

        container.add_item(
            discord.ui.TextDisplay(
                "# Ticket aberto\n"
                f"Olá, {usuario.mention}.\n\n"
                "Descreva sua solicitação neste canal. "
                "A equipe de suporte responderá assim que possível."
            )
        )

        container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))

        container.add_item(
            discord.ui.TextDisplay(
                "Não envie senhas, tokens ou outras credenciais neste canal."
            )
        )

        self.add_item(container)