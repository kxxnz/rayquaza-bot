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

        return OfertaVoo(
            origem=partida.get(
                "id",
                self.configuracoes.aeroporto_origem,
            ),
            destino=chegada.get(
                "id",
                self.configuracoes.aeroporto_destino,
            ),
            horario_saida=partida.get("time", "não informado"),
            horario_chegada=chegada.get("time", "não informado"),
            companhia=primeiro_trecho.get("airline", "não informado"),
            numero_voo=primeiro_trecho.get(
                "flight_number",
                "não informado",
            ),
            preco=float(preco),
            moeda=self.configuracoes.moeda,
            duracao_minutos=resultado.get("total_duration", 0),
            quantidade_escalas=len(trechos) - 1,
            link=link,
        )
        
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
