import logging
import secrets

from aiohttp import web


logger = logging.getLogger(__name__)


def validar_autorizacao(cabecalho: str | None, api_token: str) -> bool:
    if not cabecalho:
        return False

    partes = cabecalho.split()

    if len(partes) != 2 or partes[0].lower() != "bearer":
        return False

    return secrets.compare_digest(partes[1], api_token)


def criar_middleware_autenticacao(api_token: str):
    @web.middleware
    async def autenticar_requisicao(request: web.Request, handler):
        if not request.path.startswith("/notificacoes/"):
            return await handler(request)

        cabecalho = request.headers.get("Authorization")

        if validar_autorizacao(cabecalho, api_token):
            return await handler(request)

        logger.warning("Acesso nao autorizado | metodo=%s | caminho=%s | origem=%s", request.method, request.path, request.remote)

        return web.json_response(
            {"erro": "nao autorizado."},
            status=401,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return autenticar_requisicao
