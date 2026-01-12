"""
Aplicação Flask para consulta de boletos do Cora.
Permite que clientes busquem e visualizem seus boletos através do navegador.
"""

import os
import sys
import logging
from pathlib import Path

# Carregar variáveis de ambiente do arquivo .env primeiro
from dotenv import load_dotenv
load_dotenv()

# Verificação e configuração automática (após carregar .env)
try:
    from lib_setup import criar_env_se_nao_existe
    
    # Criar .env se não existir
    criar_env_se_nao_existe()
    load_dotenv()  # Recarregar após criar .env
except ImportError:
    # Se lib_setup não existir, continua normalmente
    pass

# Importar módulos do Flask e da aplicação
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import yaml
from libs.auth import CoraAuth
from libs.consulta import ConsultaBoletos

# Configurar logging (será ajustado após carregar configuração)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Variável global para armazenar configuração de debug
debug_mode = False

def configurar_logging_debug(debug: bool):
    """
    Configura o nível de logging baseado no modo debug.
    
    Args:
        debug (bool): Se True, configura logging para DEBUG, senão INFO
    """
    global debug_mode
    debug_mode = debug
    
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Configurar nível para root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Configurar nível para todos os handlers existentes
    for handler in root_logger.handlers:
        handler.setLevel(log_level)
    
    # Configurar nível para logger específico
    logger.setLevel(log_level)
    
    # Configurar nível para loggers de bibliotecas usadas
    logging.getLogger('libs').setLevel(log_level)
    logging.getLogger('libs.auth').setLevel(log_level)
    logging.getLogger('libs.consulta').setLevel(log_level)
    logging.getLogger('urllib3').setLevel(log_level if debug else logging.WARNING)
    logging.getLogger('requests').setLevel(log_level if debug else logging.WARNING)
    
    if debug:
        logger.info("✅ Modo DEBUG ativado - Logs detalhados habilitados")
    else:
        logger.info("Modo INFO ativado - Apenas logs informativos")

# Criar aplicação Flask
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Variáveis globais para armazenar instâncias
consulta_boletos = None


def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF usando algoritmo oficial.
    
    Args:
        cpf: String com o CPF (com ou sem formatação)
        
    Returns:
        bool: True se o CPF for válido, False caso contrário
    """
    # Remove formatação
    cpf_clean = cpf.replace('.', '').replace('-', '').strip()
    
    # Verifica se tem 11 dígitos e se não são todos iguais
    if len(cpf_clean) != 11 or cpf_clean == cpf_clean[0] * 11:
        return False
    
    # Verifica se são apenas números
    if not cpf_clean.isdigit():
        return False
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf_clean[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf_clean[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    return cpf_clean[-2:] == f"{digito1}{digito2}"


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJ usando algoritmo oficial.
    
    Args:
        cnpj: String com o CNPJ (com ou sem formatação)
        
    Returns:
        bool: True se o CNPJ for válido, False caso contrário
    """
    # Remove formatação
    cnpj_clean = cnpj.replace('.', '').replace('/', '').replace('-', '').strip()
    
    # Verifica se tem 14 dígitos e se não são todos iguais
    if len(cnpj_clean) != 14 or cnpj_clean == cnpj_clean[0] * 14:
        return False
    
    # Verifica se são apenas números
    if not cnpj_clean.isdigit():
        return False
    
    # Pesos para validação
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cnpj_clean[i]) * pesos1[i] for i in range(12))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Calcula segundo dígito verificador
    soma = sum(int(cnpj_clean[i]) * pesos2[i] for i in range(13))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    return cnpj_clean[-2:] == f"{digito1}{digito2}"


def validar_documento(documento: str):
    """
    Valida CPF ou CNPJ.
    
    Args:
        documento: String com CPF ou CNPJ (com ou sem formatação)
        
    Returns:
        tuple: (é_válido, mensagem_erro)
    """
    documento_clean = documento.replace('.', '').replace('-', '').replace('/', '').strip()
    
    if len(documento_clean) == 11:
        if validar_cpf(documento):
            return True, ""
        return False, "CPF inválido. Verifique os dígitos."
    elif len(documento_clean) == 14:
        if validar_cnpj(documento):
            return True, ""
        return False, "CNPJ inválido. Verifique os dígitos."
    else:
        return False, "Documento inválido. CPF deve ter 11 dígitos e CNPJ deve ter 14 dígitos."


def carregar_configuracao(config_path: str = 'config.yaml') -> dict:
    """
    Carrega a configuração do arquivo YAML.
    
    Args:
        config_path (str): Caminho do arquivo de configuração
        
    Returns:
        dict: Dicionário com as configurações
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_path}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config


def inicializar_consulta():
    """
    Inicializa a instância de consulta de boletos.
    """
    global consulta_boletos
    
    try:
        # Carregar configuração
        config_path = os.environ.get('CONFIG_FILE', 'config.yaml')
        config = carregar_configuracao(config_path)
        
        # Obter configurações da API
        auth_url = config['api']['auth_url']
        api_base_url = config['api'].get('base_url', 'https://matls-clients.api.cora.com.br/v2/invoices')
        client_id = config['credentials']['client_id']
        cert_path = config['certificates']['cert_path']
        key_path = config['certificates']['key_path']
        # Obter debug da configuração (pode estar em diferentes locais)
        debug = config.get('debug', False) or config.get('config', {}).get('debug', False)
        
        # Configurar logging baseado no debug
        configurar_logging_debug(debug)
        
        if debug:
            logger.debug(f"Debug mode: {debug}")
            logger.debug(f"Config carregado: {config_path}")
        
        # Inicializar autenticação
        auth = CoraAuth(
            auth_url=auth_url,
            client_id=client_id,
            cert_path=cert_path,
            key_path=key_path,
            debug=debug
        )
        
        # Inicializar consulta
        consulta_boletos = ConsultaBoletos(
            api_base_url=api_base_url,
            auth=auth,
            debug=debug
        )
        
        logger.info("Consulta de boletos inicializada com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao inicializar consulta de boletos: {str(e)}")
        raise


@app.before_request
def before_request():
    """
    Função executada antes de cada requisição.
    """
    global consulta_boletos
    if consulta_boletos is None:
        try:
            inicializar_consulta()
        except Exception as e:
            logger.error(f"Erro ao inicializar aplicação: {str(e)}")


@app.route('/')
def index():
    """
    Página inicial - formulário de busca de boleto.
    """
    return render_template('index.html')


@app.route('/buscar', methods=['POST', 'GET'])
def buscar():
    """
    Processa a busca de boletos por CPF/CNPJ.
    """
    if not consulta_boletos:
        try:
            inicializar_consulta()
        except Exception as e:
            flash(f'Erro ao inicializar sistema: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    # Obter CPF do form (POST) ou query string (GET)
    if request.method == 'POST':
        cpf = request.form.get('cpf', '').strip()
    else:
        cpf = request.args.get('cpf', '').strip()
    
    if not cpf:
        flash('Por favor, informe o CPF ou CNPJ', 'error')
        return redirect(url_for('index'))
    
    # Validar CPF/CNPJ antes de fazer a busca
    valido, mensagem_erro = validar_documento(cpf)
    if not valido:
        flash(mensagem_erro, 'error')
        return redirect(url_for('index'))
    
    try:
        # Listar boletos por CPF
        resultado = consulta_boletos.listar_boletos_por_cpf(cpf)
        
        # Processar boletos
        boletos = resultado.get('data', [])
        
        # Processar e formatar boletos (usando apenas dados da lista, sem buscar detalhes)
        boletos_formatados = []
        for boleto in boletos:
            invoice_id = boleto.get('id')
            if not invoice_id:
                continue
            
            # Extrair dados básicos da lista (sem fazer requisição adicional)
            status_boleto = boleto.get('status', 'PENDING')
            esta_pago = status_boleto in ['PAID', 'SETTLED', 'CONFIRMED']
            
            # Extrair descrição dos serviços (se disponível na lista)
            descricao = ""
            services = boleto.get('services', [])
            if services:
                descricoes = []
                for s in services:
                    desc = s.get('description', '') or s.get('name', '')
                    if desc:
                        descricoes.append(desc)
                descricao = ' | '.join(descricoes) if descricoes else ''
            
            # Extrair nome do cliente (se disponível na lista)
            nome_cliente = ""
            customer = boleto.get('customer', {})
            if customer:
                nome_cliente = customer.get('name', '')
            
            # Extrair data de vencimento (due_date) - pode estar em payment_terms ou diretamente
            due_date = boleto.get('due_date')
            if not due_date:
                payment_terms = boleto.get('payment_terms', {})
                if payment_terms and isinstance(payment_terms, dict):
                    due_date = payment_terms.get('due_date')
            
            # Extrair data de pagamento (se pago) - campo é 'occurrence_date'
            data_pagamento = None
            if esta_pago:
                data_pagamento = boleto.get('occurrence_date')
            
            boleto_formatado = {
                'id': invoice_id,
                'code': boleto.get('code'),
                'status': status_boleto,
                'esta_pago': esta_pago,
                'due_date': due_date,
                'data_pagamento': data_pagamento,
                'nome_cliente': nome_cliente,
                'descricao': descricao,
                'created_at': boleto.get('created_at', '')
            }
            
            boletos_formatados.append(boleto_formatado)
        
        # Ordenar por data de criação (mais recente primeiro) e limitar a 12
        boletos_formatados.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        boletos_formatados = boletos_formatados[:12]
        
        # Limpar CPF para exibição (adicionar formatação)
        cpf_limpo = cpf.replace('.', '').replace('-', '').replace('/', '').replace(' ', '')
        if len(cpf_limpo) == 11:
            cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        elif len(cpf_limpo) == 14:
            cpf_formatado = f"{cpf_limpo[:2]}.{cpf_limpo[2:5]}.{cpf_limpo[5:8]}/{cpf_limpo[8:12]}-{cpf_limpo[12:]}"
        else:
            cpf_formatado = cpf
        
        dados = {
            'cpf': cpf_formatado,
            'cpf_limpo': cpf_limpo,
            'boletos': boletos_formatados,
            'total': len(boletos_formatados),
            'total_original': len(resultado.get('data', []))
        }
        
        return render_template('listar_boletos.html', dados=dados)
        
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Erro ao buscar boletos: {str(e)}")
        flash(f'Erro ao buscar boletos: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/boleto/<invoice_id>')
def visualizar(invoice_id: str):
    """
    Página de visualização do boleto.
    """
    if not consulta_boletos:
        try:
            inicializar_consulta()
        except Exception as e:
            flash(f'Erro ao inicializar sistema: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    try:
        # Consultar boleto completo
        boleto = consulta_boletos.consultar_boleto_por_id(invoice_id)
        
        # Verificar status de pagamento
        status = boleto.get('status', 'UNKNOWN')
        esta_pago = consulta_boletos.boleto_esta_pago(invoice_id)
        
        # Formatar valores monetários
        if 'amount' in boleto:
            valor_centavos = boleto['amount']
            valor_reais = valor_centavos / 100.0
            boleto['valor_formatado'] = f"R$ {valor_reais:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        elif 'total_amount' in boleto:
            valor_centavos = boleto['total_amount']
            valor_reais = valor_centavos / 100.0
            boleto['valor_formatado'] = f"R$ {valor_reais:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        
        # Extrair descrição dos serviços
        descricao = ""
        services = boleto.get('services', [])
        if services:
            descricoes = []
            for s in services:
                desc = s.get('description', '') or s.get('name', '')
                if desc:
                    descricoes.append(desc)
            descricao = ' | '.join(descricoes) if descricoes else ''
        
        # Extrair data de vencimento (due_date) - pode estar em payment_terms ou diretamente
        due_date = boleto.get('due_date')
        if not due_date:
            payment_terms = boleto.get('payment_terms', {})
            if payment_terms and isinstance(payment_terms, dict):
                due_date = payment_terms.get('due_date')
        
        # Extrair data de pagamento (se pago) - campo é 'occurrence_date'
        data_pagamento = None
        if esta_pago:
            data_pagamento = boleto.get('occurrence_date')
        
        # Extrair linha digitável, URL do PDF e PIX EMV (se disponível)
        linha_digitavel = None
        url_boleto_pdf = None
        pix_emv = None
        
        # Linha digitável, código de barras e URL do PDF vêm de payment_options.bank_slip
        payment_options = boleto.get('payment_options', {})
        barcode = None
        if payment_options:
            bank_slip = payment_options.get('bank_slip', {})
            if bank_slip:
                linha_digitavel = bank_slip.get('digitable')
                url_boleto_pdf = bank_slip.get('url')
                barcode = bank_slip.get('barcode')
        
        # PIX vem diretamente do boleto.pix.emv (não de payment_options)
        pix = boleto.get('pix', {})
        if pix:
            pix_emv = pix.get('emv')
        
        # Preparar dados para o template
        dados_boleto = {
            'id': boleto.get('id'),
            'code': boleto.get('code'),
            'status': status,
            'esta_pago': esta_pago,
            'amount': boleto.get('amount'),
            'valor_formatado': boleto.get('valor_formatado', ''),
            'due_date': due_date,
            'data_pagamento': data_pagamento,
            'descricao': descricao,
            'customer': boleto.get('customer', {}),
            'payment_forms': boleto.get('payment_forms', []),
            'linha_digitavel': linha_digitavel,
            'url_boleto_pdf': url_boleto_pdf,
            'barcode': barcode,
            'pix_emv': pix_emv,
            'created_at': boleto.get('created_at'),
            'updated_at': boleto.get('updated_at')
        }
        
        return render_template('visualizar.html', boleto=dados_boleto)
        
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Erro ao visualizar boleto: {str(e)}")
        flash(f'Erro ao visualizar boleto: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/api/boleto/<invoice_id>', methods=['GET'])
def api_consultar(invoice_id: str):
    """
    Endpoint API para consultar boleto por ID (retorna JSON).
    """
    if not consulta_boletos:
        try:
            inicializar_consulta()
        except Exception as e:
            return jsonify({'erro': f'Erro ao inicializar sistema: {str(e)}'}), 500
    
    try:
        boleto = consulta_boletos.consultar_boleto_por_id(invoice_id)
        esta_pago = consulta_boletos.boleto_esta_pago(invoice_id)
        
        boleto['esta_pago'] = esta_pago
        return jsonify(boleto), 200
        
    except ValueError as e:
        return jsonify({'erro': str(e)}), 404
    except Exception as e:
        logger.error(f"Erro ao consultar boleto via API: {str(e)}")
        return jsonify({'erro': str(e)}), 500


@app.route('/api/boletos/<cpf>', methods=['GET'])
def api_listar_boletos(cpf: str):
    """
    Endpoint API para listar boletos por CPF/CNPJ (retorna JSON).
    """
    if not consulta_boletos:
        try:
            inicializar_consulta()
        except Exception as e:
            return jsonify({'erro': f'Erro ao inicializar sistema: {str(e)}'}), 500
    
    try:
        resultado = consulta_boletos.listar_boletos_por_cpf(cpf)
        return jsonify(resultado), 200
        
    except ValueError as e:
        return jsonify({'erro': str(e)}), 404
    except Exception as e:
        logger.error(f"Erro ao listar boletos via API: {str(e)}")
        return jsonify({'erro': str(e)}), 500


if __name__ == '__main__':
    # Verificação rápida de dependências antes de iniciar
    try:
        from lib_setup import verificar_configuracao_basica, tentar_instalar_dependencias_faltantes
        
        config_ok, mensagens = verificar_configuracao_basica()
        
        if not config_ok:
            print("\n" + "="*60)
            print("⚠️  VERIFICAÇÃO DE CONFIGURAÇÃO")
            print("="*60)
            for msg in mensagens:
                print(f"  {msg}")
            
            # Tentar instalar dependências automaticamente
            dependencias_faltando = [msg for msg in mensagens if 'Dependências faltando' in msg]
            if dependencias_faltando:
                print("\n📦 Tentando instalar dependências automaticamente...")
                tentar_instalar_dependencias_faltantes()
            
            print("\n💡 Dica: Execute 'python setup_app.py' para configuração completa")
            print("="*60 + "\n")
    except ImportError:
        # Se lib_setup não existir, continua normalmente
        pass
    
    # Tentar inicializar antes de iniciar o servidor
    try:
        inicializar_consulta()
    except Exception as e:
        logger.warning(f"Erro ao inicializar consulta (será inicializado na primeira requisição): {str(e)}")
    
    # Obter porta e host das variáveis de ambiente
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Verificar se está rodando no Docker
    is_docker = os.path.exists('/.dockerenv')
    
    # Desabilitar reloader e threading no Docker (evita erros de permissão)
    # O reloader tenta criar subprocessos que podem falhar em containers Docker
    # O threading também pode falhar devido a restrições de recursos
    use_reloader = debug and not is_docker
    threaded = not is_docker  # Desabilitar threading no Docker
    
    print(f"\n🚀 Iniciando servidor em http://{host}:{port}")
    print("="*60 + "\n")
    
    app.run(host=host, port=port, debug=debug, use_reloader=use_reloader, threaded=threaded)
