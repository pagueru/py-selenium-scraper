# copilot-instructions.md

## Diretrizes de Uso de Ferramentas e Fluxo de Trabalho

* Utilize todas as ferramentas disponíveis (Prompt Boost, Sequential Thinking, Brave Search, Knowledge Graph) conforme necessário, sem exigir ativação explícita.
* Majoritariamente inicie cada nova conversa com Sequential Thinking (`#sequentialthinking`) para definir as ferramentas necessárias.
* Antes de iniciar qualquer execução ou raciocínio pelo Sequential Thinking, **sempre aplique o Prompt Boost** para aprimorar e refinar automaticamente o prompt inicial. Utilize o Prompt Boost como camada intermediária obrigatória para potencializar a clareza, eficiência e qualidade do processo de resolução. **Somente após o refinamento pelo Prompt Boost, prossiga com a divisão em etapas e execução normal do Sequential Thinking.**

### Fluxo de Trabalho Principal

1. **Análise Inicial (Sequential Thinking):**
    * Divida tarefas complexas (com múltiplos passos, dependências ou que exijam pesquisa externa) em etapas gerenciáveis, documente o processo de pensamento e permita revisões/ramificações.
    * Divida a consulta em componentes principais, conceitos e relações-chave.
    * Planeje a estratégia de pesquisa e verificação, definindo as ferramentas para cada etapa.
    * **Exemplo:** Para criar uma função que lê um arquivo CSV e retorna um dicionário:
        1. **Identificar objetivo:** Criar função `ler_csv_para_dict`.
        2. **Listar etapas:**
            * Pesquisar como ler arquivos CSV em Python. (Brave Search)
            * Pesquisar como criar dicionários em Python. (Brave Search)
            * Definir a estrutura do dicionário de saída.
            * Implementar a função.
            * Testar a função com um arquivo CSV de exemplo.
        3. **Definir ferramenta para cada etapa:** Brave Search para pesquisa, Python para implementação e teste.
        4. **Executar e revisar:** Implementar, testar e ajustar o código conforme necessário.

2. **Pesquisa e Verificação (Brave Search):**
    * Realize pesquisas amplas e direcionadas, controlando volume (count, offset) e documentando consultas, URLs, títulos, datas e descrições.
    * Navegue em sites relevantes, tire capturas de tela (sempre com URL e data/hora), extraia dados, explore links e registre caminhos de interação.
    * Repita etapas de verificação se necessário.
    * Exemplo de citação:
        * "Como usar o pathlib em Python", <https://docs.python.org/3/library/pathlib.html>, acesso em 02/05/2025.

3. **Processamento e Armazenamento (Knowledge Graph):**
    * Analise e processe os dados coletados, crie visualizações se útil e armazene descobertas importantes no Knowledge Graph, mantendo links e contexto das fontes para reutilização futura. **O Knowledge Graph é crucial para reter aprendizados e acelerar futuras análises.**
    * Siga estes passos para cada interação:
        1. **Identificação do Usuário:**
            * Considere que está interagindo com default_user.
            * Caso ainda não tenha identificado default_user, tente fazê-lo proativamente.
        2. **Recuperação de Memória:**
            * Sempre inicie o chat dizendo apenas "Lembrando..." e recupere todas as informações relevantes da sua memória (Knowledge Graph).
            * Sempre se refira ao Knowledge Graph como sua "memória".
        3. **Memória:**
            * Durante a conversa, esteja atento a qualquer nova informação que se enquadre nas seguintes categorias:
                a) Identidade básica (idade, gênero, localização, cargo, nível educacional, etc.)
                b) Comportamentos (interesses, hábitos, etc.)
                c) Preferências (estilo de comunicação, idioma preferido, etc.)
                d) Objetivos (metas, aspirações, etc.)
                e) Relacionamentos (relações pessoais e profissionais até 3 graus de separação)
        4. **Atualização de Memória:**
            * Se alguma nova informação for obtida durante a interação, atualize sua memória da seguinte forma:
                a) Crie entidades para organizações recorrentes, pessoas e eventos significativos.
                b) Conecte-as às entidades atuais usando relações.
                c) Armazene fatos sobre elas como observações.

4. **Síntese e Apresentação:**
    * Estruture e combine informações de todas as ferramentas, incluindo os refinamentos realizados pelo Prompt Boost, apresente resultados de forma clara, destaque insights e gere artefatos (código, visualizações, documentos) conforme necessário.
    
### Documentação e Rastreabilidade

* Todas as fontes devem ser citadas com URLs completas, títulos, datas e metadados (evite repetir esta orientação em outras seções).
* Capturas de tela devem conter URL de origem e carimbo de data/hora.
* Descobertas devem ser rastreáveis até as fontes originais.
* O Knowledge Graph deve manter links e contexto das fontes para reutilização futura.
* Documente cada etapa da análise em comentários ou docstrings, conforme apropriado, incluindo a versão refinada do prompt obtida via Prompt Boost, quando aplicável.
* Use ferramentas proativamente e, quando apropriado, em paralelo (não repita esta orientação em outras seções). **Por exemplo, iniciar uma pesquisa com Brave Search enquanto analisa dados previamente armazenados no Knowledge Graph.**
* Tarefas complexas são aquelas que envolvem múltiplos passos, dependências externas ou pesquisa; acione o fluxo de trabalho completo nesses casos.
* Gerencie a retenção de conhecimento entre conversas via Knowledge Graph.

## Prompt Boost — Refinamento de Prompts

* Antes de qualquer execução de raciocínio estruturado (Sequential Thinking), **sempre aplique o Prompt Boost** para otimizar a clareza e a qualidade do prompt.

* O Prompt Boost atua como uma camada intermediária essencial, aprimorando a formulação inicial das consultas e instruções, potencializando a precisão e a eficiência das respostas.

* Para utilizar o Prompt Boost no VS Code, configure e ative a extensão conforme a documentação oficial:

  * [Prompt Boost — VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=chrisdias.promptboost)
  * [Repositório oficial](https://github.com/chrisdias/vscode-promptboost)

* Após o refinamento via Prompt Boost, siga com o fluxo normal: Sequential Thinking → Brave Search → Knowledge Graph → Síntese.

* **Importante:** Nunca omita o uso do Prompt Boost, mesmo em tarefas aparentemente simples. A camada de otimização é indispensável para garantir qualidade e eficiência.

## Diretrizes de Código e Estruturação de Projetos

Projetos em Python devem seguir as **Python Enhancement Proposals (PEPs)**, as convenções oficiais de nomenclatura, tipagem e estilo, além das melhores práticas da linguagem. Para garantir qualidade, manutenibilidade e legibilidade do código, recomenda-se aderir às diretrizes suportadas pelo `ruff`, que automatiza e reforça esses padrões. Entre as principais estão:

1. **PEP 8 – Style Guide for Python Code**
   Guia oficial para estilo e formatação de código Python, cobrindo indentação, espaçamento, nomes de variáveis, comprimentos de linha, entre outros.
   *Referência:* [https://peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)

2. **PEP 257 – Docstring Conventions**
   Convenções para escrita e padronização de docstrings em Python, incluindo formatos para funções, classes e módulos.
   *Referência:* [https://peps.python.org/pep-0257/](https://peps.python.org/pep-0257/)

3. **PEP 484 – Type Hints**
   Introduz o sistema de tipagem estática opcional para Python, com anotações de tipo para variáveis, funções e retornos.
   *Referência:* [https://peps.python.org/pep-0484/](https://peps.python.org/pep-0484/)

4. **PEP 563 – Postponed Evaluation of Annotations**
   Adia a avaliação das anotações de tipo para evitar importações circulares e melhorar a performance, agora padrão no Python 3.10+.
   *Referência:* [https://peps.python.org/pep-0563/](https://peps.python.org/pep-0563/)

5. **PEP 3107 – Function Annotations**
   Define a sintaxe para anotações em funções, que embasam o sistema de tipos.
   *Referência:* [https://peps.python.org/pep-3107/](https://peps.python.org/pep-3107/)

6. **Google Docstring Style Guide**
   Além do PEP 257, o estilo Google para docstrings é amplamente adotado em projetos Python, principalmente por clareza e suporte em ferramentas.
   *Referência:* [https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

7. **Ruff — Linter e Formatter**
   Ferramenta rápida que implementa e reforça essas PEPs e outras boas práticas, incluindo detecção de problemas de código, segurança, complexidade e modernização com `pyupgrade`.
   *Referência:* [https://beta.ruff.rs/docs/](https://beta.ruff.rs/docs/)

---

### Linguagem, Nomeação e Documentação

* Escreva comentários, commits e docstrings em **português do Brasil**.
* Nomeie variáveis, funções, classes e objetos similares em **inglês**.
* Docstrings devem ser escritas em linha única, na linguagem imperativa (ex: `"""Retorna o caminho absoluto do arquivo."""`).
* Arquivos `__init__.py` devem conter docstring de linha única descritiva no topo.
* Preserve todos os comentários e marcações TODO existentes ao alterar código.

---

### Tipagem e Estilo de Código

* Use `f-strings` para formatação de strings, ao invés de `%` ou `str.format`.
* Parâmetros booleanos em funções devem ser `keyword-only` (usando `*` na assinatura).
* Utilize tipagem explícita em variáveis, parâmetros e retornos:

  * Priorize tipos nativos (`str`, `int`, `list`, `dict` etc.).
  * Use o módulo `typing` somente quando necessário.

---

### Uso de Bibliotecas e Ferramentas

* Utilize `pathlib` para manipulação de arquivos e diretórios.
* Use o `logger` para registrar informações, avisos e erros:

  * Registre informações relevantes ao contexto da aplicação.
  * Utilize níveis adequados: `logger.info`, `logger.warning`, `logger.error`, etc.
  * Sempre registre exceções com `logger.exception`.
  * Nunca use diretamente o módulo `logging` (ex: `logging.info(...)`).
* Use `uv` para gerenciar dependências e ambientes virtuais (`uv add <dependência>`).

---

### Commits e Controle de Versão

* Siga o [padrão de commits convencionais](https://www.conventionalcommits.org/pt-br/v1.0.0/):

  * `init` (commit inicial)
  * `feat` (nova funcionalidade)
  * `fix` (correção de bug)
  * `update` (atualizações)
* Detalhe sempre as mudanças e seus motivos. Exemplos:

  * `feat: adiciona autenticação de usuário`
  * `fix: corrige erro de cálculo no relatório`

---

Aqui está uma versão revisada, clara, sucinta e estruturada do seu texto sobre boas práticas de fluxo e controle, com foco em legibilidade e uniformidade no estilo. Mantive seus exemplos e deixei as explicações objetivas:

---

### Convenções de Uso de Guard Clauses

* Evite `if` aninhados usando **guard clauses** que retornam ou lançam exceção imediatamente quando uma condição inviabiliza a execução do restante do código.

  ```python
  # Exemplo desejado
  def get_user_email(user):
      if user is None:
          return None
      if not user.is_active:
          return None
      return user.email

  # Exemplo indesejado
  def get_user_email(user):
      if user is not None:
          if user.is_active:
              return user.email
      return None

  ```

---

### Convenções de Tratamento de Exceções

* Use `logger.exception()` sem capturar a exceção explicitamente para garantir o stack trace completo.

  ```python
  # Exemplo desejado — com `logger`
  try:
      connect_to_db()
  except ConnectionError:
      logger.exception("Erro de conexão.")
      raise

  # Exemplo indesejado — com `logger`
  try:
      connect_to_db()
  except ConnectionError as e:
      logger.error(f"Erro de conexão: {e}")
  ```

* Caso identifique que padrão no script seja o uso de `echo`, capture a exceção como `e` e use interpolação para exibir mensagem detalhada.

  ```python
  # Exemplo desejado — com `echo`
  try:
      process_data()
  except ValueError as e:
      echo(f"Erro ao processar os dados: {e}", "error")
      raise

  # Exemplo indesejado — com `echo`
  try:
      process_data()
  except ValueError:
      echo("Erro ao processar os dados", "error")
  ```

---

### Convenção de Acesso a Dicionários

* Sempre prefira o acesso direto por chave (`config["key"]`) ao invés do método `get("key", default)` quando a presença da chave for **obrigatória** ou esperada pelo fluxo normal.

* O método `get` só deve ser utilizado quando:
  * A chave for **opcional**.
  * Houver necessidade explícita de definir um valor padrão.

* Exemplo:

  ```python
  # Exemplo desejado — quando a chave é obrigatória
  self.dataset_name = dataset_config["dataset_name"]

  # Exemplo indesejado — evita mascarar ausência de chave obrigatória
  self.dataset_name = dataset_config.get("dataset_name", "")
  ```