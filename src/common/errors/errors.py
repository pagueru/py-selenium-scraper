"""Este módulo define exceções personalizadas para o projeto."""


class ProjectError(Exception):
    """Exceção base para erros do projeto."""


class LoggerError(ProjectError):
    """Exceção para erros relacionados à configuração do logger."""
