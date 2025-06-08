"""Função principal que executa o fluxo do script."""

from src.common.echo import echo
from src.pipeline.selenium_scraper_pipeline import SeleniumScraperPipeline

try:
    scraper = SeleniumScraperPipeline(show_browser=False)
    scraper.run_workflow()
except RuntimeError:
    echo("Ocorreu um erro", "error")
except KeyboardInterrupt:
    echo("Script interrompido pelo usuário.", "warn")
else:
    echo("Script finalizado.", "info")
