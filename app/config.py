import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Configuracoes:
    bot_token: str
    command_prefix: str
    

def carregar_as_configuracoes() -> Configuracoes:
    bot_token = os.getenv("BOT_TOKEN")
    
    if not bot_token:
        raise ValueError("O token do bot nao foi configurado/encontrado.")
    
    return Configuracoes(
        bot_token=bot_token,
        command_prefix='.'
    )
    

configuracoes = carregar_as_configuracoes()