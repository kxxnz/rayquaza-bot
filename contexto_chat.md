# Contexto do projeto

**Projeto:** `rayquaza-bot`
**Diretorio raiz:** `E:\Scripts\rayquaza-bot`
**Parte:** `1/1`
**Arquivos nesta parte:** `37`

> Arquivo gerado automaticamente para uso como contexto do projeto.

## Sumario

- `.dockerignore`
- `.env.example`
- `.github/workflows/pipeline-docker.yml`
- `.gitignore`
- `.vscode/settings.json`
- `app/__init__.py`
- `app/api/__init__.py`
- `app/api/server.py`
- `app/bot.py`
- `app/commands/__init__.py`
- `app/commands/general.py`
- `app/commands/tickets.py`
- `app/config.py`
- `app/events/__init__.py`
- `app/events/membros.py`
- `app/events/ready.py`
- `app/notifications/__init__.py`
- `app/notifications/promocoes_de_voo.py`
- `app/tickets/painel.py`
- `app/tickets/servico.py`
- `compose.yml`
- `deploy/deploy.sh`
- `deploy/rayquaza-deploy.service`
- `deploy/rayquaza-deploy.timer`
- `Dockerfile`
- `LICENSE`
- `main.py`
- `README.md`
- `requirements.txt`
- `services/monitoramento_de_voos/__init__.py`
- `services/monitoramento_de_voos/cliente_serpapi.py`
- `services/monitoramento_de_voos/config.py`
- `services/monitoramento_de_voos/main.py`
- `services/monitoramento_de_voos/modelos.py`
- `services/monitoramento_de_voos/monitor.py`
- `services/monitoramento_de_voos/notificador.py`
- `services/monitoramento_de_voos/scheduler.py`

---

## `.dockerignore`

**Caminho relativo:** `.dockerignore`

```text
.git
.github
.vscode

.env
.env.*
!.env.example

.venv
venv

__pycache__
*.pyc
*.pyo
.pytest_cache

README.md
LICENSE
```

---

## `.env.example`

**Caminho relativo:** `.env.example`

```text
BOT_TOKEN=

API_HOST=127.0.0.1
API_PORT=8080
API_TOKEN=

CANAL_DE_PROMOCOES_DE_VOO=
TICKET_PANEL_CHANNEL_ID=
TICKET_CATEGORY_ID=

SERPAPI_KEY=

RAYQUAZA_API_URL=

VOO_AEROPORTO_ORIGEM=
VOO_AEROPORTO_DESTINO=
VOO_DATA_IDA=
VOO_DATA_VOLTA=
VOO_PRECO_MAXIMO=
VOO_MOEDA=

VOO_INTERVALO_MINUTOS=
VOO_MAX_RETRIES=
VOO_TIMEOUT_CICLO_SEGUNDOS=
```

---

## `.github/workflows/pipeline-docker.yml`

**Caminho relativo:** `.github/workflows/pipeline-docker.yml`

```yaml
name: Pipeline Docker

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: pipeline-docker-${{ github.ref }}
  cancel-in-progress: true

jobs:
  validar:
    name: Validar aplicacao
    runs-on: ubuntu-latest

    steps:
      - name: Baixar codigo
        uses: actions/checkout@v6

      - name: Configurar Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.13"
          cache: pip

      - name: Instalar dependencias
        run: pip install -r requirements.txt

      - name: Validar sintaxe
        run: python -m compileall app services main.py

  publicar-imagem:
    name: Publicar imagem linux 386
    if: github.event_name != 'pull_request'
    needs: validar
    runs-on: ubuntu-latest

    steps:
      - name: Baixar codigo
        uses: actions/checkout@v6

      - name: Configurar QEMU
        uses: docker/setup-qemu-action@v4
        with:
          platforms: 386

      - name: Configurar Buildx
        uses: docker/setup-buildx-action@v4

      - name: Entrar no Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Gerar metadados da imagem
        id: meta
        uses: docker/metadata-action@v6
        with:
          images: ${{ secrets.DOCKERHUB_USERNAME }}/rayquaza-bot
          tags: |
            type=raw,value=latest
            type=sha,prefix=sha-

      - name: Gerar e publicar imagem
        uses: docker/build-push-action@v7
        with:
          context: .
          file: ./Dockerfile
          platforms: linux/386
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Baixar imagem publicada
        run: |
          docker pull --platform linux/386 ${{ secrets.DOCKERHUB_USERNAME }}/rayquaza-bot:latest

      - name: Validar arquitetura da imagem
        run: |
          ARQUITETURA=$(docker image inspect             ${{ secrets.DOCKERHUB_USERNAME }}/rayquaza-bot:latest             --format '{{.Os}}/{{.Architecture}}')

          echo "Arquitetura encontrada: ${ARQUITETURA}"

          if [ "${ARQUITETURA}" != "linux/386" ]; then
            echo "A imagem nao foi gerada para linux/386."
            exit 1
          fi

      - name: Validar Python 32 bits
        run: |
          BITS=$(docker run --rm             --platform linux/386             ${{ secrets.DOCKERHUB_USERNAME }}/rayquaza-bot:latest             python -c "import struct; print(struct.calcsize('P') * 8)")

          echo "Python encontrado: ${BITS} bits"

          if [ "${BITS}" != "32" ]; then
            echo "O Python nao esta executando em 32 bits."
            exit 1
          fi

      - name: Validar dependencias da imagem
        run: |
          docker run --rm             --platform linux/386             ${{ secrets.DOCKERHUB_USERNAME }}/rayquaza-bot:latest             python -c "import discord, aiohttp, dotenv; print('Dependencias carregadas com sucesso')"
```

---

## `.gitignore`

**Caminho relativo:** `.gitignore`

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[codz]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#   Usually these files are written by a python script from a template
#   before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py.cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
# Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
# uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
# poetry.lock
# poetry.toml

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#   pdm recommends including project-wide configuration in pdm.toml, but excluding .pdm-python.
#   https://pdm-project.org/en/latest/usage/project/#working-with-version-control
# pdm.lock
# pdm.toml
.pdm-python
.pdm-build/

# pixi
#   Similar to Pipfile.lock, it is generally recommended to include pixi.lock in version control.
# pixi.lock
#   Pixi creates a virtual environment in the .pixi directory, just like venv module creates one
#   in the .venv directory. It is recommended not to include this directory in version control.
.pixi

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# Redis
*.rdb
*.aof
*.pid

# RabbitMQ
mnesia/
rabbitmq/
rabbitmq-data/

# ActiveMQ
activemq-data/

# SageMath parsed files
*.sage.py

# Environments
.env
.envrc
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#   JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#   be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#   and can be added to the global gitignore or merged into this file.  For a more nuclear
#   option (not recommended) you can uncomment the following to ignore the entire idea folder.
# .idea/

# Abstra
#   Abstra is an AI-powered process automation framework.
#   Ignore directories containing user credentials, local state, and settings.
#   Learn more at https://abstra.io/docs
.abstra/

# Visual Studio Code
#   Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore 
#   that can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#   and can be added to the global gitignore or merged into this file. However, if you prefer, 
#   you could uncomment the following to ignore the entire vscode folder
# .vscode/
# Temporary file for partial code execution
tempCodeRunnerFile.py

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Marimo
marimo/_static/
marimo/_lsp/
__marimo__/

# Streamlit
.streamlit/secrets.toml
```

---

## `.vscode/settings.json`

**Caminho relativo:** `.vscode/settings.json`

```json
{
    "python-envs.defaultEnvManager": "ms-python.python:venv"
}
```

---

## `app/__init__.py`

**Caminho relativo:** `app/__init__.py`

```python
[arquivo vazio]
```

---

## `app/api/__init__.py`

**Caminho relativo:** `app/api/__init__.py`

```python
[arquivo vazio]
```

---

## `app/api/server.py`

**Caminho relativo:** `app/api/server.py`

```python
import logging
from typing import Any

import discord
from aiohttp import web
from discord.ext import commands
from app.notifications.promocoes_de_voo import PromocaoDeVoo, criar_embed_promocao_de_voo


logger = logging.getLogger(__name__)


class RayquazaAPI:
    def __init__(self, bot: commands.Bot, host: str, port: int, notification_channel_id: int) -> None:
        self.bot = bot
        self.host = host
        self.port = port
        self.notification_channel_id = notification_channel_id
        
        self.runner: web.AppRunner | None = None
        self.site: web.TCPSite | None = None
        
    async def start(self) -> None:
        app = web.Application()
        
        app.router.add_get("/health", self.verificar_saude)
        app.router.add_post("/notificacoes/teste", self.enviar_noticacao_de_teste)
        app.router.add_post("/notificacoes/promocoes-de-voo", self.enviar_promocao_de_voo)
        
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        
        self.site = web.TCPSite(self.runner, self.host, self.port)
        await self.site.start()
        
        logger.info(f"API do Rayquaza iniciada em http://{self.host}:{self.port}")
        
    async def finalizar(self) -> None:
        if self.runner is None:
            return
        
        await self.runner.cleanup()
        
        self.runner = None
        self.site = None
        
        logger.info("API do Rayquaza finalizada.")
        
    async def verificar_saude(self, request: web.Request) -> web.Response:
        return web.json_response({"status": "online", "servico": "rayquaza-bot"})
    
    async def enviar_noticacao_de_teste(self, request: web.Request) -> web.Response:
        try:
            dados = await request.json()
        except (ValueError, TypeError):
            return web.json_response({"erro": "tem q ser um json valido."}, status=400)
        
        mensagem = self.obter_mensagem(dados)
        
        if mensagem is None:
            return web.json_response({"erro": "o campo mensagem eh obrigatorio e tem q conter entre 1 e 2000 caracteres."}, status=400)
        
        try:
            canal = await self.obter_canal()
        except discord.DiscordException:
            logger.exception("nao foi possivel localizar o canal | canal_id=%s", self.notification_channel_id)
            
            return web.json_response({"erro": "nao foi possivel localizar o canal de notificacoes."}, status=500)
        
        if canal is None or not hasattr(canal, "send"):
            logger.error("o canal de notificacoes nao eh valido para enviar mensagens | canal_id=%s", self.notification_channel_id)
            
            return web.json_response({"erro": "o canal configurado nao aceita mensagens."}, status=500)
        
        try: 
            await canal.send(mensagem)
        except discord.DiscordException:
            logger.exception("erro ao enviar notificacao | canal_id=%s", self.notification_channel_id)
            
            return web.json_response({"erro": "nao foi possível enviar a mensagem ao discord."}, status=500)
        
        logger.info("notificacao enviada com sucesso | canal_id=%s", self.notification_channel_id)
        
        return web.json_response({"status": "notificacao enviada com sucesso.", "canal_id": self.notification_channel_id})
    
    async def enviar_promocao_de_voo(self, request: web.Request) -> web.Response:
        try:
            dados = await request.json()
            
            promocao = PromocaoDeVoo(origem=dados["origem"],
                                     destino=dados["destino"],
                                     preco=float(dados["preco"]),
                                     moeda=dados["moeda"],
                                     companhia=dados["companhia"],
                                     numero_voo=dados["numero_voo"],
                                     quantidade_escalas=int(dados["quantidade_escalas"]),
                                     duracao_minutos=int(dados["duracao_minutos"]),
                                     horario_chegada=dados["horario_chegada"],
                                     horario_saida=dados["horario_saida"],
                                     link=dados["link"])
        except (KeyError, TypeError, ValueError):
            return web.json_response({"erro": "os dados de promocao de voo sao invalidos ou estao incompletos"}, status = 400)
        
        canal = await self.obter_canal()
        
        if canal is None or not hasattr(canal, "send"):
            logger.error("o canal de notificacoes nao eh valido | canal_id %s", self.notification_channel_id)
            
            return web.json_response({"erro": "o canal configurado nao aceita mensagens"}, status = 500)
        
        embed = criar_embed_promocao_de_voo(promocao)
        
        try:
            await canal.send(embed=embed)
        except discord.DiscordException:
            logger.exception("erro ao enviar promocao de voo | canal_id=%s", self.notification_channel_id)
            
            return web.json_response({"erro": "nao foi possivel enviar a promocao ao discord"}, status = 500)
        
        logger.info("promocao de voo enviada com sucesso | rota=%s-%s | preco=%.2f | canal_id=%s", promocao.origem, promocao.destino, promocao.preco, self.notification_channel_id)
        
        return web.json_response({"status": "promocao de voo enviada com sucesso.", "canal_id": self.notification_channel_id})
    
    def obter_mensagem(self, dados: dict[str, Any]) -> str | None:
        if not isinstance(dados, dict):
            return None
        
        mensagem = dados.get("mensagem")
        
        if not isinstance(mensagem, str) or not (1 <= len(mensagem) <= 2000):
            return None
        
        return mensagem
    
    async def obter_canal(self) -> discord.abc.Messageable | None:
        canal = self.bot.get_channel(self.notification_channel_id)
        
        if canal is None:
            try:
                canal = await self.bot.fetch_channel(self.notification_channel_id)
            except discord.DiscordException:
                logger.exception("erro ao buscar o canal de notificacoes | canal_id=%s", self.notification_channel_id)
                return None
        
        return canal
```

---

## `app/bot.py`

**Caminho relativo:** `app/bot.py`

```python
import discord
from discord.ext import commands

from app.config import configuracoes
from app.api.server import RayquazaAPI
from app.tickets.painel import PainelTickets


class RayquazaBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.servidor_api = RayquazaAPI(bot=self,
                                        host=configuracoes.api_host,
                                        port=configuracoes.api_port,
                                        notification_channel_id=configuracoes.notification_channel_id)
    
    async def setup_hook(self) -> None:
        # carregar as extensões do bot
        await self.load_extension("app.commands.general")
        await self.load_extension("app.commands.tickets")
        await self.load_extension("app.events.ready")
        await self.load_extension("app.events.membros")
        
        self.add_view(PainelTickets())
        
        # inicia o servidor da api
        await self.servidor_api.start()
    
    async def close(self) -> None:
        # finaliza o servidor da api
        await self.servidor_api.finalizar()
        
        await super().close()
        

def criar_bot() -> RayquazaBot:
    intents = discord.Intents.all()
    intents.message_content = True
    
    return RayquazaBot(command_prefix=configuracoes.command_prefix,
                       intents=intents,
                       help_command=None)
```

---

## `app/commands/__init__.py`

**Caminho relativo:** `app/commands/__init__.py`

```python
[arquivo vazio]
```

---

## `app/commands/general.py`

**Caminho relativo:** `app/commands/general.py`

```python
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
    async def pfp(self, contexto: commands.Context, usuario_informado: str | None = None) -> None:
        usuario = contexto.author
        
        if usuario_informado:
            usuario = await self.buscar_usuario(contexto, usuario_informado)
        
            if usuario is None:
                await contexto.reply("Não foi possível encontrar esse usuário.", mention_author=False,)
                return
        
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


    async def buscar_usuario(self, contexto: commands.Context, valor: str) -> discord.User | discord.Member | None:
        try:
            return await commands.MemberConverter().convert(contexto, valor)
        except commands.MemberNotFound:
            pass

        usuario_id = valor.replace("<@", "").replace("!", "").replace(">", "")

        if not usuario_id.isdigit():
            return None

        try:
            return await self.bot.fetch_user(int(usuario_id))
        except (discord.NotFound, discord.HTTPException):
            return None

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ComandosGerais(bot))
```

---

## `app/commands/tickets.py`

**Caminho relativo:** `app/commands/tickets.py`

```python
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
```

---

## `app/config.py`

**Caminho relativo:** `app/config.py`

```python
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
    notification_channel_id: int
    ticket_panel_channel_id: int
    ticket_category_id: int
    

def carregar_as_configuracoes() -> Configuracoes:
    bot_token = os.getenv("BOT_TOKEN")
    api_host = os.getenv("API_HOST")
    api_port = int(os.getenv("API_PORT"))
    notification_channel_id = int(os.getenv("CANAL_DE_PROMOCOES_DE_VOO"))
    ticket_panel_channel_id = int(os.getenv("TICKET_PANEL_CHANNEL_ID"))
    ticket_category_id = int(os.getenv("TICKET_CATEGORY_ID"))

    if not bot_token:
        raise ValueError("O token do bot nao foi configurado/encontrado.")
    if not api_host:
        raise ValueError("O host da API nao foi configurado/encontrado.")
    if not api_port:
        raise ValueError("A porta da API nao foi configurada/encontrada.")
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
                         notification_channel_id=notification_channel_id,
                         ticket_category_id=ticket_category_id,
                         ticket_panel_channel_id=ticket_panel_channel_id)


configuracoes = carregar_as_configuracoes()
```

---

## `app/events/__init__.py`

**Caminho relativo:** `app/events/__init__.py`

```python
[arquivo vazio]
```

---

## `app/events/membros.py`

**Caminho relativo:** `app/events/membros.py`

```python
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
```

---

## `app/events/ready.py`

**Caminho relativo:** `app/events/ready.py`

```python
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
            
            await contexto.reply("Esse comando não existe.")
            
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
```

---

## `app/notifications/__init__.py`

**Caminho relativo:** `app/notifications/__init__.py`

```python
[arquivo vazio]
```

---

## `app/notifications/promocoes_de_voo.py`

**Caminho relativo:** `app/notifications/promocoes_de_voo.py`

```python
from dataclasses import dataclass
from datetime import datetime

import discord


@dataclass(frozen=True)
class PromocaoDeVoo:
    origem: str
    destino: str
    preco: float
    moeda: str
    companhia: str
    numero_voo: str
    quantidade_escalas: int
    duracao_minutos: int
    horario_saida: str
    horario_chegada: str
    link: str


def criar_embed_promocao_de_voo(promocao: PromocaoDeVoo,) -> discord.Embed:
    embed = discord.Embed(
        title="✈️ Promoção de voo encontrada",
        description=(
            f"## {promocao.origem} → {promocao.destino}\n"
            f"Passagem encontrada por **{formatar_preco(promocao)}**"
        ),
        color=discord.Color.green(),
        timestamp=datetime.now(),
    )

    embed.add_field(name="Companhia", value=promocao.companhia, inline=True,)
    embed.add_field(name="Voo", value=promocao.numero_voo, inline=True,)
    embed.add_field(name="Escalas",value=formatar_escalas(promocao.quantidade_escalas),inline=True,)
    embed.add_field(name="Saída",value=formatar_data_hora(promocao.horario_saida),inline=True,)
    embed.add_field(name="Chegada",value=formatar_data_hora(promocao.horario_chegada),inline=True,)
    embed.add_field(name="Duração",value=formatar_duracao(promocao.duracao_minutos),inline=True,)
    embed.add_field(name="Comprar passagem", value=f"{promocao.link}", inline=False)
    embed.set_footer(text=("O preço pode mudar. ""Confirme a tarifa antes da compra."))

    return embed


def formatar_preco(promocao: PromocaoDeVoo,) -> str:
    preco_formatado = f"{promocao.preco:,.2f}"

    preco_formatado = (preco_formatado.replace(",", "TEMP").replace(".", ",").replace("TEMP", "."))

    if promocao.moeda.upper() == "BRL":
        return f"R$ {preco_formatado}"

    return f"{promocao.moeda.upper()} {preco_formatado}"


def formatar_duracao(duracao_minutos: int) -> str:
    if duracao_minutos <= 0:
        return "Não informada"

    horas, minutos = divmod(duracao_minutos,60)

    if horas == 0:
        return f"{minutos}min"

    if minutos == 0:
        return f"{horas}h"

    return f"{horas}h {minutos:02d}min"


def formatar_escalas(quantidade_escalas: int) -> str:
    if quantidade_escalas <= 0:
        return "Direto"

    if quantidade_escalas == 1:
        return "1 escala"

    return f"{quantidade_escalas} escalas"


def formatar_data_hora(data_hora: str) -> str:
    formatos_aceitos = (
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
    )

    for formato in formatos_aceitos:
        try:
            data_convertida = datetime.strptime(data_hora, formato)

            return data_convertida.strftime("%d/%m/%Y às %H:%M")
        except ValueError:
            continue

    return data_hora or "Não informado"
```

---

## `app/tickets/painel.py`

**Caminho relativo:** `app/tickets/painel.py`

```python
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
```

---

## `app/tickets/servico.py`

**Caminho relativo:** `app/tickets/servico.py`

```python
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
```

---

## `compose.yml`

**Caminho relativo:** `compose.yml`

```yaml
services:
  rayquaza-bot:
    image: jpwrlld/rayquaza-bot:${IMAGE_TAG:-latest}
    container_name: rayquaza-bot
    platform: linux/386
    restart: unless-stopped
    env_file:
      - .env
    environment:
      API_HOST: 0.0.0.0
      API_PORT: 8080
    ports:
      - "3001:8080"
    healthcheck:
      test:
        - CMD
        - python
        - -c
        - "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=5)"
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s
    networks:
      - rayquaza-network

  monitoramento-de-voos:
    image: jpwrlld/rayquaza-bot:${IMAGE_TAG:-latest}
    container_name: monitoramento-de-voos
    platform: linux/386
    restart: unless-stopped
    command: python -m services.monitoramento_de_voos.main
    env_file:
      - .env
    environment:
      RAYQUAZA_API_URL: http://rayquaza-bot:8080
    depends_on:
      rayquaza-bot:
        condition: service_healthy
    networks:
      - rayquaza-network

networks:
  rayquaza-network:
    name: rayquaza-network
```

---

## `deploy/deploy.sh`

**Caminho relativo:** `deploy/deploy.sh`

```bash
#!/bin/sh

set -eu

DIRETORIO_PROJETO="/opt/rayquaza-bot"

printf '%s
'     ""     "===================================="     "Iniciando deploy do Rayquaza"     "===================================="

cd "$DIRETORIO_PROJETO"

printf '%s
' "Baixando imagens atualizadas..."
docker compose pull

printf '%s
' "Atualizando containers..."
docker compose up -d --remove-orphans

printf '%s
' "Validando containers..."
docker compose ps

printf '%s
'     ""     "===================================="     "Deploy do Rayquaza finalizado"     "===================================="
```

---

## `deploy/rayquaza-deploy.service`

**Caminho relativo:** `deploy/rayquaza-deploy.service`

```text
[Unit]
Description=Atualiza os containers do Rayquaza
Requires=docker.service
After=docker.service network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=joao
Group=docker
WorkingDirectory=/opt/rayquaza-bot
ExecStart=/opt/rayquaza-bot/deploy.sh
TimeoutStartSec=10min
```

---

## `deploy/rayquaza-deploy.timer`

**Caminho relativo:** `deploy/rayquaza-deploy.timer`

```text
[Unit]
Description=Verifica atualizacoes do Rayquaza

[Timer]
OnActiveSec=1min
OnUnitInactiveSec=5min
Unit=rayquaza-deploy.service

[Install]
WantedBy=timers.target
```

---

## `Dockerfile`

**Caminho relativo:** `Dockerfile`

```dockerfile
FROM python:3.13-slim-bookworm AS builder

ENV PIP_NO_CACHE_DIR=1
ENV SODIUM_INSTALL=system

WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        build-essential \
        libffi-dev \
        libsodium-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt


FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        libffi8 \
        libsodium23 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

COPY app ./app
COPY services ./services
COPY main.py .

RUN useradd --create-home --uid 10001 rayquaza \
    && chown -R rayquaza:rayquaza /app

USER rayquaza

CMD ["python", "main.py"]
```

---

## `LICENSE`

**Caminho relativo:** `LICENSE`

```text
MIT License

Copyright (c) 2026 João Pedro Cavalheiro dos Reis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## `main.py`

**Caminho relativo:** `main.py`

```python
import logging

from app.bot import criar_bot
from app.config import configuracoes


def configurar_logging() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")


def main() -> None:
    configurar_logging()
    
    bot = criar_bot()
    bot.run(configuracoes.bot_token)
    

if __name__ == "__main__":
    main()
```

---

## `README.md`

**Caminho relativo:** `README.md`

```markdown
# rayquaza-bot
Bot para Discord focado em automações, integrações e aprendizado com microsserviços.
```

---

## `requirements.txt`

**Caminho relativo:** `requirements.txt`

```text
discord.py
requests
dotenv
aiohttp
pyNaCl
davey
```

---

## `services/monitoramento_de_voos/__init__.py`

**Caminho relativo:** `services/monitoramento_de_voos/__init__.py`

```python
[arquivo vazio]
```

---

## `services/monitoramento_de_voos/cliente_serpapi.py`

**Caminho relativo:** `services/monitoramento_de_voos/cliente_serpapi.py`

```python
import asyncio
import logging
from typing import Any

import aiohttp

from services.monitoramento_de_voos.config import ConfiguracoesMonitoramento
from services.monitoramento_de_voos.modelos import OfertaVoo
from urllib.parse import quote


logger = logging.getLogger(__name__)


class ClienteSerpApi:
    URL = "https://serpapi.com/search.json"

    def __init__(self, configuracoes: ConfiguracoesMonitoramento) -> None:
        self.configuracoes = configuracoes

    async def buscar_ofertas(self) -> list[OfertaVoo]:
        parametros = self._montar_parametros()

        for tentativa in range(self.configuracoes.max_retries + 1):
            try:
                timeout = aiohttp.ClientTimeout(total=60)

                async with aiohttp.ClientSession(timeout=timeout) as sessao:
                    async with sessao.get(
                        self.URL,
                        params=parametros,
                    ) as resposta:
                        dados = await resposta.json()

                        if resposta.status != 200:
                            erro = dados.get("error", "erro desconhecido")
                            raise RuntimeError(
                                f"Erro ao buscar ofertas: {erro}"
                            )

                ofertas = self._converter_ofertas(dados)

                logger.info(
                    "Consulta finalizada | origem=%s | destino=%s | ofertas=%d",
                    self.configuracoes.aeroporto_origem,
                    self.configuracoes.aeroporto_destino,
                    len(ofertas),
                )

                return ofertas

            except (asyncio.TimeoutError, aiohttp.ClientError) as erro:
                if tentativa >= self.configuracoes.max_retries:
                    logger.error(
                        "SerpApi falhou | tentativas=%d | erro=%s",
                        tentativa + 1,
                        type(erro).__name__,
                    )
                    raise

                espera = 2 ** tentativa

                logger.warning(
                    "Erro na SerpApi | tentativa=%d/%d | aguardando=%ds | erro=%s",
                    tentativa + 1,
                    self.configuracoes.max_retries + 1,
                    espera,
                    type(erro).__name__,
                )

                await asyncio.sleep(espera)

    def _montar_parametros(self) -> dict[str, Any]:
        parametros = {
            "engine": "google_flights",
            "api_key": self.configuracoes.serpapi_key,
            "departure_id": self.configuracoes.aeroporto_origem,
            "arrival_id": self.configuracoes.aeroporto_destino,
            "outbound_date": self.configuracoes.data_ida,
            "currency": self.configuracoes.moeda,
            "hl": "pt",
            "gl": "br",
            "travel_class": "1",
        }

        if self.configuracoes.data_volta:
            parametros["type"] = "1"
            parametros["return_date"] = self.configuracoes.data_volta
        else:
            parametros["type"] = "2"

        return parametros

    def _converter_ofertas(self,dados: dict[str, Any]) -> list[OfertaVoo]:
        resultados = (
            dados.get("best_flights", [])
            + dados.get("other_flights", [])
        )

        ofertas = []

        for resultado in resultados:
            oferta = self._converter_oferta(resultado)

            if oferta:
                ofertas.append(oferta)

        return ofertas

    def _converter_oferta(self,resultado: dict[str, Any]) -> OfertaVoo | None:
        trechos = resultado.get("flights", [])
        preco = resultado.get("price")

        if not trechos or not isinstance(preco, (int, float)):
            return None

        primeiro_trecho = trechos[0]
        ultimo_trecho = trechos[-1]

        partida = primeiro_trecho.get("departure_airport", {})
        chegada = ultimo_trecho.get("arrival_airport", {})
        
        link = self._montar_link_google_flights()

        return OfertaVoo(origem=partida.get("id", self.configuracoes.aeroporto_origem),
                         destino=chegada.get("id", self.configuracoes.aeroporto_destino),
                         horario_saida=partida.get("time", "não informado"),
                         horario_chegada=chegada.get("time", "não informado"),
                         companhia=primeiro_trecho.get("airline", "não informado"),
                         numero_voo=primeiro_trecho.get("flight_number", "não informado"),
                         preco=float(preco),
                         moeda=self.configuracoes.moeda,
                         duracao_minutos=resultado.get("total_duration", 0),
                         quantidade_escalas=len(trechos) - 1,
                         link=link)
        
    def _montar_link_google_flights(self) -> str:
        origem = self.configuracoes.aeroporto_origem
        destino = self.configuracoes.aeroporto_destino
        data_ida = self.configuracoes.data_ida
        data_volta = self.configuracoes.data_volta
    
        if data_volta:
            pesquisa = (
                f"Google Flights {origem} para {destino} "
                f"{data_ida} {data_volta}"
            )
        else:
            pesquisa = (
                f"Google Flights {origem} para {destino} "
                f"{data_ida} somente ida"
            )
    
        return (
            "https://www.google.com/search?"
            f"q={quote(pesquisa)}"
        )
```

---

## `services/monitoramento_de_voos/config.py`

**Caminho relativo:** `services/monitoramento_de_voos/config.py`

```python
import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class ConfiguracoesMonitoramento:
    serpapi_key: str
    rayquaza_api_url: str
    aeroporto_origem: str
    aeroporto_destino: str
    data_ida: str
    data_volta: str | None
    preco_maximo: float
    moeda: str
    intervalo_minutos: int
    max_retries: int
    timeout_ciclo_segundos: int


def obter_variavel(nome: str) -> str:
    valor = os.getenv(nome)

    if not valor:
        raise ValueError(
            f"A variável de ambiente '{nome}' não foi configurada."
        )

    return valor


def obter_inteiro(nome: str, padrao: int) -> int:
    valor = os.getenv(nome)

    if valor is None:
        return padrao

    try:
        return int(valor)
    except ValueError:
        raise ValueError(
            f"A variável de ambiente '{nome}' deve ser um inteiro."
        )


def obter_float(nome: str) -> float:
    valor = obter_variavel(nome)

    try:
        return float(valor)
    except ValueError:
        raise ValueError(
            f"A variável de ambiente '{nome}' deve ser um número."
        )


def carregar_configuracoes() -> ConfiguracoesMonitoramento:
    return ConfiguracoesMonitoramento(serpapi_key=obter_variavel("SERPAPI_KEY"),
                                      rayquaza_api_url=obter_variavel("RAYQUAZA_API_URL"),
                                      aeroporto_origem=obter_variavel("VOO_AEROPORTO_ORIGEM"),
                                      aeroporto_destino=obter_variavel("VOO_AEROPORTO_DESTINO"),
                                      data_ida=obter_variavel("VOO_DATA_IDA"),
                                      data_volta=os.getenv("VOO_DATA_VOLTA"),
                                      preco_maximo=obter_float("VOO_PRECO_MAXIMO"),
                                      moeda=obter_variavel("VOO_MOEDA"),
                                      intervalo_minutos=obter_inteiro("VOO_INTERVALO_MINUTOS", 15),
                                      max_retries=obter_inteiro("VOO_MAX_RETRIES", 3),
                                      timeout_ciclo_segundos=obter_inteiro("VOO_TIMEOUT_CICLO_SEGUNDOS", 300,))


configuracoes = carregar_configuracoes()
```

---

## `services/monitoramento_de_voos/main.py`

**Caminho relativo:** `services/monitoramento_de_voos/main.py`

```python
import asyncio
import logging

from services.monitoramento_de_voos.cliente_serpapi import ClienteSerpApi
from services.monitoramento_de_voos.config import configuracoes
from services.monitoramento_de_voos.monitor import MonitoramentoDeVoos
from services.monitoramento_de_voos.notificador import NotificadorRayquaza
from services.monitoramento_de_voos.scheduler import FlightMonitorWorker


def configurar_logs() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")


async def executar() -> None:
    logger = logging.getLogger(__name__)

    print(
        """
====================================
Iniciando monitoramento de voos
====================================
"""
    )

    cliente = ClienteSerpApi(configuracoes)
    notificador = NotificadorRayquaza(configuracoes)

    monitoramento = MonitoramentoDeVoos(configuracoes=configuracoes,
                                        cliente=cliente,
                                        notificador=notificador)

    worker = FlightMonitorWorker(configuracoes=configuracoes, 
                                 monitoramento=monitoramento)

    try:
        await worker.start()
    except KeyboardInterrupt:
        logger.info("Monitoramento interrompido pelo usuário")
    finally:
        print(
            """
====================================
Monitoramento finalizado
====================================
"""
        )


def main() -> None:
    configurar_logs()

    try:
        asyncio.run(executar())
    except KeyboardInterrupt:
        logging.getLogger(__name__).info(
            "Monitoramento interrompido pelo usuário"
        )


if __name__ == "__main__":
    main()
```

---

## `services/monitoramento_de_voos/modelos.py`

**Caminho relativo:** `services/monitoramento_de_voos/modelos.py`

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class OfertaVoo:
    origem: str
    destino: str
    horario_saida: str
    horario_chegada: str
    companhia: str
    numero_voo: str
    preco: float
    moeda: str
    duracao_minutos: int
    quantidade_escalas: int
    link: str
```

---

## `services/monitoramento_de_voos/monitor.py`

**Caminho relativo:** `services/monitoramento_de_voos/monitor.py`

```python
import logging

from services.monitoramento_de_voos.cliente_serpapi import ClienteSerpApi
from services.monitoramento_de_voos.config import ConfiguracoesMonitoramento
from services.monitoramento_de_voos.notificador import NotificadorRayquaza


logger = logging.getLogger(__name__)


class MonitoramentoDeVoos:
    def __init__(
        self,
        configuracoes: ConfiguracoesMonitoramento,
        cliente: ClienteSerpApi,
        notificador: NotificadorRayquaza,
    ) -> None:
        self.configuracoes = configuracoes
        self.cliente = cliente
        self.notificador = notificador

    async def executar(self) -> None:
        logger.info(
            "Monitoramento iniciado | rota=%s-%s | limite=%s",
            self.configuracoes.aeroporto_origem,
            self.configuracoes.aeroporto_destino,
            self.configuracoes.preco_maximo,
        )

        ofertas = await self.cliente.buscar_ofertas()

        if not ofertas:
            logger.warning("Nenhuma oferta encontrada")
            return

        menor_oferta = min(ofertas, key=lambda oferta: oferta.preco)

        logger.info(
            "Menor preço encontrado | preco=%s | companhia=%s",
            menor_oferta.preco,
            menor_oferta.companhia,
        )

        if menor_oferta.preco > self.configuracoes.preco_maximo:
            logger.info(
                "Preço acima do limite | encontrado=%s | limite=%s",
                menor_oferta.preco,
                self.configuracoes.preco_maximo,
            )
            return

        await self.notificador.enviar_oferta(menor_oferta)
```

---

## `services/monitoramento_de_voos/notificador.py`

**Caminho relativo:** `services/monitoramento_de_voos/notificador.py`

```python
import asyncio
import logging

import aiohttp

from services.monitoramento_de_voos.config import ConfiguracoesMonitoramento
from services.monitoramento_de_voos.modelos import OfertaVoo


logger = logging.getLogger(__name__)


class NotificadorRayquaza:
    def __init__(self, configuracoes: ConfiguracoesMonitoramento) -> None:
        self.api_url = configuracoes.rayquaza_api_url.rstrip("/")
        self.max_retries = configuracoes.max_retries

    async def enviar_oferta(self, oferta: OfertaVoo) -> None:
        url = f"{self.api_url}/notificacoes/promocoes-de-voo"

        dados_oferta = {
            "origem": oferta.origem,
            "destino": oferta.destino,
            "preco": oferta.preco,
            "moeda": oferta.moeda,
            "companhia": oferta.companhia,
            "numero_voo": oferta.numero_voo,
            "quantidade_escalas": oferta.quantidade_escalas,
            "duracao_minutos": oferta.duracao_minutos,
            "horario_saida": oferta.horario_saida,
            "horario_chegada": oferta.horario_chegada,
            "link": oferta.link,
        }

        for tentativa in range(self.max_retries + 1):
            try:
                timeout = aiohttp.ClientTimeout(total=15)

                async with aiohttp.ClientSession(timeout=timeout) as sessao:
                    async with sessao.post(url,json=dados_oferta) as resposta:
                        dados = await resposta.json()

                        if resposta.status != 200:
                            erro = dados.get("erro", "erro desconhecido")

                            raise RuntimeError(f"Erro ao notificar o Rayquaza: {erro}")

                logger.info("Notificação enviada | rota=%s-%s", oferta.origem, oferta.destino)

                return

            except (asyncio.TimeoutError, aiohttp.ClientError) as erro:
                if tentativa >= self.max_retries:
                    logger.error("Notificação falhou | tentativas=%d | erro=%s", tentativa + 1, type(erro).__name__)
                    raise

                espera = 2 ** tentativa

                logger.warning("Erro ao notificar Rayquaza | tentativa=%d | aguardando=%ds | erro=%s", tentativa + 1, espera, type(erro).__name__,)

                await asyncio.sleep(espera)
```

---

## `services/monitoramento_de_voos/scheduler.py`

**Caminho relativo:** `services/monitoramento_de_voos/scheduler.py`

```python
import asyncio
import logging

from services.monitoramento_de_voos.config import ConfiguracoesMonitoramento
from services.monitoramento_de_voos.monitor import MonitoramentoDeVoos


logger = logging.getLogger(__name__)


class FlightMonitorWorker:
    def __init__(
        self,
        configuracoes: ConfiguracoesMonitoramento,
        monitoramento: MonitoramentoDeVoos,
    ) -> None:
        self.configuracoes = configuracoes
        self.monitoramento = monitoramento

    async def start(self) -> None:
        intervalo = self.configuracoes.intervalo_minutos * 60

        logger.info(
            "Worker iniciado | intervalo=%d min | timeout=%d s",
            self.configuracoes.intervalo_minutos,
            self.configuracoes.timeout_ciclo_segundos,
        )

        while True:
            try:
                await asyncio.wait_for(
                    self.monitoramento.executar(),
                    timeout=self.configuracoes.timeout_ciclo_segundos,
                )

            except asyncio.TimeoutError:
                logger.error(
                    "Monitoramento excedeu o timeout | timeout=%d s",
                    self.configuracoes.timeout_ciclo_segundos,
                )

            except Exception:
                logger.exception("Erro ao executar monitoramento")

            logger.info(
                "Próximo monitoramento em %d minutos",
                self.configuracoes.intervalo_minutos,
            )

            await asyncio.sleep(intervalo)
```
