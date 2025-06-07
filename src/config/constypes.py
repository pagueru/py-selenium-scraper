"""Módulo de definição de tipos personalizados."""

from pathlib import Path

type PathLike = str | Path
"""Tipo que representa um caminho, podendo ser uma string ou um objeto Path."""

type LoggerDict = dict[str, dict[str, dict[str, bool | str] | dict[str, str]]]
"""Tipo que representa um dicionário de configuração para o logger."""
