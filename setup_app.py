#!/usr/bin/env python3
"""
Script de instalação e configuração automática da aplicação web.
Verifica e configura tudo necessário para executar a aplicação.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_step(message):
    """Imprime uma mensagem de etapa."""
    print(f"\n{'='*60}")
    print(f"📋 {message}")
    print('='*60)


def print_success(message):
    """Imprime uma mensagem de sucesso."""
    print(f"✅ {message}")


def print_warning(message):
    """Imprime uma mensagem de aviso."""
    print(f"⚠️  {message}")


def print_error(message):
    """Imprime uma mensagem de erro."""
    print(f"❌ {message}")


def check_python_version():
    """Verifica a versão do Python."""
    print_step("Verificando versão do Python")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ é necessário. Versão atual: {version.major}.{version.minor}")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro} - OK")
    return True


def check_venv():
    """Verifica se estamos em um ambiente virtual."""
    print_step("Verificando ambiente virtual")
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if not in_venv:
        venv_path = Path('.venv')
        if venv_path.exists():
            print_warning("Ambiente virtual existe mas não está ativado.")
            print_warning("Execute: source .venv/bin/activate (Linux/Mac) ou .venv\\Scripts\\activate (Windows)")
            return False
        else:
            print_warning("Ambiente virtual não encontrado. Criando...")
            try:
                subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True)
                print_success("Ambiente virtual criado com sucesso!")
                print_warning("Ative o ambiente virtual e execute este script novamente:")
                print("  Linux/Mac: source .venv/bin/activate")
                print("  Windows: .venv\\Scripts\\activate")
                return False
            except subprocess.CalledProcessError as e:
                print_error(f"Erro ao criar ambiente virtual: {e}")
                return False
    else:
        print_success("Ambiente virtual ativo - OK")
        return True


def install_dependencies():
    """Instala as dependências do projeto."""
    print_step("Instalando dependências")
    requirements_file = Path('requirements.txt')
    
    if not requirements_file.exists():
        print_error("Arquivo requirements.txt não encontrado!")
        return False
    
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
            check=True,
            capture_output=True
        )
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            check=True
        )
        print_success("Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Erro ao instalar dependências: {e}")
        return False


def create_env_file():
    """Cria o arquivo .env se não existir."""
    print_step("Configurando arquivo .env")
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print_success("Arquivo .env já existe - OK")
        return True
    
    if env_example.exists():
        try:
            shutil.copy(env_example, env_file)
            print_success("Arquivo .env criado a partir de .env.example")
            print_warning("Edite o arquivo .env e configure SECRET_KEY e outras variáveis se necessário")
            return True
        except Exception as e:
            print_error(f"Erro ao criar arquivo .env: {e}")
            return False
    else:
        # Criar .env básico se .env.example não existir
        try:
            with open(env_file, 'w') as f:
                f.write("""# Configuração da Aplicação Web
PORT=5000
HOST=0.0.0.0
DEBUG=false
SECRET_KEY=change-this-secret-key-in-production
CONFIG_FILE=config.yaml
""")
            print_success("Arquivo .env criado com configurações padrão")
            print_warning("Edite o arquivo .env e configure SECRET_KEY e outras variáveis")
            return True
        except Exception as e:
            print_error(f"Erro ao criar arquivo .env: {e}")
            return False


def check_config_file():
    """Verifica se o arquivo config.yaml existe."""
    print_step("Verificando arquivo config.yaml")
    config_file = Path('config.yaml')
    
    if config_file.exists():
        print_success("Arquivo config.yaml encontrado - OK")
        return True
    else:
        print_warning("Arquivo config.yaml não encontrado")
        print_warning("Crie o arquivo config.yaml com as configurações da API Cora")
        print_warning("Veja examples/config.example.yaml para um exemplo")
        return False  # Não é crítico, apenas aviso


def create_directories():
    """Cria diretórios necessários."""
    print_step("Criando diretórios necessários")
    directories = ['certificados', 'templates']
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print_success(f"Diretório '{directory}' criado")
            except Exception as e:
                print_error(f"Erro ao criar diretório '{directory}': {e}")
                return False
        else:
            print_success(f"Diretório '{directory}' já existe - OK")
    
    return True


def verify_installation():
    """Verifica se a instalação está completa."""
    print_step("Verificando instalação")
    
    try:
        import flask
        print_success("Flask instalado - OK")
    except ImportError:
        print_error("Flask não está instalado")
        return False
    
    try:
        import yaml
        print_success("PyYAML instalado - OK")
    except ImportError:
        print_error("PyYAML não está instalado")
        return False
    
    try:
        from dotenv import load_dotenv
        print_success("python-dotenv instalado - OK")
    except ImportError:
        print_error("python-dotenv não está instalado")
        return False
    
    return True


def main():
    """Função principal do instalador."""
    print("\n" + "="*60)
    print("🚀 INSTALADOR - Aplicação Web Consulta de Boletos Cora")
    print("="*60)
    
    # Verificações básicas
    if not check_python_version():
        sys.exit(1)
    
    # Verificar ambiente virtual (não crítico, mas recomendado)
    check_venv()
    
    # Criar diretórios
    if not create_directories():
        sys.exit(1)
    
    # Instalar dependências
    if not install_dependencies():
        sys.exit(1)
    
    # Verificar instalação
    if not verify_installation():
        print_warning("Algumas dependências não estão instaladas. Tente executar: pip install -r requirements.txt")
        sys.exit(1)
    
    # Criar arquivo .env
    create_env_file()
    
    # Verificar config.yaml
    check_config_file()
    
    # Resumo final
    print("\n" + "="*60)
    print("✅ INSTALAÇÃO CONCLUÍDA!")
    print("="*60)
    print("\n📝 Próximos passos:")
    print("1. Configure o arquivo .env (especialmente SECRET_KEY)")
    print("2. Configure o arquivo config.yaml com suas credenciais da API Cora")
    print("3. Adicione seus certificados na pasta certificados/")
    print("4. Execute: python app.py")
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    main()
