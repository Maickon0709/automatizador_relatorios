"""
conftest.py

Garante que os módulos do projeto (leitor, processador, banco, relatorio)
sejam encontrados pelo pytest, mesmo os testes estando numa subpasta
'tests/'.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
