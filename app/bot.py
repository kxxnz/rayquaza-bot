import discord
from discord.ext import commands

from app.config import configuracoes


class RayquazaBot(commands.Bot):
    async def setup_hook(self) -> None:
        # carregar as extensões do bot
        await self.load_extension("app.commands.general")
        await self.load_extension("app.events.ready")
        

def criar_bot() -> RayquazaBot:
    intents = discord.Intents.all()
    intents.message_content = True
    
    return RayquazaBot(
        command_prefix=configuracoes.command_prefix,
        intents=intents,
        help_command=None
    )