import unittest
import pandas as pd
import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.gerador import GeradorBoletos, BoletoData
from libs.auth import CoraAuth
import json
from datetime import datetime, timedelta

class TestGeradorBoletos(unittest.TestCase):
    """Testes unitários para o GeradorBoletos"""

    def setUp(self):
        """Configuração inicial dos testes"""
        # Mock do objeto de autenticação
        class MockAuth:
            def __init__(self):
                self.cert_path = "certificados/certificate.pem"
                self.key_path = "certificados/private-key.key"
        
        self.auth = MockAuth()
        self.gerador = GeradorBoletos("https://api.exemplo.com", self.auth, debug=True)
        
        # Data de vencimento padrão (amanhã)
        self.data_vencimento = (datetime.now().date() + timedelta(days=1)).strftime('%Y-%m-%d')

    def test_formatar_valor_monetario(self):
        """Testa a formatação de valores monetários em diferentes formatos"""
        casos_teste = [
            # Formato brasileiro
            ('R$ 1.234,56', 1234.56),
            ('1.234,56', 1234.56),
            ('1234,56', 1234.56),
            
            # Formato americano
            ('1,234.56', 1234.56),
            ('1234.56', 1234.56),
            
            # Valores inteiros
            ('1234', 1234.0),
            (1234, 1234.0),
            
            # Valores com múltiplos separadores
            ('1.234.567,89', 1234567.89),
            ('1,234,567.89', 1234567.89),
            
            # Casos especiais
            ('R$ 0,50', 0.50),
            ('R$1234', 1234.0),
        ]
        
        for valor_entrada, valor_esperado in casos_teste:
            with self.subTest(valor_entrada=valor_entrada):
                resultado = self.gerador._formatar_valor_monetario(valor_entrada)
                self.assertEqual(resultado, valor_esperado)

    def test_gerar_payload_cpf_valores_padrao(self):
        """Testa a geração de payload com CPF usando valores padrão de juros e multa"""
        # Cria um DataFrame com uma linha de teste
        dados = {
            'codigo': '12345',
            'nome': 'João da Silva',
            'email': 'joao@email.com',
            'documento': '123.456.789-10',
            'servico_nome': 'Consultoria',
            'servico_descricao': 'Consultoria mensal',
            'valor': 100.50,
            'data_vencimento': self.data_vencimento,
            'telefone': '(11) 98765-4321'
        }
        df = pd.DataFrame([dados])

        # Gera o payload
        payload = self.gerador._gerar_payload(df.iloc[0])

        # Verifica a estrutura do payload
        self.assertEqual(payload['code'], '12345')
        self.assertEqual(payload['customer']['name'], 'João da Silva')
        self.assertEqual(payload['customer']['email'], 'joao@email.com')
        self.assertEqual(payload['customer']['document']['identity'], '12345678910')
        self.assertEqual(payload['customer']['document']['type'], 'CPF')
        
        # Verifica o serviço
        self.assertEqual(len(payload['services']), 1)
        self.assertEqual(payload['services'][0]['name'], 'Consultoria')
        self.assertEqual(payload['services'][0]['description'], 'Consultoria mensal')
        self.assertEqual(payload['services'][0]['amount'], 10050)  # Valor em centavos

        # Verifica os termos de pagamento (valores padrão)
        self.assertEqual(payload['payment_terms']['due_date'], self.data_vencimento)
        self.assertEqual(payload['payment_terms']['fine']['amount'], 500)  # R$ 5,00 em centavos
        self.assertEqual(payload['payment_terms']['interest_monthly_percent'], 1.0)  # 1% ao mês

        # Verifica as notificações
        self.assertEqual(len(payload['notification']['channels']), 2)  # Email + SMS

    def test_gerar_payload_cpf_valores_personalizados(self):
        """Testa a geração de payload com CPF usando valores personalizados de juros e multa"""
        # Cria um DataFrame com uma linha de teste incluindo juros e multa
        dados = {
            'codigo': '12345',
            'nome': 'João da Silva',
            'email': 'joao@email.com',
            'documento': '123.456.789-10',
            'servico_nome': 'Consultoria',
            'servico_descricao': 'Consultoria mensal',
            'valor': 100.50,
            'data_vencimento': self.data_vencimento,
            'telefone': '(11) 98765-4321',
            'juros_mensal': 2.5,  # 2.5% ao mês
            'multa': '10,00'  # R$ 10,00
        }
        df = pd.DataFrame([dados])

        # Gera o payload
        payload = self.gerador._gerar_payload(df.iloc[0])

        # Verifica a estrutura do payload
        self.assertEqual(payload['code'], '12345')
        self.assertEqual(payload['customer']['name'], 'João da Silva')
        self.assertEqual(payload['customer']['email'], 'joao@email.com')
        self.assertEqual(payload['customer']['document']['identity'], '12345678910')
        self.assertEqual(payload['customer']['document']['type'], 'CPF')
        
        # Verifica o serviço
        self.assertEqual(len(payload['services']), 1)
        self.assertEqual(payload['services'][0]['name'], 'Consultoria')
        self.assertEqual(payload['services'][0]['description'], 'Consultoria mensal')
        self.assertEqual(payload['services'][0]['amount'], 10050)  # Valor em centavos

        # Verifica os termos de pagamento (valores personalizados)
        self.assertEqual(payload['payment_terms']['due_date'], self.data_vencimento)
        self.assertEqual(payload['payment_terms']['fine']['amount'], 1000)  # R$ 10,00 em centavos
        self.assertEqual(payload['payment_terms']['interest_monthly_percent'], 2.5)  # 2.5% ao mês

        # Verifica as notificações
        self.assertEqual(len(payload['notification']['channels']), 2)  # Email + SMS

    def test_gerar_payload_formatos_monetarios(self):
        """Testa diferentes formatos de valores monetários para multa"""
        formatos_teste = [
            ('10.00', 1000),  # Formato com ponto
            ('R$ 10,00', 1000),  # Formato com R$ e vírgula
            ('10,00', 1000),  # Formato com vírgula
            ('10', 1000),  # Formato sem decimais
            ('1.234,56', 123456),  # Valor maior com separador de milhar
        ]

        for valor_entrada, valor_esperado in formatos_teste:
            with self.subTest(valor_entrada=valor_entrada):
                dados = {
                    'codigo': '12345',
                    'nome': 'João da Silva',
                    'email': 'joao@email.com',
                    'documento': '123.456.789-10',
                    'servico_nome': 'Consultoria',
                    'servico_descricao': 'Consultoria mensal',
                    'valor': 100.50,
                    'data_vencimento': self.data_vencimento,
                    'telefone': '(11) 98765-4321',
                    'multa': valor_entrada
                }
                df = pd.DataFrame([dados])
                payload = self.gerador._gerar_payload(df.iloc[0])
                
                self.assertEqual(
                    payload['payment_terms']['fine']['amount'],
                    valor_esperado,
                    f"Falha ao converter '{valor_entrada}' para centavos"
                )
        email_channel = next(c for c in payload['notification']['channels'] if c['channel'] == 'EMAIL')
        sms_channel = next(c for c in payload['notification']['channels'] if c['channel'] == 'SMS')
        
        self.assertEqual(email_channel['contact'], 'joao@email.com')
        self.assertEqual(sms_channel['contact'], '+5511987654321')

        # Verifica as formas de pagamento
        self.assertEqual(payload['payment_forms'], ['BANK_SLIP', 'PIX'])

    def test_gerar_payload_cnpj(self):
        """Testa a geração de payload com CNPJ"""
        # Cria um DataFrame com uma linha de teste
        dados = {
            'codigo': 'EMP001',
            'nome': 'Empresa ABC Ltda',
            'email': 'contato@empresa.com',
            'documento': '12.345.678/0001-90',
            'servico_nome': 'Serviço Empresarial',
            'servico_descricao': 'Pacote empresarial mensal',
            'valor': 1500.00,
            'data_vencimento': self.data_vencimento,
            'rua': 'Rua Exemplo',
            'numero': '123',
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '01234-567',
            'complemento': 'Sala 45'
        }
        df = pd.DataFrame([dados])

        # Gera o payload
        payload = self.gerador._gerar_payload(df.iloc[0])

        # Verifica a estrutura do payload
        self.assertEqual(payload['code'], 'EMP001')
        self.assertEqual(payload['customer']['name'], 'Empresa ABC Ltda')
        self.assertEqual(payload['customer']['email'], 'contato@empresa.com')
        self.assertEqual(payload['customer']['document']['identity'], '12345678000190')
        self.assertEqual(payload['customer']['document']['type'], 'CNPJ')

        # Verifica o endereço
        self.assertIn('address', payload['customer'])
        self.assertEqual(payload['customer']['address']['street'], 'Rua Exemplo')
        self.assertEqual(payload['customer']['address']['number'], '123')
        self.assertEqual(payload['customer']['address']['district'], 'Centro')
        self.assertEqual(payload['customer']['address']['city'], 'São Paulo')
        self.assertEqual(payload['customer']['address']['state'], 'SP')
        self.assertEqual(payload['customer']['address']['zip_code'], '01234-567')
        self.assertEqual(payload['customer']['address']['complement'], 'Sala 45')

        # Verifica o serviço
        self.assertEqual(len(payload['services']), 1)
        self.assertEqual(payload['services'][0]['name'], 'Serviço Empresarial')
        self.assertEqual(payload['services'][0]['description'], 'Pacote empresarial mensal')
        self.assertEqual(payload['services'][0]['amount'], 150000)  # Valor em centavos

    def test_gerar_payload_valor_string(self):
        """Testa a geração de payload com valor em formato string"""
        dados = {
            'codigo': '12345',
            'nome': 'João da Silva',
            'email': 'joao@email.com',
            'documento': '123.456.789-10',
            'servico_nome': 'Consultoria',
            'servico_descricao': 'Consultoria mensal',
            'valor': 'R$ 1.234,56',
            'data_vencimento': self.data_vencimento
        }
        df = pd.DataFrame([dados])

        # Gera o payload
        payload = self.gerador._gerar_payload(df.iloc[0])

        # Verifica o valor convertido corretamente
        self.assertEqual(payload['services'][0]['amount'], 123456)  # Valor em centavos

    def test_gerar_payload_data_invalida(self):
        """Testa a geração de payload com data inválida"""
        dados = {
            'codigo': '12345',
            'nome': 'João da Silva',
            'email': 'joao@email.com',
            'documento': '123.456.789-10',
            'servico_nome': 'Consultoria',
            'servico_descricao': 'Consultoria mensal',
            'valor': 100.00,
            'data_vencimento': 'data_invalida'
        }
        df = pd.DataFrame([dados])

        # Gera o payload
        payload = self.gerador._gerar_payload(df.iloc[0])

        # Verifica se a data foi ajustada para amanhã
        data_esperada = (datetime.now().date() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.assertEqual(payload['payment_terms']['due_date'], data_esperada)

    def test_gerar_payload_documento_invalido(self):
        """Testa a geração de payload com documento inválido"""
        dados = {
            'codigo': '12345',
            'nome': 'João da Silva',
            'email': 'joao@email.com',
            'documento': '123',  # Documento inválido
            'servico_nome': 'Consultoria',
            'servico_descricao': 'Consultoria mensal',
            'valor': 100.00,
            'data_vencimento': self.data_vencimento
        }
        df = pd.DataFrame([dados])

        # Verifica se a exceção é lançada
        with self.assertRaises(ValueError) as context:
            self.gerador._gerar_payload(df.iloc[0])
        
        self.assertIn("Documento inválido", str(context.exception))

if __name__ == '__main__':
    unittest.main() 