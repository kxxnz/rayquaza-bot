from app.bot import criar_bot
from app.config import configuracoes


def main() -> None:
    bot = criar_bot()
    bot.run(configuracoes.bot_token)
    

if __name__ == "__main__":
    main()