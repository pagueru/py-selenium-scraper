# py-selenium-scraper

Automatização de acesso à plataforma Colaborar da Anhanguera para exportar datas de atividades em formato iCalendar (ICS) usando Selenium.

<p align="center">
  <img alt="Overview" src="./data/images/overview.gif" width="90%" />
</p>

[![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=flat&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Anhanguera](https://img.shields.io/badge/Anhanguera-FF6F00?style=flat&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAB10lEQVR4nI1RvWtTcRQ99/7ee/lotUlAFKqDWAURFxEdtJugs/QPEMGlDqKDXdwVcdK/Qaibg5MgiIiIZrKiGJrEGLXW5tPG8PLe797rIqWhrXjWc849nHOBHeBb9cvWrp3fid8WVq8XpPO56Xu1F+VyOfxvo+82rpu1zYZNSzrVs9tpaEvaenWveHlJYW6JBc/h0xWUOo+JTqabdbzl1NDNIInus9gHJZuXKPMI3eKFf3czI9+pzsvgS9PSH2bxdzNrmbQrZatUMpu1wZizW7vqipMPoAT5NVBnaCBO3kGwjN2uAGB1S0drfZoWF75yUfhV1T9jcU9GQx2EufQmR9nDGsdtLs1cJCI/lphIuschvAe4febjJhUPvjH7lte+P4V8/ihHAaRfnQOwuDGOrX3cFUSFS24iuKUSL4jxawAgmh6yhgs6iFeQ+GUSPj22qlB4gwuFawBPQdztTOnQkpmFv1vN/XDaMtU7GuMhu5wmncYsAJCtvp/UbP4ugok1Ho1+iuMckZxgwzE1OgBLpzhgRhAAmSyS/no56jVmKe01zjG5Obb0jBAdcdkwAhwgKSAKGAAoYAbA/aXsCvl+/a1zwXEV7wF4M9uY2sZ+RSAjcMSkI3n6B93+8tgmpT2yAAAAAElFTkSuQmCC)](https://www.anhanguera.com/)
[![Colaborar](https://img.shields.io/badge/Colaborar-FDFCFB?style=flat&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAMAAAAolt3jAAAA0lBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIjMALTwAGygAM0AAM00AM0cALEYARF0AITEAJTUAIzIAOVUAPloAJzQAQFkAIjMAJTUAJDQAOFIAQ2AAT28AYYgAZokAX40AYYoAYY0AY4wAb6MAaZYAjL4Ahr4AhsIAfrEAibwAm9MAj9MAjMgAk9QAnucAoucAouYApOcAouUAn+IApOsApesArfIAqfIAqfIAqvIAqvIAqvIAqvMAqvIAqvIAqvIAqvIAqvIAqvIAqvIAqvIAqvIOQNevAAAARXRSTlMAAQIDBAYJCg8RExQUGR0eHyIkJCUnKC0wMTI1NzpBQ0xMUFNhcXZ2fX2KkpWZsbK0uLrMz9zl6Ors7vT19vf4+fr7/P3k6244AAAAiUlEQVQIW2XORxbCMAxFUZvQeyfU0HvvAQOxLO1/S2B7Aoc3u0cafMb+CuVrtqhWei1ASgAI3I+cDd0XXnt8JtQsPEWPp3K8fDJ0ccWHvlg2pspQ9eMX0tmr6ib8L+KcTR6w7czsM96avNqKJA+voiFdR6Xs4Eg7RxMQUUoV7DN6VKxuq4TN4p/e/gAWAfnkAFcAAAAASUVORK5CYII=)](https://www.colaboraread.com.br/login/auth)

---

## Sobre o Projeto

Este projeto tem como objetivo aprofundar conhecimentos em Python, Selenium e boas práticas de organização e documentação, por meio do desenvolvimento de uma aplicação para automatizar o acompanhamento das pendências do meu curso. Utilizando Selenium, a aplicação acessa o ambiente acadêmico, extrai as informações relevantes e as organiza em um arquivo ICS (iCalendar) para importar para o Google Calendar.

### Principais aprendizados

- **Selenium**: Manipulação de elementos, tratamento de exceções e boas práticas em automação.
- **Organização**: Estruturação modular e reutilização de código.
- **Documentação**: Registro claro das etapas para facilitar manutenção.
- **Boas Práticas**: Código limpo, manipulação de dados e verificações de tipo.

## Requisitos

- [Python](https://www.python.org/downloads/)
- [Pyenv](https://pypi.org/project/pyenv/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

Para usar este projeto, recomenda-se o `Pyenv` para gerenciar versões do Python e o `uv` para as dependências do `pyproject.toml`. Ambos são opcionais, pois você pode usar a versão do Python do sistema e instalar dependências via `pip` com o `requirements.txt`.

## Configuração do Projeto

### 1. Clonando o Repositório

Para começar, clone o repositório do projeto:

```bash
git clone https://github.com/pagueru/py-selenium-scraper
cd py-selenium-scraper
```

### 2. Preparando o Ambiente de Desenvolvimento

O projeto requer a versão 3.12.7 do Python:

```bash
pyenv update
pyenv install 3.12.7
pyenv local 3.12.7
```

Configure o Poetry para gerenciar as dependências do projeto:

```bash
poetry env use 3.12.7
poetry shell
poetry install
```

## 3. Personalizando o Arquivo de Configuração

Renomeie o arquivo `config_template.yml` para `config.yml` com suas informações:

  ```yaml
  # Configurações do ambiente
  profile_mode: info

  # Caminho do ChromeDriver
  chromedriver: C:\caminho\para\chromedriver.exe

  # Data de acesso ao portal
  usuario: SEU_CPF
  senha: SUA_SENHA

  # Informações do aluno
  matricula: SUA_MATRICULA

  # Informações do curso
  nome_curso: NOME_DO_CURSO
  semestre: 1o
  nome_aluno: SEU_NOME

  # URL's do portal
  colaborar_url: https://www.colaboraread.com.br/login/auth
  colaborar_index_url: https://www.colaboraread.com.br/aluno/timeline/index

  # Atividades ignoradas
  atividades_ignoradas: [
    Conteúdo WEB,
    Leitura,
    Engajamento AVA,
    Teleaula,
    Live
  ]
  ```

## 4. Executando o Projeto

  Como o projeto utiliza `[tool.poetry.scripts]` no arquivo `pyproject.toml`, você pode executar o script diretamente utilizando `poetry run main`

  ```bash
  poetry run main
  ```

  ou

  ```bash
  poetry run python src/main.py
  ```

<p align="center">
  <img alt="Poetry Run" src="./data/images/poetry_run_main.gif" width="90%" />
</p>

O script acessa o portal e exporta as atividades para um arquivo ICS. Os dados gerados também estarão disponíveis em JSON e YAML para melhor visualização.

Abaixo está um exemplo de como os dados são organizados no formato YAML, com detalhes sobre as atividades, períodos e tipos de tarefas:

```plaintext
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Raphael Coelho//5o Superior de Tecnologia em Inteligência \
de Mercado e Análise de Dados//PT-BR
BEGIN:VEVENT
SUMMARY:Início Relatório de Aula Prática - Web Analytics
DTSTART;VALUE=DATE:20250203
DESCRIPTION:Atividade da disciplina Web Analytics
END:VCALENDAR
```

- O campo `PRODID` foi quebrado para melhor visualização.

### Exemplos de Retornos

<details><summary>Formato YAML</summary>

```yaml
Web Analytics:
  atividades:
  - nome_atividade: Relatório de Aula Prática - Web Analytics
    periodo: 03/02/25 - 17/05/25
    tipo_atividade: Portfólio
  - nome_atividade: Av1 - Web Analytics
    periodo: 14/04/25 - 26/05/25
    tipo_atividade: Avaliação Virtual
  - nome_atividade: Av2 - Web Analytics
    periodo: 14/04/25 - 02/06/25
    tipo_atividade: Avaliação Virtual
  - nome_atividade: Av - Subst. 1 - Web Analytics
    periodo: 03/06/25 - 07/06/25
    tipo_atividade: Avaliação Virtual
  - nome_atividade: Av - Subst. 2 - Web Analytics
    periodo: 03/06/25 - 07/06/25
    tipo_atividade: Avaliação Virtual
  - nome_atividade: Prova Presencial - 1º Chamada - Web Analytics
    periodo: 24/05/25 - 31/05/25
    tipo_atividade: Prova Presencial da Disciplina
  - nome_atividade: Prova Presencial - 2º Chamada - Web Analytics
    periodo: 09/06/25 - 14/06/25
    tipo_atividade: Prova Presencial da Disciplina
  - nome_atividade: Prova Presencial - Recuperação - Web Analytics
    periodo: 16/06/25 - 21/06/25
    tipo_atividade: Prova Presencial da Disciplina
  link_disciplina: https://www.colaboraread.com.br/aluno/timeline/index/XXXXXXXXXX?ofertaDisciplinaId=XXXXXXX
```

</details>

<details><summary>Formato JSON</summary>

```json
"Web Analytics": {
        "link_disciplina": "https://www.colaboraread.com.br/aluno/timeline/index/XXXXXXXXXX?ofertaDisciplinaId=XXXXXXX",
        "atividades": [
            {
                "nome_atividade": "Relatório de Aula Prática - Web Analytics",
                "tipo_atividade": "Portfólio",
                "periodo": "03/02/25 - 17/05/25"
            },
            {
                "nome_atividade": "Av1 - Web Analytics",
                "tipo_atividade": "Avaliação Virtual",
                "periodo": "14/04/25 - 26/05/25"
            },
            {
                "nome_atividade": "Av2 - Web Analytics",
                "tipo_atividade": "Avaliação Virtual",
                "periodo": "14/04/25 - 02/06/25"
            },
            {
                "nome_atividade": "Av - Subst. 1 - Web Analytics",
                "tipo_atividade": "Avaliação Virtual",
                "periodo": "03/06/25 - 07/06/25"
            },
            {
                "nome_atividade": "Av - Subst. 2 - Web Analytics",
                "tipo_atividade": "Avaliação Virtual",
                "periodo": "03/06/25 - 07/06/25"
            },
            {
                "nome_atividade": "Prova Presencial - 1º Chamada - Web Analytics",
                "tipo_atividade": "Prova Presencial da Disciplina",
                "periodo": "24/05/25 - 31/05/25"
            },
            {
                "nome_atividade": "Prova Presencial - 2º Chamada - Web Analytics",
                "tipo_atividade": "Prova Presencial da Disciplina",
                "periodo": "09/06/25 - 14/06/25"
            },
            {
                "nome_atividade": "Prova Presencial - Recuperação - Web Analytics",
                "tipo_atividade": "Prova Presencial da Disciplina",
                "periodo": "16/06/25 - 21/06/25"
            }
        ]
    }
```

</details>

## Contato

GitHub: [pagueru](https://github.com/pagueru/)

LinkedIn: [Raphael Coelho](https://www.linkedin.com/in/raphaelhvcoelho/)

E-mail: [raphael.phael@gmail.com](mailto:raphael.phael@gmail.com)
