import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Configuracoes:
    bot_token: str
    command_prefix: str
    api_host: str
    api_port: int
    api_token: str
    notification_channel_id: int
    ticket_panel_channel_id: int
    ticket_category_id: int


def carregar_as_configuracoes() -> Configuracoes:
    bot_token = os.getenv("BOT_TOKEN")
    api_host = os.getenv("API_HOST")
    api_port = int(os.getenv("API_PORT"))
    api_token = os.getenv("API_TOKEN")
    notification_channel_id = int(os.getenv("CANAL_DE_PROMOCOES_DE_VOO"))
    ticket_panel_channel_id = int(os.getenv("TICKET_PANEL_CHANNEL_ID"))
    ticket_category_id = int(os.getenv("TICKET_CATEGORY_ID"))

    if not bot_token:
        raise ValueError("O token do bot nao foi configurado/encontrado.")
    if not api_host:
        raise ValueError("O host da API nao foi configurado/encontrado.")
    if not api_port:
        raise ValueError("A porta da API nao foi configurada/encontrada.")
    if not api_token:
        raise ValueError("O token da API nao foi configurado/encontrado.")
    if not notification_channel_id:
        raise ValueError("O ID do canal de notificacoes nao foi configurado/encontrado.")
    if not ticket_panel_channel_id:
        raise ValueError("O ID do canal de ticket nao foi configurado/encontrado.")
    if not ticket_category_id:
        raise ValueError("O ID da categoria de ticket nao foi configurado/encontrado.")

    return Configuracoes(bot_token=bot_token,
                         command_prefix='.',
                         api_host=api_host,
                         api_port=api_port,
                         api_token=api_token,
                         notification_channel_id=notification_channel_id,
                         ticket_category_id=ticket_category_id,
                         ticket_panel_channel_id=ticket_panel_channel_id)


configuracoes = carregar_as_configuracoes()
