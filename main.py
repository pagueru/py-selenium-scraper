"""Função principal que executa o fluxo do script."""

from src.common.echo import echo
from src.pipeline.selenium_scraper_pipeline import SeleniumScraperPipeline

# start_time = time.time()
try:
    scraper = SeleniumScraperPipeline(show_browser=False)
    scraper.run_workflow()
except RuntimeError:
    echo("Ocorreu um erro", "error")
except KeyboardInterrupt:
    echo("Script interrompido pelo usuário.", "warning")
finally:
    echo("Script finalizado.", "info")
    # execution_time(start_time)
    # terminal_line()
