#!/usr/bin/env python3
"""
Testes de validação dos dataclasses do sistema de geração de boletos Cora.
"""

import pytest
from datetime import datetime, timedelta

from libs.gerador import (
    CustomerDocument, CustomerAddress, Customer, Service,
    NotificationChannel, Notification, Interest, Fine, PaymentTerms, BoletoData
)

class TestCustomerDocument:
    """Testes para a classe CustomerDocument"""
    
    def test_cpf_valido(self):
        """Testa CPF válido"""
        doc = CustomerDocument("123.456.789-09", "CPF")
        assert doc.identity == "12345678909"
        assert doc.type == "CPF"
    
    def test_cpf_invalido(self):
        """Testa CPF inválido"""
        with pytest.raises(ValueError, match="CPF inválido"):
            CustomerDocument("123.456.789-10", "CPF")
    
    def test_cnpj_valido(self):
        """Testa CNPJ válido"""
        doc = CustomerDocument("11.222.333/0001-81", "CNPJ")
        assert doc.identity == "11222333000181"
        assert doc.type == "CNPJ"
    
    def test_cnpj_invalido(self):
        """Testa CNPJ inválido"""
        with pytest.raises(ValueError, match="CNPJ inválido"):
            CustomerDocument("11.222.333/0001-82", "CNPJ")
    
    def test_documento_tamanho_invalido(self):
        """Testa documento com tamanho inválido"""
        with pytest.raises(ValueError, match="deve ter 11 ou 14 dígitos"):
            CustomerDocument("12345", "CPF")

class TestCustomerAddress:
    """Testes para a classe CustomerAddress"""
    
    def test_endereco_valido(self):
        """Testa endereço válido"""
        address = CustomerAddress(
            street="Rua das Flores",
            number="123",
            district="Centro",
            city="São Paulo",
            state="SP",
            zip_code="01234-567"
        )
        assert address.street == "Rua das Flores"
        assert address.zip_code == "01234-567"
        assert address.state == "SP"
    
    def test_cep_invalido(self):
        """Testa CEP inválido"""
        with pytest.raises(ValueError, match="CEP inválido"):
            CustomerAddress(
                street="Rua A",
                number="123",
                district="Centro",
                city="SP",
                state="SP",
                zip_code="12345"
            )
    
    def test_campo_obrigatorio_faltando(self):
        """Testa campo obrigatório faltando"""
        with pytest.raises(ValueError, match="Rua é obrigatória"):
            CustomerAddress(
                street="",
                number="123",
                district="Centro",
                city="SP",
                state="SP",
                zip_code="01234-567"
            )

class TestCustomer:
    """Testes para a classe Customer"""
    
    def test_cliente_valido(self):
        """Testa cliente válido"""
        doc = CustomerDocument("123.456.789-09", "CPF")
        customer = Customer(
            name="João Silva",
            email="joao@email.com",
            document=doc
        )
        assert customer.name == "João Silva"
        assert customer.email == "joao@email.com"
    
    def test_email_invalido(self):
        """Testa email inválido"""
        doc = CustomerDocument("123.456.789-09", "CPF")
        with pytest.raises(ValueError, match="Email inválido"):
            Customer(
                name="João Silva",
                email="email-invalido",
                document=doc
            )
    
    def test_nome_vazio(self):
        """Testa nome vazio"""
        doc = CustomerDocument("123.456.789-09", "CPF")
        with pytest.raises(ValueError, match="Nome é obrigatório"):
            Customer(
                name="",
                email="joao@email.com",
                document=doc
            )

class TestService:
    """Testes para a classe Service"""
    
    def test_servico_valido(self):
        """Testa serviço válido"""
        service = Service(
            name="Consultoria",
            description="Serviço de consultoria técnica",
            amount=1500.50
        )
        assert service.name == "Consultoria"
        assert service.amount == 1500.50
    
    def test_valor_negativo(self):
        """Testa valor negativo"""
        with pytest.raises(ValueError, match="deve ser maior que zero"):
            Service(
                name="Consultoria",
                description="Serviço de consultoria",
                amount=-100.00
            )
    
    def test_campo_obrigatorio_faltando(self):
        """Testa campo obrigatório faltando"""
        with pytest.raises(ValueError, match="Nome do serviço é obrigatório"):
            Service(
                name="",
                description="Descrição",
                amount=100.00
            )

class TestNotificationChannel:
    """Testes para a classe NotificationChannel"""
    
    def test_canal_valido(self):
        """Testa canal válido"""
        channel = NotificationChannel(
            channel="EMAIL",
            contact="teste@email.com",
            rules=["NOTIFY_ON_DUE_DATE"]
        )
        assert channel.channel == "EMAIL"
        assert channel.contact == "teste@email.com"
    
    def test_canal_invalido(self):
        """Testa canal inválido"""
        with pytest.raises(ValueError, match="Canal inválido"):
            NotificationChannel(
                channel="TELEGRAM",
                contact="teste@email.com",
                rules=["NOTIFY_ON_DUE_DATE"]
            )
    
    def test_regra_invalida(self):
        """Testa regra inválida"""
        with pytest.raises(ValueError, match="Regra inválida"):
            NotificationChannel(
                channel="EMAIL",
                contact="teste@email.com",
                rules=["REGRA_INVALIDA"]
            )

class TestInterest:
    """Testes para a classe Interest"""
    
    def test_juros_valido(self):
        """Testa juros válido"""
        interest = Interest(rate=2.5)
        assert interest.rate == 2.5
        assert interest.to_dict() == {"rate": 2.5}
    
    def test_juros_invalido_alto(self):
        """Testa juros muito alto"""
        with pytest.raises(ValueError, match="entre 0 e 100%"):
            Interest(rate=150.0)
    
    def test_juros_invalido_negativo(self):
        """Testa juros negativo"""
        with pytest.raises(ValueError, match="entre 0 e 100%"):
            Interest(rate=-5.0)
    
    def test_juros_nulo(self):
        """Testa juros nulo"""
        interest = Interest(rate=None)
        assert interest.rate is None
        assert interest.to_dict() is None

class TestFine:
    """Testes para a classe Fine"""
    
    def test_multa_valida(self):
        """Testa multa válida"""
        fine = Fine(date="2025-07-15", amount=50.00)
        assert fine.amount == 50.00
        assert fine.to_dict() == {"date": "2025-07-15", "amount": 50.00}
    
    def test_multa_valor_negativo(self):
        """Testa multa com valor negativo"""
        with pytest.raises(ValueError, match="maior ou igual a zero"):
            Fine(amount=-10.00)
    
    def test_multa_data_invalida(self):
        """Testa multa com data inválida"""
        with pytest.raises(ValueError, match="formato YYYY-MM-DD"):
            Fine(date="15/07/2025", amount=50.00)
    
    def test_multa_apenas_valor(self):
        """Testa multa apenas com valor"""
        fine = Fine(amount=50.00)
        assert fine.to_dict() == {"amount": 50.00}

class TestPaymentTerms:
    """Testes para a classe PaymentTerms"""
    
    def test_data_vencimento_valida(self):
        """Testa data de vencimento válida"""
        future_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        payment_terms = PaymentTerms(
            due_date=future_date,
            interest=Interest(rate=1.0),
            fine=Fine(amount=10.00)
        )
        assert payment_terms.due_date == future_date
    
    def test_data_vencimento_passado(self):
        """Testa data de vencimento no passado"""
        past_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
        with pytest.raises(ValueError, match="não pode estar no passado"):
            PaymentTerms(
                due_date=past_date,
                interest=Interest(rate=1.0),
                fine=Fine(amount=10.00)
            )
    
    def test_data_vencimento_formato_invalido(self):
        """Testa formato de data inválido"""
        with pytest.raises(ValueError, match="formato YYYY-MM-DD"):
            PaymentTerms(
                due_date="15/07/2025",
                interest=Interest(rate=1.0),
                fine=Fine(amount=10.00)
            )

class TestBoletoData:
    """Testes para a classe BoletoData"""
    
    def test_boleto_completo_valido(self):
        """Testa boleto completo válido"""
        boleto = BoletoData(
            code="BOL001",
            customer=Customer(
                name="João Silva",
                email="joao@email.com",
                document=CustomerDocument("123.456.789-09", "CPF")
            ),
            services=[Service(
                name="Consultoria",
                description="Serviço de consultoria",
                amount=1500.00
            )],
            payment_terms=PaymentTerms(
                due_date=(datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
                interest=Interest(rate=2.5),
                fine=Fine(amount=50.00)
            ),
            notification=Notification(
                name="João Silva",
                channels=[NotificationChannel(
                    channel="EMAIL",
                    contact="joao@email.com",
                    rules=["NOTIFY_ON_DUE_DATE"]
                )]
            )
        )
        
        assert boleto.code == "BOL001"
        assert boleto.customer.name == "João Silva"
        assert boleto.services[0].amount == 1500.00
        
        # Testa conversão para dicionário
        boleto_dict = boleto.to_dict()
        assert "code" in boleto_dict
        assert "customer" in boleto_dict
        assert "services" in boleto_dict
        assert "payment_terms" in boleto_dict
        assert "notification" in boleto_dict
    
    def test_boleto_sem_juros_multa(self):
        """Testa boleto sem juros e multa"""
        boleto = BoletoData(
            code="BOL002",
            customer=Customer(
                name="Maria Silva",
                email="maria@email.com",
                document=CustomerDocument("987.654.321-00", "CPF")
            ),
            services=[Service(
                name="Desenvolvimento",
                description="Desenvolvimento de sistema",
                amount=5000.00
            )],
            payment_terms=PaymentTerms(
                due_date=(datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
                interest=Interest(rate=None),
                fine=Fine()
            ),
            notification=Notification(
                name="Maria Silva",
                channels=[NotificationChannel(
                    channel="EMAIL",
                    contact="maria@email.com",
                    rules=["NOTIFY_ON_DUE_DATE"]
                )]
            )
        )
        
        boleto_dict = boleto.to_dict()
        # Verifica que interest e fine não estão no dicionário
        assert "interest" not in boleto_dict["payment_terms"]
        assert "fine" not in boleto_dict["payment_terms"]

@pytest.mark.validation
class TestValidacoesIntegracao:
    """Testes de integração das validações"""
    
    def test_fluxo_completo_valido(self):
        """Testa fluxo completo com dados válidos"""
        # Cria todos os objetos necessários
        doc = CustomerDocument("123.456.789-09", "CPF")
        address = CustomerAddress(
            street="Rua das Flores",
            number="123",
            district="Centro",
            city="São Paulo",
            state="SP",
            zip_code="01234-567"
        )
        customer = Customer("João Silva", "joao@email.com", doc, address)
        service = Service("Consultoria", "Serviço técnico", 1500.00)
        interest = Interest(rate=2.5)
        fine = Fine(amount=50.00)
        payment_terms = PaymentTerms(
            due_date=(datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
            interest=interest,
            fine=fine
        )
        channel = NotificationChannel(
            "EMAIL", "joao@email.com", ["NOTIFY_ON_DUE_DATE"]
        )
        notification = Notification("João Silva", [channel])
        
        # Cria o boleto
        boleto = BoletoData(
            "BOL001", customer, [service], payment_terms, notification
        )
        
        # Verifica que tudo foi criado corretamente
        assert boleto.customer.document.identity == "12345678909"
        assert boleto.customer.address.zip_code == "01234-567"
        assert boleto.services[0].amount == 1500.00
        assert boleto.payment_terms.interest.rate == 2.5
        assert boleto.payment_terms.fine.amount == 50.00 