"""
Cora Boletos - Sistema de geração automatizada de boletos.

Este pacote fornece uma interface completa para gerar boletos bancários
utilizando a API da Cora, com validações robustas e tratamento de erros.
"""

__version__ = "2.0.0"
__author__ = "Afonso Carvalho"
__email__ = "afonso@email.com"
__license__ = "MIT"

from libs.auth import CoraAuth
from libs.gerador import GeradorBoletos

__all__ = [
    "CoraAuth",
    "GeradorBoletos",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]