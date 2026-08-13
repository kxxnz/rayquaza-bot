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