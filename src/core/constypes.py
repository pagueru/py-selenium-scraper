# ./src/core/constypes.py

from pathlib import Path
from typing import List, Optional, TypeAlias, Union

import __init__
from core.debug import debug

PathLike: TypeAlias = Union[str, Path]
"""Tipo que representa um caminho, podendo ser uma string ou um objeto Path."""

PathLikeAndList: TypeAlias = Union[PathLike, List[PathLike]]
"""Tipo que representa um caminho ou uma lista de caminhos (strings ou objetos Path)."""


def find_project_root(start_dir: Optional[Path] = None) -> Path:
    """
    Encontra o diretório raiz do projeto a partir do diretório informado. A busca é feita
    procurando pelos arquivos 'pyproject.toml' ou '.python-version' em todos os diretórios pais
    do diretório informado. Caso um dos arquivos seja encontrado, o diretório pai é considerado
    o diretório raiz do projeto. Se nenhum dos arquivos for encontrado, o diretório atual ('./')
    será usado como padrão.

    Args:
        start_dir (Path, optional): O diretório a partir do qual a busca começará. Se omitido, o
        diretório atual (onde o script está localizado) será usado.

    Returns:
        Path: O diretório raiz do projeto localizado ou './' se nenhum arquivo for encontrado.
    """
    # Caminho absoluto do diretório inicial
    start_path: Path = Path(start_dir or __file__).resolve()
    for parent in start_path.parents:
        # Verifica se os arquivos 'pyproject.toml' ou '.python-version' foram encontrados
        if (parent / "pyproject.toml").exists() or (
            parent / ".python-version"
        ).exists():
            return parent
    # Se nenhum arquivo for encontrado, retorna o diretório atual
    return Path("./").resolve()


# Caminho base do projeto
PROJECT_ROOT: Path = find_project_root()

# Diretórios principais
CONFIG_DIR: Path = PROJECT_ROOT / "config"
DATA_DIR: Path = PROJECT_ROOT / "data"
LOG_DIR: Path = PROJECT_ROOT / "log"
DOC_DIR: Path = DATA_DIR / "docs"

# Subdiretórios de 'data'
OUTPUT_DIR: Path = DATA_DIR / "output"
INPUT_DIR: Path = DATA_DIR / "input"
IMAGE_DIR: Path = DATA_DIR / "images"

# Arquivos principais
LOG_FILE: Path = LOG_DIR / "app.log"
CONFIG_FILE: Path = CONFIG_DIR / "config.toml"

# Nome do projeto
PROJECT_NAME: str = PROJECT_ROOT.name


if __name__ == "__main__":
    debug("constypes.py")
