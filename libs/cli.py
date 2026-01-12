#!/usr/bin/env python3
"""
Interface de linha de comando para o sistema de boletos Cora.
"""

import argparse
import sys
import yaml
from pathlib import Path
from .auth import CoraAuth
from .gerador import GeradorBoletos


def main():
    """Função principal do CLI."""
    parser = argparse.ArgumentParser(
        description="Sistema de geração de boletos Cora",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  cora-boletos --config config.yaml --excel clientes.xlsx
  cora-boletos --config config.yaml --individual '{"nome": "João", "valor": 100}'
  cora-boletos --config config.yaml --test
        """
    )
    
    parser.add_argument(
        "--config", "-c",
        default="config.yaml",
        help="Arquivo de configuração (padrão: config.yaml)"
    )
    
    parser.add_argument(
        "--excel", "-e",
        help="Arquivo Excel com dados dos boletos"
    )
    
    parser.add_argument(
        "--individual", "-i",
        help="Dados JSON para um boleto individual"
    )
    
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Executar teste de conectividade"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Modo verboso"
    )
    
    args = parser.parse_args()
    
    try:
        # Carregar configuração
        if not Path(args.config).exists():
            print(f"❌ Arquivo de configuração não encontrado: {args.config}")
            sys.exit(1)
        
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
        
        # Configurar autenticação
        auth = CoraAuth(
            auth_url=config['api']['auth_url'],
            client_id=config['credentials']['client_id'],
            cert_path=config['certificates']['cert_path'],
            key_path=config['certificates']['key_path']
        )
        
        # Criar gerador
        gerador = GeradorBoletos(
            api_url=config['api']['base_url'],
            auth=auth,
            debug=args.verbose
        )
        
        # Executar ação solicitada
        if args.test:
            print("🧪 Testando conectividade...")
            token = auth.get_access_token()
            print(f"✅ Token obtido: {token[:20]}...")
            print("✅ Conectividade OK!")
            
        elif args.excel:
            print(f"📊 Processando arquivo Excel: {args.excel}")
            resultados = gerador.gerar_boletos_em_lote(args.excel)
            print(f"✅ Boletos gerados: {len(resultados['sucessos'])}")
            print(f"❌ Erros: {len(resultados['erros'])}")
            
        elif args.individual:
            import json
            dados = json.loads(args.individual)
            print(f"📄 Gerando boleto individual...")
            resultado = gerador.gerar_boleto_individual(dados)
            print(f"✅ Boleto gerado: {resultado.get('id', 'N/A')}")
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()