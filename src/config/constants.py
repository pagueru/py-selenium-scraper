"""Módulo de definição de constantes globais para o projeto."""

from pathlib import Path
from zoneinfo import ZoneInfo

APP_NAME: str = "py-selenium-scraper"
"""Nome da aplicação: `py-selenium-scraper`."""

VERSION: str = "0.1.0"
"""Versão da aplicação: `0.1.0`"""

SETTINGS_FILE: Path = Path("./src/config/files/settings.yaml")
"""Caminho para o arquivo de configuração global: `./src/config/files/settings.yaml`"""

BRT: ZoneInfo = ZoneInfo("America/Sao_Paulo")
"""Define o objeto de fuso horário para o horário de Brasília:  `America/Sao_Paulo`"""

PROFILE_MODE: str = "info"
"""Define o modo de perfil da aplicação: `info`"""

OUTPUT_DIR: Path = Path("./data/output")
"""Diretório de saída para arquivos gerados: `./data/output`"""

IMAGE_DIR: Path = Path("./data/output/images")
"""Diretório de saída para imagens: `./data/output/images`"""
