"""Módulo base para todas as classes do projeto."""

from dataclasses import dataclass, field
import inspect
import json
from logging import Logger
from pathlib import Path
import shutil
from typing import Any

import yaml

from src.common.echo import echo
from src.common.errors.errors import ProjectError
from src.config.constypes import PathLike


@dataclass
class BaseClass:
    """Classe base para fornecer métodos comuns a todas as classes."""

    logger: Logger = field(init=False)
    """Logger singleton para registrar eventos e erros."""

    def _get_current_method_name(self) -> str:
        """Retorna dinamicamente o nome da classe e do método atual."""
        try:
            current_frame = inspect.currentframe()
            if current_frame is not None:
                method_name = current_frame.f_code.co_name
                return f"{self.__class__.__name__}.{method_name}"
        except ProjectError:
            echo("Falha ao obter o nome do método atual.", "error")
            raise
        else:
            return f"{self.__class__.__name__}.<desconhecido>"

    def _raise_error(self) -> str:
        """Levanta um erro personalizado com o nome da classe e do método atual."""
        return f"Erro inesperado ao executar o método '{self._get_current_method_name()}'"

    def _handle_value_error(self, message: str) -> None:
        """Lança um ValueError com mensagem padronizada e registra o erro."""
        raise ValueError(message)

    def _separator_line(self, char: str = "-", padding: int = 0) -> None:
        """Imprime uma linha ajustada ao tamanho do terminal ou ao valor fornecido pelo usuário."""
        try:
            width = padding if padding > 0 else shutil.get_terminal_size((80, 20)).columns
            print(char * width)
        except ProjectError as e:
            echo(f"Falha ao obter o tamanho do terminal: {e}", "warn")
            raise

    def _ensure_path(self, path_str: PathLike) -> Path:
        """Converte uma string de caminho em um objeto Path e garante que o diretório exista."""
        if not isinstance(path_str, (str, Path)):
            msg = "O caminho deve ser uma string ou um objeto Path."
            echo(msg, "error")
            raise ProjectError(msg)
        path: Path = Path(path_str)
        if not path.parent.exists():
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
            except ProjectError as e:
                echo(f"Erro ao criar diretório: {e}", "error")
                raise
        return path

    def _load_file(self, file_path: PathLike, key: str | None = None) -> dict[str, Any]:
        """Carrega dados de um arquivo JSON, YAML ou ICS. Para YAML/JSON, pode acessar uma key."""
        try:
            file_path = Path(file_path)
            file_extension = file_path.suffix.lower()

            with file_path.open("r", encoding="utf-8") as file:
                if file_extension in [".yaml", ".yml"]:
                    data = yaml.safe_load(file)
                if file_extension == ".json":
                    data = json.load(file)
                if file_extension == ".ics":
                    return {"ics_content": file.read()}
                self._handle_value_error(f"Formato de arquivo não suportado: {file_extension}")

                if not isinstance(data, dict):
                    self._handle_value_error(
                        f"Esperado um dicionário no conteúdo de {file_path.name}, "
                        f"mas recebeu: {type(data)}"
                    )

                return data[key] if key else data

        except FileNotFoundError as e:
            echo(f"Arquivo de configurações não encontrado: {e}", "error")
            raise
        except Exception as e:
            echo(f"Erro ao carregar o arquivo '{file_path}': {e}", "error")
            raise
