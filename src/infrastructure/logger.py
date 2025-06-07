"""Módulo de configuração e acesso ao logger singleton da aplicação."""

import json
import logging
from typing import Any, ClassVar, Optional
import warnings

import yaml

from src.common.base.base_class import BaseClass
from src.common.echo import echo
from src.common.errors.errors import LoggerError
from src.config.constants import SETTINGS_FILE
from src.config.constypes import LoggerDict, PathLike


class LoggerSingleton(BaseClass):
    """Singleton para gerenciamento centralizado de logging."""

    _instance: ClassVar[Optional["LoggerSingleton"]] = None
    """Instância única do LoggerSingleton."""

    _initialized: bool = False
    """Indica se o logger foi inicializado."""

    logger: logging.Logger | None = None
    """Logger configurado para uso na aplicação."""

    def __new__(cls) -> "LoggerSingleton":
        """Cria ou retorna a instância única da classe Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Inicializa a instância do logger se ainda não estiver inicializada."""
        if self._initialized:
            return

        config = config if config else self._load_config_from_yaml(SETTINGS_FILE)
        """Carrega a configuração do logger a partir de um dicionário ou arquivo YAML."""

        # Atribui as configurações do dicionário às variáveis da classe.
        self._assign_config(config)

        logger_instance = self._define_handlers()
        """Configura o logger com handlers para console e arquivo (opcional)."""

        self.logger = logger_instance
        """Armazena o logger configurado como atributo público."""

        # Compartilhe o logger no singleton
        LoggerSingleton.logger = logger_instance

        # Marque a instância como inicializada
        self._initialized = True

    def __getattr__(self, name: str) -> Any:
        """Delegar chamadas de métodos ao logger interno."""
        self._ensure_initialized()
        if hasattr(self.logger, name):
            return getattr(self.logger, name)
        msg = f"Objeto '{type(self).__name__}' não possui o atributo '{name}'"
        raise AttributeError(msg)

    def _ensure_initialized(self) -> None:
        """Garante que o logger está inicializado."""
        if not self._initialized:
            self.__class__()  # Cria nova instância que será retornada pelo singleton

    def _raise_missing_keys(self, required_keys: set[str]) -> None:
        msg = f"Configuração inválida: chaves obrigatórias ausentes. Esperado: {required_keys}"
        echo(msg, "error")
        raise KeyError(msg)

    def _load_config_from_yaml(self, file_path: PathLike) -> LoggerDict:
        """Carrega a configuração do logger a partir do arquivo YAML ou a configuração padrão."""
        file_path = super()._ensure_path(file_path)
        if not file_path.is_file():
            echo(
                f"O arquivo de configuração {file_path} não foi encontrado. "
                "Usando configuração padrão.",
                "warn",
            )
            return self.get_default_config()
        try:
            echo(f"Carregando configuração de logging: '{file_path}'", "info")
            with file_path.open("r", encoding="utf-8") as file:
                config: dict[str, dict] = yaml.safe_load(file)

            # Validação das chaves esperadas
            required_keys = {"file", "console"}
            if not required_keys.issubset(config["logger"].keys()):
                self._raise_missing_keys(required_keys)

            echo("Configuração carregada com sucesso!", "success")
            super()._separator_line()
        except (yaml.YAMLError, OSError) as e:
            echo(f"Erro ao carregar arquivo YAML: {e}. Usando configuração padrão.", "error")
            return self.get_default_config()
        else:
            return config

    def get_default_config(self) -> LoggerDict:
        """Retorna a configuração padrão do logger."""
        return {
            "logger": {
                "file": {
                    "enabled": True,
                    "level": "DEBUG",
                    "path": "logs/app.log",
                },
                "console": {
                    "level": "INFO",
                },
            }
        }

    def _assign_config(self, config: LoggerDict) -> None:
        """Atribui as configurações do dicionário às variáveis da classe."""
        try:
            optional_keys = {"suppress", "ignore_libs"}
            for key in optional_keys:
                if key not in config["logger"]:
                    config["logger"][key] = []
            self.file_enabled: bool = bool(config["logger"]["file"]["enabled"])
            self.file_level: str = str(config["logger"]["file"]["level"])
            self.file_path: PathLike = str(config["logger"]["file"]["path"])
            self.console_level: str = str(config["logger"]["console"]["level"])
            self.suppress_list: list[str] = [str(item) for item in config["logger"]["suppress"]]
            self.ignore_libs: list[str] = [str(lib) for lib in config["logger"]["ignore_libs"]]
        except KeyError as e:
            echo(f"Erro ao atribuir as chaves do dicionário de configurações: {e}", "error")
            raise

    def _suppress_warnings(self) -> None:
        """Suprime warnings específicos e mensagens de bibliotecas configuradas."""
        try:
            if self.suppress_list:
                for warning_message in self.suppress_list:
                    warnings.filterwarnings(action="ignore", message=warning_message)
        except LoggerError:
            msg = "Erro ao suprimir warnings. Verifique a lista de mensagens."
            echo(msg, "error")
            raise

        try:
            if hasattr(self, "ignore_libs") and self.ignore_libs:
                for lib in self.ignore_libs:
                    logging.getLogger(lib).setLevel(logging.CRITICAL)
        except LoggerError:
            msg = "Erro ao ignorar mensagens de bibliotecas. Verifique a lista de bibliotecas."
            echo(msg, "error")
            raise

    def _define_handlers(self) -> logging.Logger:
        """Configura e retorna um logger com handlers para console e arquivo (opcional)."""
        # Configura o root logger
        logging.basicConfig(level=logging.NOTSET)
        root_logger = logging.getLogger()

        # Remove handlers existentes para evitar duplicação
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Define o nível do logger
        root_logger.setLevel(getattr(logging, self.console_level, logging.INFO))

        # Configura o formato padrão
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(module)s:%(lineno)03d - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Handler de console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, self.console_level, logging.INFO))
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # Handler de arquivo (opcional)
        if self.file_enabled and self.file_path:
            try:
                file_path = super()._ensure_path(self.file_path)
                file_handler = logging.FileHandler(file_path, encoding="utf-8")
                file_handler.setLevel(getattr(logging, self.file_level, logging.DEBUG))
                file_handler.setFormatter(formatter)
                root_logger.addHandler(file_handler)
            except OSError:
                console_handler.setLevel(logging.ERROR)
                root_logger.exception("Erro ao configurar log de arquivo")

        self._suppress_warnings()

        return root_logger

    def dump_config(self) -> str:
        """Retorna a configuração da classe em um JSON dump sem identação."""
        return json.dumps(
            {
                "file_enabled": self.file_enabled,
                "file_level": self.file_level,
                "file_path": str(self.file_path),
                "console_level": self.console_level,
                "suppress_list": self.suppress_list,
            }
        )

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Instancia o logger, inicializando-o  com a configuração padrão se necessário."""
        try:
            if not (cls._instance and cls._instance.logger):
                instance = cls()
                if instance.logger is None:
                    raise RuntimeError("Logger não pôde ser inicializado.")
                return instance.logger
        except LoggerError as e:
            echo(f"Erro um erro ao instanciar o logger: {e}", "error")
            raise
        else:
            return cls._instance.logger
