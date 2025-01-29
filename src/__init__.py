# ./src/__init__.py

import sys
from pathlib import Path

# Adiciona o caminho do diretório 'src' ao sys.path
src_path = Path("./src").resolve()
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))
