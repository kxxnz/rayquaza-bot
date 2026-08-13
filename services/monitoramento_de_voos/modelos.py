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