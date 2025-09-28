"""Orquestrador principal: executa scraping, transformação e armazenamento."""

import json
import os
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Any

import yaml
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.common.base.base_class import BaseClass
from src.common.echo import echo
from src.common.errors.errors import ProjectError
from src.config.constants import BRT, IMAGE_DIR, OUTPUT_DIR, PROFILE_MODE, SETTINGS_FILE
from src.config.constypes import PathLike
from src.infrastructure.logger import LoggerSingleton

# Verifica se o modo de perfil foi definido
if not PROFILE_MODE:
    raise RuntimeError("O modo de perfil não foi definido.")


class SeleniumScraperPipeline(BaseClass):
    """Classe para automação de scraping com Selenium no portal ColaborarEAD."""

    def __init__(self, config: dict[str, Any] | None = None, *, show_browser: bool = False) -> None:
        """Inicializa a instância do SeleniumScraperPipeline."""
        self.logger = LoggerSingleton().logger or LoggerSingleton.get_logger()
        """Logger singleton para registrar eventos e erros."""

        self.settings = config if config else super()._load_file(SETTINGS_FILE)
        """Configurações carregadas do arquivo ou fornecidas via parâmetro."""

        self.driver = None
        """Instância do WebDriver do Selenium."""

        self.image_folder = IMAGE_DIR
        """Diretório onde as capturas de tela serão salvas."""

        self.output_path = OUTPUT_DIR
        """Diretório de saída para arquivos gerados."""

        self.login_url = "https://www.colaboraread.com.br/login/auth"
        """URL da página de login do portal."""

        self.json_filepath = OUTPUT_DIR / "informacoes_disciplinas.json"
        """Caminho do arquivo JSON de saída."""

        self.yml_filepath = OUTPUT_DIR / "informacoes_disciplinas.yml"
        """Caminho do arquivo YAML de saída."""

        self.ics_filepath = OUTPUT_DIR / "informacoes_disciplinas.ics"
        """Caminho do arquivo ICS de saída."""

        self.ics_template_filepath = "./src/config/files/ics_template.ics"
        """Caminho do template ICS."""

        self.show_browser = show_browser
        """Define se o navegador será exibido (modo headless ou não)."""

    def _convert_ics_date(self, date_str: str) -> str:
        """Converte uma string de data do formato 'ddmmyy' para 'yyyymmdd'."""
        return datetime.strptime(date_str, "%d%m%y").replace(tzinfo=BRT).strftime("%Y%m%d")

    def _setup_webdriver(self) -> webdriver.Chrome:
        """Configura e inicializa o WebDriver do Chrome usando webdriver-manager."""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-tools")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--remote-debugging-port=0")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)  # noqa: FBT003
        if not self.show_browser:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36"
        )
        service = ChromeService(ChromeDriverManager().install(), log_path=os.devnull)
        return webdriver.Chrome(service=service, options=chrome_options)

    def _save_screenshot(self, filename: str, image_format: str = "png") -> None:
        """Salva uma captura de tela do navegador em um diretório especificado."""
        # Se o modo de perfil não for "debug", não executa a função
        if PROFILE_MODE != "debug":
            return

        # Lista os arquivos existentes no diretório de imagens
        existing_files: list[str] = []
        for image_file in Path(self.image_folder).iterdir():
            if image_file.is_file() and image_file.name.endswith(f".{image_format}"):
                existing_files.append(image_file.name)

        # Extrai as tags numéricas dos arquivos existentes
        tags = []
        for file in existing_files:
            if "_" in file and file.split("_")[0].isdigit():
                tags.append(int(file.split("_")[0]))

        # Define a nova tag numérica
        tag = str(max(tags) + 1) if tags else "1"
        new_filename = f"{tag}_{filename}.{image_format}"

        # Salva a captura de tela no caminho especificado
        screenshot_path = Path(self.image_folder) / new_filename
        self.driver.save_screenshot(screenshot_path)
        self.logger.debug(f"Captura de tela salva em: {screenshot_path}")

    def portal_login(self, username: str, password: str) -> None:
        """Realiza o login no site e captura screenshots em diferentes etapas do processo."""
        # Define a URL de login padrão, se não fornecida

        # Abre a página de login
        self.logger.info(f"Abrindo o site de login: '{self.login_url}'")
        self.driver.get(self.login_url)
        self.driver.implicitly_wait(5)
        self._save_screenshot("pagina_login")

        # Preenche o campo de login
        self.logger.info("Preenchendo o campo de login")
        login_field = self.driver.find_element(By.ID, "username")
        login_field.send_keys(username)
        self._save_screenshot("campo_usuario_preenchido")

        # Preenche o campo de senha
        self.logger.info("Preenchendo o campo de senha")
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        self._save_screenshot("campo_senha_preenchido")

        # Fecha o aviso de cookies, se presente
        try:
            self.logger.info("Fechando o aviso de cookies")
            cookies_button = self.driver.find_element(By.ID, "btnCookiesAuth")
            cookies_button.click()
            self.driver.implicitly_wait(1)
            self._save_screenshot("aviso_cookies_fechado")
        except NoSuchElementException:
            self.logger.warning("Aviso de cookies não encontrado, prosseguindo")

        # Clica no botão de login
        self.logger.info("Clicando no botão de login")
        login_button = self.driver.find_element(
            By.CSS_SELECTOR, "button.btn.btn-primary.btn-lg.btn-block.mb-10"
        )
        login_button.click()
        self._save_screenshot("botao_login_clicado")
        self.driver.implicitly_wait(5)

    def access_course(self, curso_nome: str) -> None:
        """Acessa o curso especificado."""
        try:
            self.logger.info(f"Acessando o curso: '{curso_nome}'")

            # Encontra e clica no botão do curso
            course_button = self.driver.find_element(
                By.CSS_SELECTOR,
                f"button.btn.btn-primary.entrar[title='Entrar em {curso_nome}']",
            )
            course_button.click()
            self.driver.implicitly_wait(5)

            # Salva a captura de tela após clicar no botão
            self._save_screenshot("botao_acessar_curso_clicado")
        except NoSuchElementException:
            self.logger.exception("Erro ao tentar acessar o curso")

    def find_subjects(self, index_url: str, matricula: str) -> list[dict[str, str | Any]]:
        """Encontra os links e nomes das disciplinas disponíveis."""
        try:
            self.logger.info("Encontrando links e nomes das disciplinas")
            disciplinas = self.driver.find_elements(
                By.CSS_SELECTOR, "li.atividadesCronograma a.atividadeNome"
            )

            # Coleta as informações das disciplinas
            disciplinas_info = []
            for disciplina in disciplinas:
                if disciplina.get_attribute("href") and disciplina.get_attribute("title"):
                    disciplinas_info.append(
                        {
                            "nome": disciplina.get_attribute("title").strip(),
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
                self.logger.info(f"Disciplina encontrada: '{info['nome']}'")

            self._save_screenshot("disciplinas_encontradas")

        except NoSuchElementException:
            self.logger.exception("Erro ao tentar encontrar os links e nomes das disciplinas")
            return []
        else:
            return disciplinas_filtradas

    def capture_subjects(self, disciplinas_info: list[dict[str, str | Any]]) -> None:
        """Acessa cada disciplina e tira uma captura de tela."""
        # Itera sobre cada disciplina
        for disciplina in disciplinas_info:
            try:
                # Acessa a página da disciplina
                self.logger.info(f"Acessando a disciplina: {disciplina['nome']}")
                self.driver.get(disciplina["link"])
                self.driver.implicitly_wait(5)

                # Salva a captura de tela da disciplina
                screenshot_filename = f"{disciplina['nome'].replace(' ', '_')}"
                self._save_screenshot(screenshot_filename)
                self.logger.info(f"Captura de tela da disciplina '{disciplina['nome']}' salva.")

            # Trata exceções de elementos não encontrados
            except NoSuchElementException:
                self.logger.exception(f"Erro ao tentar acessar a disciplina '{disciplina['nome']}'")

            # Trata exceções de runtime
            except RuntimeError:
                self.logger.exception(f"Erro ao acessar a disciplina '{disciplina['nome']}'")

    def fetch_subjects_information(
        self,
        disciplinas_info: list[dict[str, str | Any]],
        atividades_ignoradas: list[str | Any],
    ) -> dict[str, str | list[dict[str, str]]]:
        """Captura informações de cada disciplina e as salva em um JSON."""
        # Itera sobre cada disciplina para capturar suas informações
        informacoes_disciplinas: dict[str, Any] = {}
        for disciplina in disciplinas_info:
            try:
                # Acessa a página da disciplina
                self.logger.debug(f"Capturando informações da disciplina: {disciplina['nome']}")
                self.driver.get(disciplina["link"])
                self.driver.implicitly_wait(5)

                # Encontra os elementos das atividades na página da disciplina
                atividades_elements = self.driver.find_elements(
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
                        if any(ignorada in tipo_atividade for ignorada in atividades_ignoradas):
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
                self.logger.info(f"Informações da disciplina '{disciplina['nome']}' capturadas.")
            except RuntimeError:
                self.logger.exception(
                    f"Erro ao capturar informações da disciplina '{disciplina['nome']}'"
                )

        return informacoes_disciplinas

    def _convert_json_to_yaml(self, json_filepath: PathLike, yml_filepath: PathLike) -> None:
        """Converte um arquivo JSON para YML."""
        yml_filepath = Path(yml_filepath)
        json_filepath = Path(json_filepath)
        data = super()._load_file(json_filepath)

        with yml_filepath.open("w", encoding="utf-8") as yml_file:
            yaml.dump(data, yml_file, allow_unicode=True, default_flow_style=False)

        self.logger.info(f"Arquivo YML salvo em '{yml_filepath}'.")

    def _ensure_string(self, template: str, **kwargs: str) -> str:
        """Garante que o template é string antes de aplicar .format."""
        if not isinstance(template, str):
            template = str(template)
        return template.format(**kwargs)

    def _generate_ics_file(
        self,
        informacoes: dict[str, Any],
        template_path: PathLike,
        output_path: PathLike,
        config: dict[str, Any],
    ) -> None:
        """Gera um arquivo .ics a partir das informações das disciplinas."""
        # Carrega o template do arquivo .ics
        template_dict: dict[str, str] = super()._load_file(template_path)
        # Extrai o conteúdo do template ICS
        template = template_dict["ics_content"].strip()

        # Obtém apenas o cabeçalho
        header, event_template = template.split("BEGIN:VEVENT", 1)
        event_template = "BEGIN:VEVENT" + event_template
        header = self._ensure_string(
            header,
            nome_aluno=config["nome_aluno"],
            semestre=config["semestre"],
            nome_curso=config["nome_curso"],
        ).strip()  # Remove espaços em branco no início e no fim

        eventos = []

        # Itera sobre as disciplinas e atividades
        for disciplina, dados in informacoes.items():
            for atividade in dados["atividades"]:
                nome_atividade = atividade["nome_atividade"]
                periodo = str(atividade["periodo"]).split(" - ")
                inicio = self._convert_ics_date(periodo[0].replace("/", ""))
                fim = self._convert_ics_date(periodo[1].replace("/", ""))

                # Adiciona evento de início
                eventos.append(
                    self._ensure_string(
                        event_template,
                        tipo_periodo="Início",
                        nome_atividade=nome_atividade,
                        data_periodo=inicio,
                        disciplina=disciplina,
                    )
                )

                if inicio != fim:
                    eventos.append(
                        self._ensure_string(
                            event_template,
                            tipo_periodo="Fim",
                            nome_atividade=nome_atividade,
                            data_periodo=fim,
                            disciplina=disciplina,
                        )
                    )

        ics_content = f"{header}\n" + "\n".join(eventos) + "\nEND:VCALENDAR\n"

        with output_path.open("w", encoding="utf-8") as ics_file:
            ics_file.write(ics_content)

        self.logger.info(f"Informações salvas em ICS: '{output_path}'")

    def export_information(self, informacoes: dict[str, str | Any], config: dict[str, Any]) -> None:
        """Salva as informações das disciplinas em arquivos JSON, YAML e ICS."""
        # Salva as informações em formato JSON
        with self.json_filepath.open("w", encoding="utf-8") as json_file:
            json.dump(informacoes, json_file, ensure_ascii=False, indent=4)

        # Salva as informações em formato YAML
        with self.yml_filepath.open("w", encoding="utf-8") as yml_file:
            yaml.dump(informacoes, yml_file, allow_unicode=True, default_flow_style=False)

        # Gera o arquivo ICS com base nas informações e no template
        self._generate_ics_file(informacoes, self.ics_template_filepath, self.ics_filepath, config)

        # Loga as informações dos arquivos salvos
        self.logger.info(f"Informações salvas em JSON: '{self.json_filepath}'")
        self.logger.info(f"Informações salvas em YAML: '{self.yml_filepath}'")

    def _shutdown_resources(self) -> None:
        """Encerra todos os recursos abertos (WebDriver, pools, etc.) de forma segura."""
        # Encerra o WebDriver, se estiver ativo
        if getattr(self, "driver", None):
            try:
                self.logger.info("Encerrando o WebDriver...")
                self.driver.quit()
            except Exception:
                self.logger.exception("Erro ao encerrar o WebDriver.")
            finally:
                self.driver = None

    def run_workflow(self) -> None:
        """Executa o fluxo principal do script."""
        try:
            # Configura o WebDriver
            self.driver = self._setup_webdriver()

            # Define o diretório de imagens com base no modo de perfil
            if PROFILE_MODE == "debug":
                timestamp = datetime.now(tz=BRT).strftime("%Y%m%d_%H%M%S")
                self.image_folder = self.image_folder / timestamp
                self.image_folder.mkdir(parents=True, exist_ok=True)
            else:
                self.image_folder = self.image_folder

            # Realiza o login no portal
            self.portal_login(
                self.settings["usuario"],
                self.settings["senha"],
            )

            # Acessa o curso especificado
            self.access_course(self.settings["nome_curso"])

            # Encontra as disciplinas disponíveis
            disciplinas_info = self.find_subjects(
                self.settings["colaborar_index_url"],
                self.settings["matricula"],
            )

            # Captura as disciplinas, se em modo "debug"
            if PROFILE_MODE == "debug":
                for disciplina in disciplinas_info:
                    self.capture_subjects([disciplina])

            # Captura as informações das disciplinas
            informacoes_disciplinas = self.fetch_subjects_information(
                disciplinas_info,
                self.settings.get("atividades_ignoradas", []),
            )

            # Exporta as informações das disciplinas
            self.export_information(informacoes_disciplinas, self.settings)
        except KeyboardInterrupt:
            self.logger.warning("Script interrompido pelo usuário.")
        except ProjectError:
            self.logger.exception("Erro durante a execução do pipeline.")
            raise
        finally:
            if PROFILE_MODE == "debug" and self.driver and self.image_folder:
                self._save_screenshot("final_state")
            self._shutdown_resources()
            super()._separator_line()
            echo(
                f"Pipeline finalizado com sucesso. Resultado salvo em: '{self.output_path}'",
                "success",
            )
