import discord
from discord.ext import commands

from app.config import configuracoes
from app.api.server import RayquazaAPI


class RayquazaBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.servidor_api = RayquazaAPI(
            bot=self,
            host=configuracoes.api_host,
            port=configuracoes.api_port,
            notification_channel_id=configuracoes.notification_channel_id,
        )
    
    async def setup_hook(self) -> None:
        # carregar as extensões do bot
        await self.load_extension("app.commands.general")
        await self.load_extension("app.events.ready")
        await self.load_extension("app.events.membros")
        
        # inicia o servidor da api
        await self.servidor_api.start()
    
    async def close(self) -> None:
        # finaliza o servidor da api
        await self.servidor_api.finalizar()
        
        await super().close()
        

def criar_bot() -> RayquazaBot:
    intents = discord.Intents.all()
    intents.message_content = True
    
    return RayquazaBot(
        command_prefix=configuracoes.command_prefix,
        intents=intents,
        help_command=None
    )