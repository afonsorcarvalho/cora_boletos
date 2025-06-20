#!/usr/bin/env python3
"""
Script de exemplo que demonstra como gerar boletos passando os dados diretamente para o gerador,
sem necessidade de arquivo Excel.
"""

import os
import sys
import yaml
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.auth import CoraAuth
from libs.gerador import GeradorBoletos, BoletoData

def criar_dados_boleto() -> List[Dict[str, Any]]:
    """
    Cria uma lista de dados para geração de boletos.
    
    Returns:
        List[Dict[str, Any]]: Lista de dicionários com dados dos boletos
    """
    return [
        {
            "codigo": "BOL001",
            "nome": "João da Silva",
            "email": "joao@email.com",
            "documento": "356.490.490-50",
            "telefone": "(11) 98765-4321",
            "servico_nome": "Consultoria",
            "servico_descricao": "Consultoria mensal - Janeiro 2024",
            "valor": 1500.50,
            "data_vencimento": (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
            "juros_mensal": 2.5,  # 2.5% ao mês
            "multa": 10.00,  # R$ 10,00 de multa
        },
        {
            "codigo": "BOL002",
            "nome": "Empresa XYZ Ltda",
            "email": "financeiro@xyz.com.br",
            "documento": "12.345.678/0001-90",
            "telefone": "(11) 3333-4444",
            "servico_nome": "Desenvolvimento",
            "servico_descricao": "Desenvolvimento de sistema - Fase 1",
            "valor": 5000.00,
            "data_vencimento": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
            "juros_mensal": 1.0,  # 1% ao mês
            "multa": 50.00,  # R$ 50,00 de multa
        }
    ]

def carregar_config() -> Dict[str, Any]:
    """
    Carrega as configurações do arquivo config.yaml.
    
    Returns:
        Dict[str, Any]: Configurações carregadas
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
    
    if not os.path.exists(config_path):
        print(f"Erro: Arquivo de configuração não encontrado: {config_path}")
        print("Crie o arquivo config.yaml com as configurações necessárias")
        sys.exit(1)
        
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Verifica se os certificados existem
    cert_path = config.get('certificates', {}).get('cert_path')
    key_path = config.get('certificates', {}).get('key_path')
    
    if cert_path and not os.path.exists(cert_path):
        print(f"Aviso: Certificado não encontrado: {cert_path}")
        print("Crie o diretório 'certificados' e adicione os arquivos de certificado")
        
    if key_path and not os.path.exists(key_path):
        print(f"Aviso: Chave privada não encontrada: {key_path}")
        print("Crie o diretório 'certificados' e adicione os arquivos de certificado")
    
    return config

def main():
    """Função principal que demonstra o uso do gerador de boletos."""
    # Carrega configurações
    config = carregar_config()
    
    # Obtém configurações da API usando a estrutura correta do config.yaml
    api_config = config.get('api', {})
    credentials = config.get('credentials', {})
    certificates = config.get('certificates', {})
    
    client_id = credentials.get('client_id')
    cert_path = certificates.get('cert_path')
    key_path = certificates.get('key_path')
    api_url = api_config.get('base_url')
    auth_url = api_config.get('auth_url')
    
    if not all([client_id, cert_path, key_path, api_url]):
        print("Erro: Configurações da API incompletas no config.yaml")
        print("Verifique se as seguintes configurações estão presentes:")
        print("- credentials.client_id")
        print("- certificates.cert_path")
        print("- certificates.key_path")
        print("- api.base_url")
        sys.exit(1)
    
    try:
        # Inicializa autenticação
        auth = CoraAuth(
            auth_url=auth_url,
            client_id=client_id,
            cert_path=cert_path,
            key_path=key_path,
            debug=True
        )
        
        # Inicializa gerador
        gerador = GeradorBoletos(
            api_url=api_url,
            auth=auth,
            debug=True
        )
        
        # Obtém dados dos boletos
        dados_boletos = criar_dados_boleto()
        
        # Gera os boletos
        print("\nGerando boletos...")
        for dados in dados_boletos:
            print(f"\nProcessando boleto {dados['codigo']} para {dados['nome']}")
            
            try:
                # Cria o payload e envia para a API
                response = gerador.gerar_boleto_individual(dados)
                print(response)
                
                
            except Exception as e:
                print(f"Erro ao gerar boleto: {str(e)}")
                continue
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 