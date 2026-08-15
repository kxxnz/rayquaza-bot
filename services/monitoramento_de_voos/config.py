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