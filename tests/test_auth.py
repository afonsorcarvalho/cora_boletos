import unittest
import os
import sys
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import requests

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.auth import CoraAuth

class TestCoraAuth(unittest.TestCase):
    """Testes unitários para a classe CoraAuth"""

    def setUp(self):
        """Configuração inicial dos testes"""
        self.auth_url = "https://matls-clients.api.cora.com.br/token"
        self.client_id = "test-client-id"
        self.cert_path = "certificados/certificate.pem"
        self.key_path = "certificados/private-key.key"
        
        # Mock dos arquivos de certificado
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            self.auth = CoraAuth(
                self.auth_url,
                self.client_id,
                self.cert_path,
                self.key_path,
                debug=True
            )

    def test_init(self):
        """Testa a inicialização da classe"""
        self.assertEqual(self.auth.auth_url, self.auth_url)
        self.assertEqual(self.auth.client_id, self.client_id)
        self.assertEqual(self.auth.cert_path, self.cert_path)
        self.assertEqual(self.auth.key_path, self.key_path)
        self.assertTrue(self.auth.debug)
        self.assertIsNone(self.auth._access_token)
        self.assertIsNone(self.auth._token_expiry)

    def test_validar_certificados_sucesso(self):
        """Testa a validação dos certificados quando existem"""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            # Não deve levantar exceção
            self.auth._validar_certificados()

    def test_validar_certificados_erro(self):
        """Testa a validação dos certificados quando não existem"""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            with self.assertRaises(FileNotFoundError):
                self.auth._validar_certificados()

    @patch('requests.post')
    def test_request_new_token(self, mock_post):
        """Testa a solicitação de um novo token"""
        # Configura o mock da resposta
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test-token-123',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response

        # Solicita novo token
        token = self.auth._request_new_token()

        # Verifica se o token foi retornado corretamente
        self.assertEqual(token, 'test-token-123')

        # Verifica se a requisição foi feita corretamente
        mock_post.assert_called_once_with(
            self.auth_url,
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id
            },
            cert=(self.cert_path, self.key_path),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

    @patch('requests.post')
    def test_request_new_token_erro(self, mock_post):
        """Testa o tratamento de erro na solicitação de token"""
        # Configura o mock para simular um erro
        mock_post.side_effect = requests.exceptions.RequestException("Erro de conexão")

        # Verifica se a exceção é propagada
        with self.assertRaises(requests.exceptions.RequestException):
            self.auth._request_new_token()

    @patch.object(CoraAuth, '_request_new_token')
    def test_get_access_token_novo(self, mock_request_token):
        """Testa a obtenção de um novo token quando não existe token atual"""
        mock_request_token.return_value = 'new-token-123'
        
        token = self.auth.get_access_token()
        
        self.assertEqual(token, 'new-token-123')
        mock_request_token.assert_called_once()

    @patch.object(CoraAuth, '_request_new_token')
    def test_get_access_token_cache(self, mock_request_token):
        """Testa o uso do token em cache quando ainda é válido"""
        # Configura um token válido em cache
        self.auth._access_token = 'cached-token-123'
        self.auth._token_expiry = datetime.now() + timedelta(minutes=10)
        
        token = self.auth.get_access_token()
        
        self.assertEqual(token, 'cached-token-123')
        mock_request_token.assert_not_called()

    @patch.object(CoraAuth, '_request_new_token')
    def test_get_access_token_expirado(self, mock_request_token):
        """Testa a renovação do token quando está expirado"""
        # Configura um token expirado em cache
        self.auth._access_token = 'expired-token-123'
        self.auth._token_expiry = datetime.now() - timedelta(minutes=1)
        
        mock_request_token.return_value = 'new-token-123'
        
        token = self.auth.get_access_token()
        
        self.assertEqual(token, 'new-token-123')
        mock_request_token.assert_called_once()

    def test_get_auth_headers(self):
        """Testa a geração dos headers de autenticação"""
        with patch.object(CoraAuth, 'get_access_token') as mock_get_token:
            mock_get_token.return_value = 'test-token-123'
            
            headers = self.auth.get_auth_headers()
            
            self.assertEqual(headers, {
                'Authorization': 'Bearer test-token-123',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            })
            mock_get_token.assert_called_once()

if __name__ == '__main__':
    unittest.main() 