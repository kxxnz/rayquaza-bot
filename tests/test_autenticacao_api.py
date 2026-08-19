import unittest

from app.api.autenticacao import validar_autorizacao


class TestAutenticacaoAPI(unittest.TestCase):
    API_TOKEN = "token-correto"

    def test_deve_autorizar_token_correto(self) -> None:
        autorizado = validar_autorizacao("Bearer token-correto", self.API_TOKEN)

        self.assertTrue(autorizado)

    def test_deve_recusar_cabecalho_ausente(self) -> None:
        autorizado = validar_autorizacao(None, self.API_TOKEN)

        self.assertFalse(autorizado)

    def test_deve_recusar_token_incorreto(self) -> None:
        autorizado = validar_autorizacao("Bearer token-incorreto", self.API_TOKEN)

        self.assertFalse(autorizado)

    def test_deve_recusar_esquema_incorreto(self) -> None:
        autorizado = validar_autorizacao("Basic abc123", self.API_TOKEN)

        self.assertFalse(autorizado)

    def test_deve_recusar_bearer_sem_token(self) -> None:
        autorizado = validar_autorizacao("Bearer", self.API_TOKEN)

        self.assertFalse(autorizado)

    def test_deve_aceitar_espacos_extras(self) -> None:
        autorizado = validar_autorizacao("Bearer    token-correto", self.API_TOKEN)

        self.assertTrue(autorizado)

    def test_deve_recusar_cabecalho_malformado(self) -> None:
        autorizado = validar_autorizacao("Bearer token-correto extra", self.API_TOKEN)

        self.assertFalse(autorizado)


if __name__ == "__main__":
    unittest.main()
