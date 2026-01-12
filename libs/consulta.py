"""
Módulo responsável por consultar boletos na API do Cora.
Implementa funcionalidades para buscar e visualizar boletos existentes.
"""

import logging
import requests
from typing import Optional, Dict, Any
from .auth import CoraAuth


class ConsultaBoletos:
    """
    Classe responsável por consultar boletos na API do Cora.
    Implementa métodos para buscar boletos por ID.
    """
    
    def __init__(
        self,
        api_base_url: str,
        auth: CoraAuth,
        debug: bool = False
    ):
        """
        Inicializa o consultor de boletos.
        
        Args:
            api_base_url (str): URL base da API (ex: https://matls-clients.api.cora.com.br/v2/invoices)
            auth (CoraAuth): Instância de autenticação
            debug (bool): Habilita/desabilita logs de debug
        """
        # Normalizar a URL base - remover /invoices do final se presente
        self.api_base_url = api_base_url.rstrip('/')
        if self.api_base_url.endswith('/invoices'):
            self.api_base_url = self.api_base_url[:-9]
        elif self.api_base_url.endswith('/invoices/'):
            self.api_base_url = self.api_base_url[:-10]
        
        # Garantir que não termina com /v2 (será adicionado nos métodos)
        if self.api_base_url.endswith('/v2'):
            self.api_base_url = self.api_base_url[:-3]
        self.api_base_url = self.api_base_url.rstrip('/')
        
        self.auth = auth
        self.debug = debug
        
        if debug:
            logging.debug(f"ConsultaBoletos inicializado")
            logging.debug(f"API Base URL: {self.api_base_url}")
    
    def consultar_boleto_por_id(self, invoice_id: str) -> Dict[str, Any]:
        """
        Consulta um boleto pelo ID (invoice_id).
        
        Args:
            invoice_id (str): ID do boleto (invoice) a ser consultado
            
        Returns:
            dict: Dados do boleto retornados pela API
            
        Raises:
            requests.exceptions.RequestException: Em caso de erro na requisição
            ValueError: Se o invoice_id for inválido
        """
        if not invoice_id or not invoice_id.strip():
            raise ValueError("ID do boleto não pode ser vazio")
        
        invoice_id = invoice_id.strip()
        
        # URL do endpoint de consulta
        url = f"{self.api_base_url}/v2/invoices/{invoice_id}"
        
        if self.debug:
            logging.debug(f"Consultando boleto: {invoice_id}")
            logging.debug(f"URL: {url}")
        
        try:
            # Obtém o token de autenticação
            token = self.auth.get_access_token()
            if self.debug:
                logging.debug(f"Token obtido: {token[:20]}...")
            
            # Obtém os certificados
            cert_path = self.auth.cert_path
            key_path = self.auth.key_path
            if self.debug:
                logging.debug(f"Usando certificado: {cert_path}")
                logging.debug(f"Usando chave: {key_path}")
            
            # Prepara os headers
            headers = self.auth.get_auth_headers()
            headers['Accept'] = 'application/json'
            
            if self.debug:
                logging.debug("Headers da requisição:")
                for key, value in headers.items():
                    if key == 'Authorization':
                        logging.debug(f"  {key}: Bearer {value[:20]}...")
                    else:
                        logging.debug(f"  {key}: {value}")
            
            # Faz a requisição GET
            response = requests.get(
                url,
                headers=headers,
                cert=(cert_path, key_path),
                verify=True,
                timeout=30
            )
            
            # Log da resposta
            if self.debug:
                logging.debug(f"Status code: {response.status_code}")
                logging.debug(f"Headers da resposta: {dict(response.headers)}")
            
            # Verifica o status da resposta
            if response.status_code == 200:
                boleto_data = response.json()
                if self.debug:
                    logging.debug("Boleto encontrado com sucesso")
                    logging.debug(f"Dados do boleto: {boleto_data}")
                return boleto_data
            elif response.status_code == 404:
                error_msg = f"Boleto não encontrado: {invoice_id}"
                logging.warning(error_msg)
                raise ValueError(error_msg)
            elif response.status_code == 401:
                error_msg = "Token de autenticação inválido ou expirado"
                logging.error(error_msg)
                raise requests.exceptions.HTTPError(error_msg, response=response)
            elif response.status_code == 403:
                error_msg = "Sem permissão para consultar este boleto"
                logging.error(error_msg)
                raise requests.exceptions.HTTPError(error_msg, response=response)
            else:
                error_msg = f"Erro ao consultar boleto: {response.status_code} {response.reason}"
                logging.error(error_msg)
                if response.text:
                    logging.error(f"Resposta do servidor: {response.text}")
                response.raise_for_status()
                return {}
                
        except requests.exceptions.Timeout:
            error_msg = "Timeout ao consultar boleto"
            logging.error(error_msg)
            raise
        except requests.exceptions.ConnectionError:
            error_msg = "Erro de conexão ao consultar boleto"
            logging.error(error_msg)
            raise
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro ao consultar boleto: {str(e)}"
            logging.error(error_msg)
            raise
    
    def obter_status_pagamento(self, invoice_id: str) -> Optional[str]:
        """
        Obtém o status de pagamento de um boleto.
        
        Args:
            invoice_id (str): ID do boleto
            
        Returns:
            str: Status do pagamento (ex: 'PENDING', 'PAID', 'LATE', 'CANCELLED') ou None em caso de erro
        """
        try:
            boleto = self.consultar_boleto_por_id(invoice_id)
            return boleto.get('status')
        except Exception as e:
            logging.error(f"Erro ao obter status de pagamento: {str(e)}")
            return None
    
    def boleto_esta_pago(self, invoice_id: str) -> bool:
        """
        Verifica se um boleto está pago.
        
        Args:
            invoice_id (str): ID do boleto
            
        Returns:
            bool: True se o boleto estiver pago, False caso contrário
        """
        status = self.obter_status_pagamento(invoice_id)
        # Status pagos podem ser: 'PAID', 'SETTLED', etc.
        status_pagos = ['PAID', 'SETTLED', 'CONFIRMED']
        return status in status_pagos if status else False
    
    def _extrair_boletos_da_resposta(self, resposta: Dict[str, Any]) -> tuple:
        """
        Extrai lista de boletos da resposta da API.
        A API pode retornar em diferentes formatos.
        
        Args:
            resposta: Resposta JSON da API
            
        Returns:
            tuple: (lista_de_boletos, metadados)
        """
        # Se for uma lista direta
        if isinstance(resposta, list):
            return resposta, {}
        
        # Se for um dicionário, tentar diferentes campos
        if isinstance(resposta, dict):
            # Formato comum: {"data": [...], "meta": {...}}
            if 'data' in resposta:
                return resposta['data'], resposta.get('meta', {})
            
            # Formato alternativo: {"items": [...], ...}
            if 'items' in resposta:
                return resposta['items'], {k: v for k, v in resposta.items() if k != 'items'}
            
            # Formato alternativo: {"invoices": [...], ...}
            if 'invoices' in resposta:
                return resposta['invoices'], {k: v for k, v in resposta.items() if k != 'invoices'}
            
            # Se não tiver campo conhecido, retornar como lista vazia
            return [], resposta
        
        return [], {}
    
    def listar_boletos_por_cpf(self, cpf: str, page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """
        Lista boletos associados a um CPF/CNPJ.
        
        Args:
            cpf (str): CPF ou CNPJ do cliente (com ou sem formatação)
            page (int): Número da página (padrão: 1)
            per_page (int): Itens por página (padrão: 50)
            
        Returns:
            dict: Resposta da API com lista de boletos
            
        Raises:
            requests.exceptions.RequestException: Em caso de erro na requisição
            ValueError: Se o CPF for inválido
        """
        if not cpf or not cpf.strip():
            raise ValueError("CPF/CNPJ não pode ser vazio")
        
        # Remove formatação do CPF/CNPJ
        cpf_limpo = cpf.strip().replace('.', '').replace('-', '').replace('/', '').replace(' ', '')
        
        # Validação básica
        if len(cpf_limpo) not in [11, 14]:
            raise ValueError(f"CPF/CNPJ inválido: deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ)")
        
        if not cpf_limpo.isdigit():
            raise ValueError("CPF/CNPJ deve conter apenas números")
        
        # URL do endpoint de listagem
        url = f"{self.api_base_url}/v2/invoices"
        
        # Parâmetros da requisição
        params = {
            'search': cpf_limpo,
            'page': page,
            'perPage': per_page
        }
        
        if self.debug:
            logging.debug(f"Listando boletos para CPF/CNPJ: {cpf_limpo}")
            logging.debug(f"URL: {url}")
            logging.debug(f"Params: {params}")
        
        try:
            # Obtém o token de autenticação
            token = self.auth.get_access_token()
            if self.debug:
                logging.debug(f"Token obtido: {token[:20]}...")
            
            # Obtém os certificados
            cert_path = self.auth.cert_path
            key_path = self.auth.key_path
            if self.debug:
                logging.debug(f"Usando certificado: {cert_path}")
                logging.debug(f"Usando chave: {key_path}")
            
            # Prepara os headers
            headers = self.auth.get_auth_headers()
            headers['Accept'] = 'application/json'
            
            if self.debug:
                logging.debug("Headers da requisição:")
                for key, value in headers.items():
                    if key == 'Authorization':
                        logging.debug(f"  {key}: Bearer {value[:20]}...")
                    else:
                        logging.debug(f"  {key}: {value}")
            
            # Faz a requisição GET
            response = requests.get(
                url,
                headers=headers,
                params=params,
                cert=(cert_path, key_path),
                verify=True,
                timeout=30
            )
            
            # Log da resposta
            if self.debug:
                logging.debug(f"Status code: {response.status_code}")
                logging.debug(f"Headers da resposta: {dict(response.headers)}")
            
            # Verifica o status da resposta
            if response.status_code == 200:
                boletos_data = response.json()
                
                if self.debug:
                    import json
                    logging.debug("Boletos encontrados com sucesso")
                    logging.debug(f"Estrutura da resposta: {type(boletos_data)}")
                    logging.debug(f"Resposta completa (JSON): {json.dumps(boletos_data, indent=2, ensure_ascii=False)[:1000]}")
                
                # Extrair lista de boletos usando método auxiliar
                boletos_lista, metadados = self._extrair_boletos_da_resposta(boletos_data)
                
                if self.debug:
                    logging.debug(f"Boletos extraídos: {len(boletos_lista)} itens")
                    logging.debug(f"Metadados: {metadados}")
                
                # Normalizar resposta para formato padrão
                resposta_normalizada = {
                    'data': boletos_lista,
                    **metadados
                }
                
                return resposta_normalizada
            elif response.status_code == 404:
                error_msg = f"Nenhum boleto encontrado para o CPF/CNPJ: {cpf_limpo}"
                logging.warning(error_msg)
                raise ValueError(error_msg)
            elif response.status_code == 401:
                error_msg = "Token de autenticação inválido ou expirado"
                logging.error(error_msg)
                raise requests.exceptions.HTTPError(error_msg, response=response)
            elif response.status_code == 403:
                error_msg = "Sem permissão para consultar boletos"
                logging.error(error_msg)
                raise requests.exceptions.HTTPError(error_msg, response=response)
            else:
                error_msg = f"Erro ao listar boletos: {response.status_code} {response.reason}"
                logging.error(error_msg)
                if response.text:
                    logging.error(f"Resposta do servidor: {response.text}")
                response.raise_for_status()
                return {}
                
        except requests.exceptions.Timeout:
            error_msg = "Timeout ao listar boletos"
            logging.error(error_msg)
            raise
        except requests.exceptions.ConnectionError:
            error_msg = "Erro de conexão ao listar boletos"
            logging.error(error_msg)
            raise
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro ao listar boletos: {str(e)}"
            logging.error(error_msg)
            raise
