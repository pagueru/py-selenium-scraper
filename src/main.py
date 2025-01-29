# ./src/main.py

import json
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import __init__
from core.constypes import IMAGE_DIR, PathLike
from core.utils import logger, start_config


def setup_webdriver(chromedriver_path: PathLike) -> webdriver.Chrome:
    """
    Configura e inicializa o WebDriver do Chrome.

    Args:
        chromedriver_path (PathLike): Caminho para o executável do ChromeDriver.

    Returns:
        webdriver.Chrome: Instância do WebDriver configurada.
    """
    # Inicializa as opções do WebDriver do Chrome
    chrome_options = webdriver.ChromeOptions()

    # Evita detecção por sites
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Executa o Chrome em modo headless (sem interface gráfica)
    chrome_options.add_argument("--headless")

    # Desativa o sandbox para melhorar a compatibilidade
    chrome_options.add_argument("--no-sandbox")

    # Define um user-agent personalizado
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36"
    )

    # Configura o serviço do ChromeDriver
    chrome_service = webdriver.ChromeService(
        chromedriver_path, service_log_path=os.devnull
    )

    # Retorna a instância do WebDriver
    return webdriver.Chrome(service=chrome_service, options=chrome_options)


def save_screenshot(
    driver: webdriver.Chrome,
    filename: str,
    image_folder: PathLike,
    image_format: str = "png",
) -> None:
    """
    Salva uma captura de tela no diretório especificado, adicionando uma
    tag numérica com base nos arquivos existentes.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver.
        filename (str): Nome do arquivo para salvar a captura de tela.
        image_folder (str): Diretório onde a captura de tela será salva.
        image_format (str): Formato da imagem a ser salva (padrão: "png").
    """
    # Lista todos os arquivos no diretório de imagens
    existing_files: List[str] = []
    for f in os.listdir(image_folder):
        if f.endswith(f".{image_format}"):
            existing_files.append(f)

    # Extrai as tags numéricas dos arquivos existentes
    tags = []
    for file in existing_files:
        if "_" in file and file.split("_")[0].isdigit():
            tags.append(int(file.split("_")[0]))

    # Define a próxima tag disponível
    tag = str(max(tags) + 1) if tags else "1"

    # Define o nome do arquivo com a tag numérica
    new_filename = f"{tag}_{filename}.{image_format}"
    screenshot_path = Path(image_folder) / new_filename

    # Salva a captura de tela
    driver.save_screenshot(screenshot_path)
    logger.debug(f"Captura de tela salva em: {screenshot_path}")


def portal_login(
    driver: webdriver.Chrome,
    username: str,
    password: str,
    login_url: str,
    image_folder: PathLike,
) -> None:
    """
    Realiza o login no site especificado e captura screenshots em diferentes etapas do processo.
    Caso nenhum site seja especificado, o site do Colaborar, Portal do Aluno da Anhanguera,
    será usado.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver.
        username (str): Nome de usuário para login.
        password (str): Senha para login.
        login_url (str): URL da página de login. Se não fornecida, será usada a URL padrão.
        image_folder (PathLike): Diretório onde as capturas de tela serão salvas.

    Raises:
        NoSuchElementException: Se algum dos elementos necessários para o login não for encontrado.
    """
    # Verifica se a URL de login foi fornecida
    if not login_url:
        login_url = "https://www.colaboraread.com.br/login/auth"

    # Abre a URL de login
    logger.info("Abrindo o site de login")
    driver.get(login_url)
    driver.implicitly_wait(5)
    save_screenshot(driver, "pagina_login", image_folder)

    # Preenche o campo de login
    logger.info("Preenchendo o campo de login")
    login_field = driver.find_element(By.ID, "username")
    login_field.send_keys(username)
    save_screenshot(driver, "campo_usuario_preenchido", image_folder)

    # Preenche o campo de senha
    logger.info("Preenchendo o campo de senha")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    save_screenshot(driver, "campo_senha_preenchido", image_folder)

    # Fecha o aviso de cookies, se presente
    try:
        logger.info("Fechando o aviso de cookies")
        cookies_button = driver.find_element(By.ID, "btnCookiesAuth")
        cookies_button.click()
        driver.implicitly_wait(1)
        save_screenshot(driver, "aviso_cookies_fechado", image_folder)
    except NoSuchElementException:
        logger.warning("Aviso de cookies não encontrado, prosseguindo")

    # Clica no botão de login
    logger.info("Clicando no botão de login")
    login_button = driver.find_element(
        By.CSS_SELECTOR, "button.btn.btn-primary.btn-lg.btn-block.mb-10"
    )
    login_button.click()
    save_screenshot(driver, "botao_login_clicado", image_folder)
    driver.implicitly_wait(5)


def acessar_curso(
    driver: webdriver.Chrome, curso_nome: str, image_folder: PathLike
) -> None:
    """
    Acessa o curso especificado.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver.
        curso_nome (str): Nome do curso a ser acessado.
        image_folder (str): Diretório onde as capturas de tela serão salvas.
    """
    # Tentar acessar o curso pelo nome
    try:
        # Registra a tentativa de acesso ao curso
        logger.info(f"Acessando o curso: {curso_nome}")

        # Clica no botão do curso para acessá-lo
        course_button = driver.find_element(
            By.CSS_SELECTOR,
            f"button.btn.btn-primary.entrar[title='Entrar em {curso_nome}']",
        )
        course_button.click()
        driver.implicitly_wait(5)
        save_screenshot(driver, "accessed_course", image_folder)
        logger.info("Acesso ao curso realizado com sucesso!")

    # Registrar o erro caso o botão do curso não seja encontrado
    except NoSuchElementException as e:
        logger.error(f"Ocorreu um erro ao tentar acessar o curso: {e}")


def encontrar_disciplinas(
    driver: webdriver.Chrome, index_url: str, matricula: str, image_folder: PathLike
) -> List[Dict[str, Any]]:
    """
    Encontra os links e nomes das disciplinas disponíveis.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver.
        index_url (str): URL da página de índice.
        matricula (str): Matrícula do usuário.
        image_folder (str): Diretório onde as capturas de tela serão salvas.

    Returns:
        List[Dict[str, Any]]: Lista de dicionários contendo links e nomes das
        disciplinas encontradas.
    """
    # Tentar encontrar os links e nomes das disciplinas
    try:
        # Registra a tentativa de encontrar links e nomes das disciplinas
        logger.info("Encontrando links e nomes das disciplinas")

        # Encontra todos os elementos que correspondem ao seletor CSS
        disciplinas = driver.find_elements(
            By.CSS_SELECTOR, "li.atividadesCronograma a.atividadeNome"
        )

        # Inicializa uma lista para armazenar as informações das disciplinas
        disciplinas_info = []

        # Itera sobre os elementos para obter as informações das disciplinas
        for disciplina in disciplinas:
            # Obtém o href e o nome da disciplina
            href = disciplina.get_attribute("href")
            nome = disciplina.get_attribute("title")

            # Remover espaços em branco do nome, se existir
            if nome:
                nome = nome.strip()

            # Adicionar as informações da disciplina à lista, se o href não for None
            if href is not None:
                disciplinas_info.append({"nome": nome, "link": href})

        # Filtrar disciplinas que não correspondem ao link do índice
        disciplinas_filtradas = []
        for info in disciplinas_info:
            if info["link"] != f"{index_url}/{matricula}":
                disciplinas_filtradas.append(info)

        # Loga nomes de disciplinas encontradas
        for info in disciplinas_filtradas:
            logger.info(f"Disciplina encontrada: {info['nome']}")

        # Salva uma captura de tela após encontrar os links das disciplinas
        save_screenshot(driver, "found_discipline_links", image_folder)

        # Retorna a lista de disciplinas filtradas
        return disciplinas_filtradas

    # Registrar o erro caso não seja possível encontrar os links e nomes das disciplinas
    except NoSuchElementException as e:
        logger.error(
            f"Ocorreu um erro ao tentar encontrar os links e nomes das disciplinas: {e}"
        )
        return []


def acessar_disciplinas(
    driver: webdriver.Chrome, disciplinas_info: List[Dict[str, Any]]
) -> None:
    """
    Acessa cada disciplina e tira uma captura de tela.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver.
        disciplinas_info (List[Dict[str, Any]]): Lista de dicionários contendo links
        e nomes das disciplinas.
    """
    for disciplina in disciplinas_info:
        try:
            logger.info(f"Acessando a disciplina: {disciplina['nome']}")
            driver.get(disciplina["link"])
            driver.implicitly_wait(5)
            screenshot_filename = f"{disciplina['nome'].replace(' ', '_')}"
            driver.save_screenshot(IMAGE_DIR / screenshot_filename)
            save_screenshot(driver, "screenshot_filename", IMAGE_DIR)
            logger.info(f"Captura de tela da disciplina '{disciplina['nome']}' salva.")
        except RuntimeError as e:
            logger.error(f"Erro ao acessar a disciplina '{disciplina['nome']}': {e}")


def capturar_informacoes_disciplinas(
    driver: webdriver.Chrome,
    disciplinas_info: List[Dict[str, Any]],
    atividades_ignoradas: List[str],
) -> Dict[str, Any]:
    """
    Captura informações de cada disciplina e as salva em um JSON.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver.
        disciplinas_info (List[Dict[str, Any]]): Lista de dicionários contendo links
        e nomes das disciplinas.
        atividades_ignoradas (List[str]): Lista de atividades a serem ignoradas.

    Returns:
        Dict[str, Any]: Dicionário contendo as informações das disciplinas.
    """
    informacoes_disciplinas = {}

    for disciplina in disciplinas_info:
        try:
            logger.debug(f"Capturando informações da disciplina: {disciplina['nome']}")
            driver.get(disciplina["link"])
            driver.implicitly_wait(5)

            # Capturar todas as atividades e seus períodos
            atividades_elements = driver.find_elements(
                By.CSS_SELECTOR, "#js-activities-container .atividades"
            )
            atividades = []
            for atividade_element in atividades_elements:
                try:
                    nome_atividade_element = atividade_element.find_element(
                        By.CSS_SELECTOR, "div.timeline-heading h4.timeline-title small"
                    )
                    nome_atividade = nome_atividade_element.text.strip()

                    # Ignorar atividades listadas em atividades_ignoradas
                    if any(
                        ignorada in nome_atividade for ignorada in atividades_ignoradas
                    ):
                        continue

                    periodo_element = atividade_element.find_element(
                        By.CSS_SELECTOR, "small.text-muted em"
                    )
                    periodo = periodo_element.text.strip()

                    atividades.append(
                        {
                            "nome_atividade": nome_atividade,
                            "periodo": periodo,
                        }
                    )
                except NoSuchElementException:
                    continue

            # Adicionar informações ao dicionário
            informacoes_disciplinas[disciplina["nome"]] = {
                "link_disciplina": disciplina["link"],
                "atividades": atividades,
            }

            logger.info(f"Informações da disciplina '{disciplina['nome']}' capturadas.")
        except RuntimeError as e:
            logger.error(
                f"Erro ao capturar informações da disciplina '{disciplina['nome']}': {e}"
            )

    return informacoes_disciplinas


def converter_json_para_yml(json_filepath: str, yml_filepath: str) -> None:
    """
    Converte um arquivo JSON para YML.

    Args:
        json_filepath (str): Caminho do arquivo JSON.
        yml_filepath (str): Caminho do arquivo YML.
    """
    with open(json_filepath, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    with open(yml_filepath, "w", encoding="utf-8") as yml_file:
        yaml.dump(data, yml_file, allow_unicode=True, default_flow_style=False)

    logger.info(f"Arquivo YML salvo em '{yml_filepath}'.")


def carregar_configuracoes(config_path: str) -> Dict[str, Any]:
    """Carrega as configurações a partir de um arquivo YAML."""
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def salvar_informacoes(informacoes: Dict[str, Any], output_dir: str) -> None:
    """Salva as informações das disciplinas em arquivos JSON e YAML."""
    json_filepath = Path(output_dir) / "informacoes_disciplinas.json"
    yml_filepath = Path(output_dir) / "informacoes_disciplinas.yml"

    with open(json_filepath, "w", encoding="utf-8") as json_file:
        json.dump(informacoes, json_file, ensure_ascii=False, indent=4)
    yaml.dump(
        informacoes,
        open(yml_filepath, "w", encoding="utf-8"),
        allow_unicode=True,
        default_flow_style=False,
    )

    logger.info(f"Informações salvas em JSON: {json_filepath}")
    logger.info(f"Informações salvas em YAML: {yml_filepath}")


def executar_fluxo(config: Dict[str, Any]) -> None:
    """Executa o fluxo principal do script."""
    driver = None
    try:
        driver = setup_webdriver(config["chromedriver"])

        # Cria uma nova pasta com data e hora para salvar as capturas de tela
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_folder = Path("./data/images") / timestamp
        image_folder.mkdir(parents=True, exist_ok=True)

        portal_login(
            driver,
            config["usuario"],
            config["senha"],
            config["colaborar_url"],
            image_folder,
        )
        acessar_curso(driver, config["nome_curso"], image_folder)
        disciplinas_info = encontrar_disciplinas(
            driver, config["colaborar_index_url"], config["matricula"], image_folder
        )

        if config.get("profile_mode", "info") == "debug":
            for disciplina in disciplinas_info:
                acessar_disciplinas(driver, [disciplina])
                save_screenshot(
                    driver, f"{disciplina['nome'].replace(' ', '_')}", image_folder
                )

        informacoes_disciplinas = capturar_informacoes_disciplinas(
            driver, disciplinas_info, config.get("atividades_ignoradas", [])
        )

        salvar_informacoes(informacoes_disciplinas, "./data/output")
    finally:
        if driver:
            save_screenshot(driver, "final_state", IMAGE_DIR)
            driver.quit()


def main() -> None:
    """Função principal que executa o fluxo do script."""
    try:
        # Carregar o arquivo de configuração
        config_yml = carregar_configuracoes("./config/config.yml")

        # Executar o fluxo principal do script
        executar_fluxo(config_yml)

    except RuntimeError as e:
        logger.error(f"Ocorreu um erro: {e}")
    except KeyboardInterrupt:
        logger.warning("O script foi interrompido pelo usuário.")
    finally:
        logger.info("Script finalizado.")


if __name__ == "__main__":
    start_config()
    main()
