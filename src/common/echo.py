"""Módulo para saída personalizada no terminal com símbolos e cores ANSI.

Fornece funções utilitárias para exibir mensagens estilizadas conforme o tipo de informação
(informativo, erro, sucesso, etc.). Ajusta automaticamente a saída para ambientes interativos
e não interativos, removendo códigos ANSI quando necessário.
"""

import re
import sys


class Echo:
    """Classe para saída personalizada no terminal com símbolos e cores ANSI."""

    # Constantes para formatação de texto
    _RESET = "\033[0m"
    _BOLD = "\033[1m"
    _BLUE = "\033[34m"
    _RED = "\033[31m"
    _YELLOW = "\033[33m"
    _GREEN = "\033[32m"
    _CYAN = "\033[36m"
    _MAGENTA = "\033[35m"

    # Símbolos para os tipos de mensagem
    _INFO_SYMBOL = f"{_BOLD}{_BLUE}i{_RESET}"
    _ERROR_SYMBOL = f"{_BOLD}{_RED}✖{_RESET}"
    _WARN_SYMBOL = f"{_BOLD}{_YELLOW}!{_RESET}"
    _SUCCESS_SYMBOL = f"{_BOLD}{_GREEN}✔{_RESET}"
    _WAIT_SYMBOL = f"{_BOLD}{_CYAN}…{_RESET}"
    _ARROW_SYMBOL = f"{_BOLD}{_BLUE}➔{_RESET}"
    _BULLET_SYMBOL = f"{_BOLD}{_CYAN}•{_RESET}"
    _STAR_SYMBOL = f"{_BOLD}{_YELLOW}★{_RESET}"
    _PROGRESS_SYMBOL = f"{_BOLD}{_CYAN}>{_RESET}"
    _TIME_SYMBOL = f"{_BOLD}{_BLUE}⧗{_RESET}"
    _FLAG_SYMBOL = f"{_BOLD}{_RED}⚑{_RESET}"
    _LINK_SYMBOL = f"{_BOLD}{_YELLOW}↗{_RESET}"
    _DASH_SYMBOL = f"{_BOLD}{_CYAN}–{_RESET}"

    def __init__(self) -> None:
        """Inicializa a classe Echo."""
        self._SYMBOL_MAP: dict[str, str] = {
            "info": self._INFO_SYMBOL,
            "error": self._ERROR_SYMBOL,
            "warn": self._WARN_SYMBOL,
            "success": self._SUCCESS_SYMBOL,
            "wait": self._WAIT_SYMBOL,
            "arrow": self._ARROW_SYMBOL,
            "bullet": self._BULLET_SYMBOL,
            "star": self._STAR_SYMBOL,
            "progress": self._PROGRESS_SYMBOL,
            "time": self._TIME_SYMBOL,
            "flag": self._FLAG_SYMBOL,
            "link": self._LINK_SYMBOL,
            "dash": self._DASH_SYMBOL,
            "blank": " ",
        }
        self._error = f"{self._BOLD}{self._RED}X{self._RESET}"
        """Símbolo de erro para mensagens de fallback."""

        self._ANSI_ESCAPE: re.Pattern[str] = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        """Mapeia tipos de mensagens para símbolos correspondentes."""

        self._enabled: bool = True
        """Indica se o echo está ativo ou não."""

    def is_interactive_terminal(self) -> bool:
        """Retorna True se a saída padrão for um terminal interativo."""
        return hasattr(sys, "stdout") and hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    def echo(self, message: str, message_type: str = "info") -> None:
        """Formata e imprime mensagem estilizada no terminal, ou faz fallback para print."""
        if not self._enabled:
            print(message)
            return

        try:
            symbol = self._SYMBOL_MAP.get(message_type.lower())
            if symbol is None:
                print(f"{self._error} [ECHO-ERRO] Tipo de mensagem inválido: {message_type}")
                symbol = self._INFO_SYMBOL

            formatted_message = f"{symbol} {message}"

            if self.is_interactive_terminal():
                print(formatted_message)
            else:
                print(self._ANSI_ESCAPE.sub("", formatted_message))

        except Exception as e:  # noqa: BLE001
            print(
                f"{self._error} [ECHO-DESATIVADO] Falha detectada: {e}. "
                f"Futuras chamadas usarão `print()`."
            )
            self._enabled = False
            print(message)

    def echo_list(self, *, as_list: bool = False) -> None:
        """Lista todos os tipos de mensagens disponíveis usando a instância padrão de Echo."""
        if as_list:
            items = [
                f"{self._SYMBOL_MAP[message_type]} {message_type}"
                for message_type in self._SYMBOL_MAP
            ]
            if self.is_interactive_terminal():
                print(", ".join(items))
            else:
                print(", ".join(self._ANSI_ESCAPE.sub("", item) for item in items))
        else:
            for message_type in self._SYMBOL_MAP:
                self.echo(message_type, message_type)

    def reset(self) -> None:
        """Reativa a saída estilizada após falha."""
        self._enabled = True


_default_echo = Echo()
"""Instância padrão de Echo para uso global."""


def echo(message: str, message_type: str = "info") -> None:
    """Imprime mensagem estilizada no terminal usando a instância padrão de Echo."""
    try:
        _default_echo.echo(message, message_type)
    except Exception as e:  # noqa: BLE001
        print(f"[ECHO-ERRO] Falha detectada: {e}. Futuras chamadas usarão `print()`.")


def echo_list(*, as_list: bool = False) -> None:
    """Lista todos os tipos de mensagens disponíveis usando a instância padrão de Echo."""
    _default_echo.echo_list(as_list=as_list)


def _validate_echo_attribute_error() -> None:
    """Força a funcionalidade de erro do Echo, provocando um AttributeError."""
    del _default_echo._SYMBOL_MAP  # noqa: SLF001
    echo("Esta mensagem de teste recebeu um fallback com 'print()'.")


if __name__ == "__main__":
    print("> Testando a função 'echo_list()' como lista horizontal:")
    echo_list(as_list=True)
    print("\n> Testando a função 'echo_list()' como lista vertical:")
    echo_list()
    print("\n> Testando a função '_validate_echo_attribute_error()':")
    _validate_echo_attribute_error()
