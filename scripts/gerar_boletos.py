import pandas as pd
import requests
import uuid
import logging
import os
import json
import yaml
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv
from libs.auth import CoraAuth
from libs.gerador import GeradorBoletos


# Configuração global do logging
def configurar_logging(debug: bool = False):
    """
    Configura o sistema de logging.
    
    Args:
        debug (bool): Se True, habilita logs de debug
    """
    # Remove handlers existentes
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Define o nível de log
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Configura o formato do log
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Configura o handler do arquivo
    file_handler = logging.FileHandler('boletos.log')
    file_handler.setFormatter(logging.Formatter(log_format))
    file_handler.setLevel(log_level)
    
    # Configura o handler do console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setLevel(log_level)
    
    # Configura o logger root
    logging.root.setLevel(log_level)
    logging.root.addHandler(file_handler)
    logging.root.addHandler(console_handler)
    
    if debug:
        logging.debug("Sistema de logging configurado em modo DEBUG")
    else:
        logging.info("Sistema de logging configurado em modo INFO")

def carregar_configuracao(config_path: str = 'config.yaml') -> dict:
    """
    Carrega as configurações do arquivo YAML.
    
    Args:
        config_path (str): Caminho para o arquivo de configuração
        
    Returns:
        dict: Dicionário com as configurações carregadas
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            logging.info(f"Configurações carregadas de: {config_path}")
            return config
    except Exception as e:
        logging.error(f"Erro ao carregar arquivo de configuração: {str(e)}")
        raise

if __name__ == "__main__":
    # Carrega configurações
    config = carregar_configuracao('config.yaml')
    
    # Configurações
    AUTH_URL = config['api']['auth_url']
    API_URL = config['api']['base_url']
    CLIENT_ID = config['credentials']['client_id']
    CERT_PATH = config['certificates']['cert_path']
    KEY_PATH = config['certificates']['key_path']
    EXCEL_FILE = config['config']['excel_file']
    DEBUG = config['config']['debug']  # Obtém configuração de debug
    
    # Configura o logging antes de qualquer operação
    configurar_logging(DEBUG)
    
    if DEBUG:
        logging.debug("Iniciando execução do script")
        logging.debug(f"Configurações carregadas:")
        logging.debug(f"AUTH_URL: {AUTH_URL}")
        logging.debug(f"API_URL: {API_URL}")
        logging.debug(f"CLIENT_ID: {CLIENT_ID}")
        logging.debug(f"CERT_PATH: {CERT_PATH}")
        logging.debug(f"KEY_PATH: {KEY_PATH}")
        logging.debug(f"EXCEL_FILE: {EXCEL_FILE}")
    
    # Inicializa autenticação
    auth = CoraAuth(AUTH_URL, CLIENT_ID, CERT_PATH, KEY_PATH, debug=DEBUG)
    
    # Inicializa o gerador de boletos com debug
    gerador = GeradorBoletos(API_URL, auth, debug=DEBUG)
    
    # Processa o arquivo Excel
    gerador.processar_arquivo(EXCEL_FILE) 