import os
import requests
import logging
from datetime import datetime, timedelta
from typing import Optional

class CoraAuth:
    """
    Classe responsável por gerenciar a autenticação com a API da Cora.
    Implementa o fluxo de Client Credentials com certificado mTLS.
    """
    
    def __init__(
        self,
        auth_url: str,
        client_id: str,
        cert_path: str,
        key_path: str,
        debug: bool = False
    ):
        """
        Inicializa o gerenciador de autenticação.
        
        Args:
            auth_url (str): URL de autenticação
            client_id (str): ID do cliente
            cert_path (str): Caminho do certificado
            key_path (str): Caminho da chave privada
            debug (bool): Habilita/desabilita logs de debug
        """
        self.auth_url = auth_url
        self.client_id = client_id
        self.cert_path = os.path.expanduser(cert_path)
        self.key_path = os.path.expanduser(key_path)
        self.debug = debug
        self._access_token = None
        self._token_expiry = None
        
        # Validação dos arquivos de certificado
        self._validar_certificados()
        
        if debug:
            logging.debug("Inicializando CoraAuth")
            logging.debug(f"Auth URL: {auth_url}")
            logging.debug(f"Client ID: {client_id}")
            logging.debug(f"Certificado: {self.cert_path}")
            logging.debug(f"Chave: {self.key_path}")
            logging.debug(f"Certificado existe? {os.path.exists(self.cert_path)}")
            logging.debug(f"Chave existe? {os.path.exists(self.key_path)}")
    
    def _validar_certificados(self):
        """
        Valida a existência dos arquivos de certificado.
        """
        if not os.path.exists(self.cert_path):
            raise FileNotFoundError(f"Certificado não encontrado: {self.cert_path}")
        if not os.path.exists(self.key_path):
            raise FileNotFoundError(f"Chave privada não encontrada: {self.key_path}")
        
        if self.debug:
            logging.debug("Certificados validados com sucesso")
    
    def _request_new_token(self) -> str:
        """
        Solicita um novo token de acesso.
        
        Returns:
            str: Token de acesso
        """
        try:
            if self.debug:
                logging.debug("Solicitando novo token de acesso")
                logging.debug(f"Client ID: {self.client_id}")
                logging.debug(f"Auth URL: {self.auth_url}")
                logging.debug(f"Certificado: {self.cert_path}")
                logging.debug(f"Chave: {self.key_path}")

            payload = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id
            }
            
            if self.debug:
                logging.debug(f"Payload da requisição: {payload}")

            response = requests.post(
                self.auth_url,
                data=payload,
                cert=(self.cert_path, self.key_path),
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if self.debug:
                logging.debug(f"Status code: {response.status_code}")
                logging.debug(f"Headers da resposta: {dict(response.headers)}")
                logging.debug(f"Resposta: {response.text}")

            response.raise_for_status()
            token_data = response.json()
            
            if self.debug:
                logging.debug("Token obtido com sucesso")
                logging.debug(f"Token: {token_data['access_token'][:20]}...")
                logging.debug(f"Expira em: {token_data.get('expires_in', 'N/A')} segundos")

            return token_data['access_token']

        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao solicitar token de acesso: {str(e)}")
            if hasattr(e.response, 'text'):
                logging.error(f"Resposta do servidor: {e.response.text}")
            raise
    
    def get_access_token(self) -> str:
        """
        Obtém um token de acesso válido.
        
        Returns:
            str: Token de acesso
        """
        # Verifica se o token atual é válido
        if self._access_token and self._token_expiry and datetime.now() < self._token_expiry:
            if self.debug:
                logging.debug("Usando token existente")
                logging.debug(f"Token expira em: {self._token_expiry}")
            return self._access_token

        # Solicita novo token
        if self.debug:
            logging.debug("Token expirado ou não existe, solicitando novo token")

        self._access_token = self._request_new_token()
        # Define expiração para 50 minutos (token geralmente válido por 1 hora)
        self._token_expiry = datetime.now() + timedelta(minutes=50)
        
        if self.debug:
            logging.debug(f"Novo token obtido: {self._access_token[:20]}...")
            logging.debug(f"Token expira em: {self._token_expiry}")

        return self._access_token
    
    def get_auth_headers(self) -> dict:
        """
        Obtém os headers de autenticação.
        
        Returns:
            dict: Headers de autenticação
        """
        token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if self.debug:
            logging.debug("Gerando headers de autenticação")
            logging.debug(f"Authorization: Bearer {token[:20]}...")
            logging.debug(f"Content-Type: {headers['Content-Type']}")
            logging.debug(f"Accept: {headers['Accept']}")

        return headers 