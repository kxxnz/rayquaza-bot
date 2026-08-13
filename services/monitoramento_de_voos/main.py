import asyncio
import logging

from services.monitoramento_de_voos.cliente_serpapi import ClienteSerpApi
from services.monitoramento_de_voos.config import configuracoes
from services.monitoramento_de_voos.monitor import MonitoramentoDeVoos
from services.monitoramento_de_voos.notificador import NotificadorRayquaza
from services.monitoramento_de_voos.scheduler import FlightMonitorWorker


def configurar_logs() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


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

    monitoramento = MonitoramentoDeVoos(
        configuracoes=configuracoes,
        cliente=cliente,
        notificador=notificador,
    )

    worker = FlightMonitorWorker(
        configuracoes=configuracoes,
        monitoramento=monitoramento,
    )

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