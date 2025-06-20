"""
Configuração do pytest para os testes do sistema de geração de boletos Cora.
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH para importar os módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configurações do pytest
def pytest_configure(config):
    """Configurações adicionais do pytest"""
    # Adiciona marcadores personalizados
    config.addinivalue_line(
        "markers", "unit: marca testes unitários"
    )
    config.addinivalue_line(
        "markers", "integration: marca testes de integração"
    )
    config.addinivalue_line(
        "markers", "validation: marca testes de validação"
    )

def pytest_collection_modifyitems(config, items):
    """Modifica itens de teste durante a coleta"""
    for item in items:
        # Adiciona marcador padrão para testes de validação
        if "validacao" in item.name.lower() or "validation" in item.name.lower():
            item.add_marker("validation")
        # Adiciona marcador padrão para testes unitários
        elif "test_" in item.name.lower():
            item.add_marker("unit") 