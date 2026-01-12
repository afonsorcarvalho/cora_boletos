"""
Módulo de verificação e configuração automática.
Usado pelo app.py para verificar se tudo está configurado.
"""

import os
import sys
import subprocess
from pathlib import Path


def verificar_dependencias():
    """Verifica se as dependências necessárias estão instaladas."""
    dependencias = {
        'flask': 'Flask',
        'yaml': 'PyYAML',
        'dotenv': 'python-dotenv',
        'requests': 'requests'
    }
    
    faltando = []
    for modulo, nome in dependencias.items():
        try:
            __import__(modulo)
        except ImportError:
            faltando.append(nome)
    
    return faltando


def criar_env_se_nao_existe():
    """Cria o arquivo .env se não existir."""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        return True
    
    if env_example.exists():
        try:
            import shutil
            shutil.copy(env_example, env_file)
            return True
        except Exception:
            pass
    
    # Criar .env básico
    try:
        with open(env_file, 'w') as f:
            f.write("""# Configuração da Aplicação Web
PORT=5000
HOST=0.0.0.0
DEBUG=false
SECRET_KEY=change-this-secret-key-in-production
CONFIG_FILE=config.yaml
""")
        return True
    except Exception:
        return False


def verificar_configuracao_basica():
    """
    Verifica se a configuração básica está presente.
    Retorna (ok, mensagens)
    """
    mensagens = []
    ok = True
    
    # Verificar .env
    if not Path('.env').exists():
        if criar_env_se_nao_existe():
            mensagens.append("✅ Arquivo .env criado automaticamente")
        else:
            mensagens.append("⚠️  Não foi possível criar arquivo .env")
    
    # Verificar config.yaml
    if not Path('config.yaml').exists():
        ok = False
        mensagens.append("❌ Arquivo config.yaml não encontrado. Configure antes de executar.")
    
    # Verificar dependências
    dependencias_faltando = verificar_dependencias()
    if dependencias_faltando:
        ok = False
        mensagens.append(f"❌ Dependências faltando: {', '.join(dependencias_faltando)}")
        mensagens.append("   Execute: pip install -r requirements.txt")
    
    return ok, mensagens


def tentar_instalar_dependencias_faltantes():
    """Tenta instalar dependências faltantes."""
    dependencias_faltando = verificar_dependencias()
    if not dependencias_faltando:
        return True
    
    try:
        print("📦 Tentando instalar dependências faltantes...")
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            check=True,
            capture_output=True
        )
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências automaticamente")
        print("   Execute manualmente: pip install -r requirements.txt")
        return False
    except Exception:
        return False
