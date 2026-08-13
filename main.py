import logging

from app.bot import criar_bot
from app.config import configuracoes


def configurar_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    configurar_logging()
    
    bot = criar_bot()
    bot.run(configuracoes.bot_token)
    

if __name__ == "__main__":
    main()