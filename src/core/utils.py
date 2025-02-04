# ./src/core/utils.py

import logging
import platform
import subprocess
import time
import warnings
import winsound
from datetime import datetime
from typing import List, Optional

import __init__
from core.constypes import LOG_FILE, PROFILE_MODE, PathLike
from core.debug import debug


def setup_logger(
    log_file_path: Optional[PathLike] = None,
    enable_file_log: bool = False,
    level: int = logging.INFO,
    suppress_loggers: Optional[List[str]] = None,
) -> logging.Logger:
    """
    Configura e retorna um logger com handlers para console e arquivo (opcional).

    Args:
        log_file_path (Optional[PathLike]): Caminho do arquivo de log.
        enable_file_log (bool): Ativa ou desativa o log em arquivo (padrão: False).
        level (int): Nível de log (padrão: INFO).
        suppress_loggers (Optional[List[str]]): Lista de loggers a serem suprimidos.

    Returns:
        logging.Logger: Logger configurado.
    """
    logger_setup: logging.Logger = logging.getLogger(__name__)
    logger_setup.setLevel(level)

    # Evita adicionar handlers duplicados
    if logger_setup.hasHandlers():
        return logger_setup

    # Formato do log
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger_setup.addHandler(console_handler)

    # Handler opcional para arquivo
    if enable_file_log and log_file_path:
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger_setup.addHandler(file_handler)

    # Suprime logs de módulos específicos (por exemplo, Selenium)
    if suppress_loggers:
        for logger_name in suppress_loggers:
            logging.getLogger(logger_name).setLevel(logging.WARNING)

    return logger_setup


# Configura o nível de log
log_level = logging.INFO

if PROFILE_MODE == "debug":
    log_level = logging.DEBUG
if PROFILE_MODE == "info":
    log_level = logging.INFO

# Inicializa o logger global
logger = setup_logger(log_file_path=LOG_FILE, enable_file_log=True, level=log_level)


def terminal_line(value: int = 79, char: str = "-") -> None:
    """
    Imprime uma linha no terminal com o caractere especificado.

    Args:
        value (int): Comprimento da linha (padrão: 79).
        char (str): Caractere a ser usado na linha (padrão: "-").
    """
    if value <= 0:
        raise ValueError("O valor deve ser maior que 0.")
    print(char * value)


def start_config(clear_terminal: bool = True) -> None:
    """
    Limpa o terminal e maraca o inicio do script.
    """
    try:
        if clear_terminal:
            subprocess.run(
                ["cls" if platform.system() == "Windows" else "clear"],
                shell=True,
                check=False,
            )
        warnings.filterwarnings("ignore", category=UserWarning, module="selenium")
        terminal_line()
        logger.info("Iniciando o script.")
    except RuntimeError as e:
        logger.error(f"Erro ao limpar o terminal: {e}")
        raise


def execution_time(start_time: float, beep: bool = False) -> None:
    """
    Calcula e registra o tempo de execução do script.

    Args:
        start_time (float): Tempo de início da execução.
    """
    logger.info(f"Tempo de execução: {round(time.time() - start_time, 2)} segundos")
    if beep:
        winsound.Beep(750, 300)


def ics_date(date_str: str) -> str:
    """
    Converte uma string de data do formato 'ddmmyy' para 'yyyymmdd'.

    Args:
        date_str (str): A string de data no formato 'ddmmyy'.

    Returns:
        str: A string de data formatada no formato 'yyyymmdd'.
    """
    return datetime.strptime(date_str, "%d%m%y").strftime("%Y%m%d")


if __name__ == "__main__":
    debug("utils.py")
