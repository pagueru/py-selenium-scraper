# ./src/main.py

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import __init__
from core.constypes import PROFILE_MODE, PathLike, load_file
from core.utils import execution_time, logger, start_config, terminal_line

# Verifica se o modo de perfil foi definido
if not PROFILE_MODE:
    raise RuntimeError("O modo de perfil não foi definido.")


def setup_webdriver(chromedriver_path: PathLike) -> webdriver.Chrome:
    """
    Configura e inicializa o WebDriver do Chrome.

    Args:
        chromedriver_path (PathLike): Caminho para o executável do ChromeDriver.

    Returns:
        webdriver.Chrome: Instância do WebDriver configurada.
    """
    # Configura opções do Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36"
    )

    # Configura o serviço do ChromeDriver
    chrome_service = webdriver.ChromeService(
        chromedriver_path, service_log_path=os.devnull
    )

    # Inicializa e retorna a instância do WebDriver
    return webdriver.Chrome(service=chrome_service, options=chrome_options)


def save_screenshot(
    driver: webdriver.Chrome,
    filename: str,
    image_folder: PathLike,
    image_format: str = "png",
) -> None:
    """
    Salva uma captura de tela no diretório especificado, adicionando uma
    tag numérica com base nos arquivos existentes, se o profile_mode for "debug".

    Args:
        driver (webdriver.Chrome): Instância do WebDriver.
        filename (str): Nome do arquivo para salvar a captura de tela.
        image_folder (str): Diretório onde a captura de tela será salva.
        image_format (str): Formato da imagem a ser salva (padrão: "png").
    """
    # Se o modo de perfil não for "debug", não executa a função
    if PROFILE_MODE != "debug":
        return

    # Lista os arquivos existentes no diretório de imagens
    existing_files: List[str] = []
    for image_file in os.listdir(image_folder):
        if image_file.endswith(f".{image_format}"):
            existing_files.append(image_file)

    # Extrai as tags numéricas dos arquivos existentes
    tags = []
    for file in existing_files:
        if "_" in file and file.split("_")[0].isdigit():
            tags.append(int(file.split("_")[0]))

    # Define a nova tag numérica
    tag = str(max(tags) + 1) if tags else "1"
    new_filename = f"{tag}_{filename}.{image_format}"

    # Salva a captura de tela no caminho especificado
    screenshot_path = Path(image_folder) / new_filename
    driver.save_screenshot(screenshot_path)
    logger.debug(f"Captura de tela salva em: {screenshot_path}")


def portal_login(
    driver: webdriver.Chrome,
    username: str,
    password: str,
    login_url: Optional[str],
    image_folder: PathLike,
) -> None:
    """
    Realiza o login no site especificado e captura screenshots em diferentes etapas do processo.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver.
        username (str): Nome de usuário para login.
        password (str): Senha para login.
        login_url (str): URL da página de login. Se não fornecida, será usada a URL padrão.
        image_folder (PathLike): Diretório onde as capturas de tela serão salvas.

    Raises:
        NoSuchElementException: Se algum dos elementos necessários para o login não for encontrado.
    """
    # Define a URL de login padrão, se não fornecida
    if not login_url:
        login_url = "https://www.colaboraread.com.br/login/auth"

    # Abre a página de login
    logger.info(f"Abrindo o site de login: {login_url}")
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


def access_course(
    driver: webdriver.Chrome, curso_nome: str, image_folder: PathLike
) -> None:
    """
    Acessa o curso especificado.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver.
        curso_nome (str): Nome do curso a ser acessado.
        image_folder (str): Diretório onde as capturas de tela serão salvas.
    """
    try:
        logger.info(f"Acessando o curso: {curso_nome}")

        # Encontra e clica no botão do curso
        course_button = driver.find_element(
            By.CSS_SELECTOR,
            f"button.btn.btn-primary.entrar[title='Entrar em {curso_nome}']",
        )
        course_button.click()
        driver.implicitly_wait(5)

        # Salva a captura de tela após clicar no botão
        save_screenshot(driver, "botao_acessar_curso_clicado", image_folder)
    except NoSuchElementException as e:
        # Loga o erro caso o botão do curso não seja encontrado
        logger.error(f"Erro ao tentar acessar o curso: {e}")


def find_subjects(
    driver: webdriver.Chrome,
    index_url: str,
    matricula: str,
    image_folder: PathLike,
) -> List[Dict[str, Union[str, Any]]]:
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
    # Encontra os links e nomes das disciplinas disponíveis
    try:
        logger.info("Encontrando links e nomes das disciplinas")
        disciplinas = driver.find_elements(
            By.CSS_SELECTOR, "li.atividadesCronograma a.atividadeNome"
        )

        # Coleta as informações das disciplinas
        disciplinas_info = []
        for disciplina in disciplinas:
            if disciplina.get_attribute("href") and disciplina.get_attribute("title"):
                disciplinas_info.append(
                    {
                        "nome": disciplina.get_attribute("title").strip(),  # type: ignore
                        "link": disciplina.get_attribute("href"),
                    }
                )

        # Filtra as disciplinas
        disciplinas_filtradas = []
        for info in disciplinas_info:
            if info["link"] != f"{index_url}/{matricula}":
                disciplinas_filtradas.append(info)

        # Loga as disciplinas encontradas
        for info in disciplinas_filtradas:
            logger.info(f"Disciplina encontrada: {info['nome']}")

        save_screenshot(driver, "disciplinas_encontradas", image_folder)
        return disciplinas_filtradas

    except NoSuchElementException as e:
        logger.error(f"Erro ao tentar encontrar os links e nomes das disciplinas: {e}")
        return []


def capture_subjects(
    driver: webdriver.Chrome,
    disciplinas_info: List[Dict[str, Union[str, Any]]],
    image_folder: PathLike,
) -> None:
    """
    Acessa cada disciplina e tira uma captura de tela.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver.
        disciplinas_info (List[Dict[str, Any]]): Lista de dicionários contendo links
        e nomes das disciplinas.
    """
    # Itera sobre cada disciplina
    for disciplina in disciplinas_info:
        try:
            # Acessa a página da disciplina
            logger.info(f"Acessando a disciplina: {disciplina['nome']}")
            driver.get(disciplina["link"])
            driver.implicitly_wait(5)

            # Salva a captura de tela da disciplina
            screenshot_filename = f"{disciplina['nome'].replace(' ', '_')}"
            save_screenshot(driver, screenshot_filename, image_folder)
            logger.info(f"Captura de tela da disciplina '{disciplina['nome']}' salva.")

        # Trata exceções de elementos não encontrados
        except NoSuchElementException as e:
            logger.error(
                f"Erro ao tentar acessar a disciplina '{disciplina['nome']}': {e}"
            )

        # Trata exceções de runtime
        except RuntimeError as e:
            logger.error(f"Erro ao acessar a disciplina '{disciplina['nome']}': {e}")


def fetch_subjects_information(
    driver: webdriver.Chrome,
    disciplinas_info: List[Dict[str, Union[str, Any]]],
    atividades_ignoradas: List[Union[str, Any]],
) -> Dict[str, Union[str, List[Dict[str, str]]]]:
    """
    Captura informações de cada disciplina e as salva em um JSON.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver.
        disciplinas_info (List[Dict[str, Any]]): Lista de dicionários contendo
        links e nomes das disciplinas.
        atividades_ignoradas (List[str]): Lista de atividades a serem ignoradas.

    Returns:
        Dict[str, Any]: Dicionário contendo as informações das disciplinas.
    """
    # Itera sobre cada disciplina para capturar suas informações
    informacoes_disciplinas: Dict[str, Any] = {}
    for disciplina in disciplinas_info:
        try:
            # Acessa a página da disciplina
            logger.debug(f"Capturando informações da disciplina: {disciplina['nome']}")
            driver.get(disciplina["link"])
            driver.implicitly_wait(5)

            # Encontra os elementos das atividades na página da disciplina
            atividades_elements = driver.find_elements(
                By.CSS_SELECTOR, "#js-activities-container .atividades"
            )

            # Itera sobre cada elemento de atividade para extrair suas informações
            atividades = []
            for atividade_element in atividades_elements:
                try:
                    # Extrai o tipo de atividade
                    tipo_atividade = (
                        atividade_element.find_element(
                            By.CSS_SELECTOR, "div.timeline-heading h4.timeline-title"
                        )
                        .text.strip()
                        .split("\n")[0]
                    )

                    # Ignora atividades que estão na lista de atividades ignoradas
                    if any(
                        ignorada in tipo_atividade for ignorada in atividades_ignoradas
                    ):
                        continue

                    # Extrai o nome e o período da atividade
                    nome_atividade = atividade_element.find_element(
                        By.CSS_SELECTOR, "div.timeline-heading h4.timeline-title small"
                    ).text.strip()

                    periodo = atividade_element.find_element(
                        By.CSS_SELECTOR, "small.text-muted em"
                    ).text.strip()

                    # Adiciona a atividade à lista de atividades da disciplina
                    atividades.append(
                        {
                            "nome_atividade": nome_atividade,
                            "tipo_atividade": tipo_atividade,
                            "periodo": periodo,
                        }
                    )
                except NoSuchElementException:
                    continue

            # Adiciona as informações da disciplina ao dicionário
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


def convert_json_to_yaml(json_filepath: str, yml_filepath: str) -> None:
    """
    Converte um arquivo JSON para YML.

    Args:
        json_filepath (str): Caminho do arquivo JSON.
        yml_filepath (str): Caminho do arquivo YML.
    """
    data = load_file(json_filepath)

    with open(yml_filepath, "w", encoding="utf-8") as yml_file:
        yaml.dump(data, yml_file, allow_unicode=True, default_flow_style=False)

    logger.info(f"Arquivo YML salvo em '{yml_filepath}'.")


def generate_ics_file(
    informacoes: Dict[str, Any],
    template_path: PathLike,
    output_path: PathLike,
    config: Dict[str, Any],
) -> None:
    """
    Gera um arquivo .ics a partir das informações das disciplinas.

    Args:
        informacoes (Dict[str, Any]): Dicionário contendo as informações das disciplinas.
        template_path (PathLike): Caminho do arquivo de template .ics.
        output_path (PathLike): Caminho onde o arquivo .ics gerado será salvo.
        config (Dict[str, Any]): Dicionário contendo as configurações do script.
    """
    # Carrega o template do arquivo .ics e inicia o conteúdo
    template = load_file(template_path)["ics_content"]
    ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\n"

    # Itera sobre as disciplinas e atividades
    for disciplina, dados in informacoes.items():
        for atividade in dados["atividades"]:
            nome_atividade = atividade["nome_atividade"]
            periodo = str(atividade["periodo"]).split(" - ")
            inicio = periodo[0].replace("/", "")
            fim = periodo[1].replace("/", "")

            # Adiciona evento de início
            evento = template.format(
                nome_aluno=config["nome_aluno"],
                semestre=config["semestre"],
                nome_curso=config["nome_curso"],
                tipo_periodo="Início",
                nome_atividade=nome_atividade,
                data_periodo=inicio,
                disciplina=disciplina,
            )
            ics_content += evento

            if inicio != fim:
                evento = template.format(
                    nome_aluno=config["nome_aluno"],
                    semestre=config["semestre"],
                    nome_curso=config["nome_curso"],
                    tipo_periodo="Fim",
                    nome_atividade=nome_atividade,
                    data_periodo=fim,
                    disciplina=disciplina,
                )
                ics_content += evento

    ics_content += "END:VCALENDAR\n"

    with open(output_path, "w", encoding="utf-8") as ics_file:
        ics_file.write(ics_content)

    logger.info(f"Informações salvas em ICS: {output_path}")


def export_information(
    informacoes: Dict[str, Union[str, Any]], output_dir: str, config: Dict[str, Any]
) -> None:
    """
    Salva as informações das disciplinas em arquivos JSON, YAML e ICS.

    Args:
        informacoes (Dict[str, Any]): Dicionário contendo as informações das disciplinas.
        output_dir (str): Diretório de saída para salvar os arquivos.
        config (Dict[str, Any]): Dicionário contendo as configurações do script.
    """
    # Define os caminhos dos arquivos de saída
    json_filepath = Path(output_dir) / "informacoes_disciplinas.json"
    yml_filepath = Path(output_dir) / "informacoes_disciplinas.yml"
    ics_filepath = Path(output_dir) / "informacoes_disciplinas.ics"

    # Salva as informações em formato JSON
    with open(json_filepath, "w", encoding="utf-8") as json_file:
        json.dump(informacoes, json_file, ensure_ascii=False, indent=4)

    # Salva as informações em formato YAML
    with open(yml_filepath, "w", encoding="utf-8") as yml_file:
        yaml.dump(informacoes, yml_file, allow_unicode=True, default_flow_style=False)

    # Gera o arquivo ICS com base nas informações e no template
    generate_ics_file(
        informacoes,
        "./config/ics_template.ics",
        ics_filepath,
        config,
    )

    # Loga as informações dos arquivos salvos
    logger.info(f"Informações salvas em JSON: {json_filepath}")
    logger.info(f"Informações salvas em YAML: {yml_filepath}")


def run_workflow(config: Dict[str, Union[str, Any]]) -> None:
    """
    Executa o fluxo principal do script.

    Args:
        config (Dict[str, Any]): Dicionário contendo as configurações do script.
    """
    # Executa o fluxo principal do script
    driver = None
    image_folder = None
    try:
        # Configura o WebDriver
        driver = setup_webdriver(config["chromedriver"])

        # Marca o início do script
        start_config()

        # Define o diretório de imagens com base no modo de perfil
        if PROFILE_MODE == "debug":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_folder = Path("./data/images") / timestamp
            image_folder.mkdir(parents=True, exist_ok=True)
        else:
            image_folder = Path("./data/images")

        # Realiza o login no portal
        portal_login(
            driver,
            config["usuario"],
            config["senha"],
            config["colaborar_url"],
            image_folder,
        )

        # Acessa o curso especificado
        access_course(driver, config["nome_curso"], image_folder)

        # Encontra as disciplinas disponíveis
        disciplinas_info = find_subjects(
            driver, config["colaborar_index_url"], config["matricula"], image_folder
        )

        # Captura as disciplinas, se em modo "debug"
        if PROFILE_MODE == "debug":
            for disciplina in disciplinas_info:
                capture_subjects(driver, [disciplina], image_folder)

        # Captura as informações das disciplinas
        informacoes_disciplinas = fetch_subjects_information(
            driver, disciplinas_info, config.get("atividades_ignoradas", [])  # type: ignore
        )

        # Exporta as informações das disciplinas
        export_information(informacoes_disciplinas, "./data/output", config)
    except KeyboardInterrupt:
        logger.warning("Script interrompido pelo usuário.")
    finally:
        if driver and image_folder:
            save_screenshot(driver, "final_state", image_folder)
            driver.quit()


def main() -> None:
    """Função principal que executa o fluxo do script."""
    start_time = time.time()
    try:
        config_yml = load_file("./config/config.yml")
        run_workflow(config_yml)
    except RuntimeError as e:
        logger.error(f"Ocorreu um erro: {e}")
    except KeyboardInterrupt:
        logger.warning("Script interrompido pelo usuário.")
    finally:
        logger.info("Script finalizado.")
        execution_time(start_time)
        terminal_line()
        sys.exit(0)


if __name__ == "__main__":
    main()
