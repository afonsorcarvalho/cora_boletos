import pandas as pd
import requests
import logging
import os
from datetime import datetime
from .auth import CoraAuth
import json
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union

@dataclass
class CustomerDocument:
    """Representa o documento do cliente (CPF/CNPJ)"""
    identity: str
    type: str
    
    def __post_init__(self):
        """Valida o documento após a inicialização"""
        # Remove formatação
        identity_clean = str(self.identity).replace('.', '').replace('-', '').replace('/', '')
        
        # Valida CPF
        if len(identity_clean) == 11:
            if not self._validar_cpf(identity_clean):
                raise ValueError(f"CPF inválido: {self.identity}")
            self.identity = identity_clean.zfill(11)
            self.type = "CPF"
        # Valida CNPJ
        elif len(identity_clean) == 14:
            if not self._validar_cnpj(identity_clean):
                raise ValueError(f"CNPJ inválido: {self.identity}")
            self.identity = identity_clean.zfill(14)
            self.type = "CNPJ"
        else:
            raise ValueError(f"Documento inválido: {self.identity} (deve ter 11 ou 14 dígitos)")
    
    def _validar_cpf(self, cpf: str) -> bool:
        """Valida CPF usando algoritmo oficial"""
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        # Calcula primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        # Calcula segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        return cpf[-2:] == f"{digito1}{digito2}"
    
    def _validar_cnpj(self, cnpj: str) -> bool:
        """Valida CNPJ usando algoritmo oficial"""
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
        
        # Pesos para validação
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        
        # Calcula primeiro dígito verificador
        soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        # Calcula segundo dígito verificador
        soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        return cnpj[-2:] == f"{digito1}{digito2}"

@dataclass
class CustomerAddress:
    """Representa o endereço do cliente"""
    street: str
    number: str
    district: str
    city: str
    state: str
    zip_code: str
    complement: Optional[str] = None
    
    def __post_init__(self):
        """Valida o endereço após a inicialização"""
        # Valida campos obrigatórios
        if not self.street.strip():
            raise ValueError("Rua é obrigatória")
        if not self.number.strip():
            raise ValueError("Número é obrigatório")
        if not self.city.strip():
            raise ValueError("Cidade é obrigatória")
        if not self.state.strip():
            raise ValueError("Estado é obrigatório")
        
        # Valida CEP
        cep_clean = str(self.zip_code).replace('-', '').replace('.', '')
        if len(cep_clean) != 8 or not cep_clean.isdigit():
            raise ValueError(f"CEP inválido: {self.zip_code}")
        
        # Formata CEP
        self.zip_code = f"{cep_clean[:5]}-{cep_clean[5:]}"
        
        # Limpa e valida outros campos
        self.street = self.street.strip()
        self.number = self.number.strip()
        self.district = self.district.strip()
        self.city = self.city.strip()
        self.state = self.state.strip().upper()
        self.complement = self.complement.strip() if self.complement else None

@dataclass
class Customer:
    """Representa os dados do cliente"""
    name: str
    email: str
    document: CustomerDocument
    address: Optional[CustomerAddress] = None
    
    def __post_init__(self):
        """Valida o cliente após a inicialização"""
        # Valida nome
        if not self.name.strip():
            raise ValueError("Nome é obrigatório")
        self.name = self.name.strip()
        
        # Valida email
        if not self._validar_email(self.email):
            raise ValueError(f"Email inválido: {self.email}")
        self.email = self.email.strip().lower()
    
    def _validar_email(self, email: str) -> bool:
        """Valida formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

@dataclass
class Service:
    """Representa um serviço no boleto"""
    name: str
    description: str
    amount: float
    
    def __post_init__(self):
        """Valida o serviço após a inicialização"""
        if not self.name.strip():
            raise ValueError("Nome do serviço é obrigatório")
        if not self.description.strip():
            raise ValueError("Descrição do serviço é obrigatória")
        if self.amount <= 0:
            raise ValueError(f"Valor do serviço deve ser maior que zero: {self.amount}")
        
        self.name = self.name.strip()
        self.description = self.description.strip()

@dataclass
class NotificationChannel:
    """Representa um canal de notificação"""
    channel: str
    contact: str
    rules: List[str]
    
    def __post_init__(self):
        """Valida o canal de notificação após a inicialização"""
        # Valida canal
        canais_validos = ["EMAIL", "SMS", "WHATSAPP"]
        if self.channel.upper() not in canais_validos:
            raise ValueError(f"Canal inválido: {self.channel}. Válidos: {canais_validos}")
        
        # Valida contato
        if not self.contact.strip():
            raise ValueError("Contato é obrigatório")
        
        # Valida regras
        regras_validas = [
            "NOTIFY_FIVE_DAYS_BEFORE_DUE_DATE",
            "NOTIFY_TWO_DAYS_BEFORE_DUE_DATE", 
            "NOTIFY_ON_DUE_DATE",
            "NOTIFY_WHEN_PAID"
        ]
        
        for regra in self.rules:
            if regra not in regras_validas:
                raise ValueError(f"Regra inválida: {regra}. Válidas: {regras_validas}")
        
        self.channel = self.channel.upper()
        self.contact = self.contact.strip()

@dataclass
class Notification:
    """Representa as configurações de notificação"""
    name: str
    channels: List[NotificationChannel]
    
    def __post_init__(self):
        """Valida a notificação após a inicialização"""
        if not self.name.strip():
            raise ValueError("Nome da notificação é obrigatório")
        if not self.channels:
            raise ValueError("Pelo menos um canal de notificação é obrigatório")
        
        self.name = self.name.strip()

@dataclass
class Interest:
    """Representa os termos de interest"""
    rate: Optional[float] = None
    
    def __post_init__(self):
        """Valida o interest após a inicialização"""
        if self.rate is not None:
            if self.rate < 0 or self.rate > 100:
                raise ValueError(f"Taxa de juros deve estar entre 0 e 100%: {self.rate}")
    
    def to_dict(self) -> Optional[dict]:
        """Converte para dicionário se válido"""
        if self.rate is not None:
            return {"rate": self.rate}
        return None

@dataclass
class Fine:
    """Representa os termos de fine"""
    date: Optional[str] = None
    amount: Optional[float] = None
    
    def __post_init__(self):
        """Valida o fine após a inicialização"""
        #TODO: Colocar o outro tipo de fine tipo rate procurar na documentação https://developers.cora.com.br/reference/emiss%C3%A3o-de-boleto-registrado-v2#objeto-fine
        if self.amount is not None and self.amount < 0:
            raise ValueError(f"Valor da multa deve ser maior ou igual a zero: {self.amount}")
        
        if self.date is not None:
            try:
                datetime.strptime(self.date, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f"Data da multa deve estar no formato YYYY-MM-DD: {self.date}")
    
    def to_dict(self) -> Optional[dict]:
        """Converte para dicionário se válido"""
        result = {}
        if self.date is not None:
            result["date"] = self.date
        if self.amount is not None:
            result["amount"] = self.amount
        return result if result else None

@dataclass
class PaymentTerms:
    """Representa os termos de pagamento"""
    due_date: str
    interest: Interest
    fine: Fine
    
    def __post_init__(self):
        """Valida os termos de pagamento após a inicialização"""
        # Valida data de vencimento
        try:
            data_vencimento = datetime.strptime(self.due_date, '%Y-%m-%d')
            data_atual = datetime.now().date()
            
            if data_vencimento.date() < data_atual:
                raise ValueError(f"Data de vencimento não pode estar no passado: {self.due_date}")
        except ValueError as e:
            if "passado" in str(e):
                raise e
            raise ValueError(f"Data de vencimento deve estar no formato YYYY-MM-DD: {self.due_date}")

@dataclass
class BoletoData:
    """Representa todos os dados necessários para gerar um boleto"""
    code: str
    customer: Customer
    services: List[Service]
    payment_terms: PaymentTerms
    notification: Notification
    payment_forms: List[str] = None

    def __post_init__(self):
        """Inicializa valores padrão após a criação do objeto"""
        if self.payment_forms is None:
            self.payment_forms = ["BANK_SLIP", "PIX"]

    def to_dict(self) -> dict:
        """Converte os dados do boleto para o formato de dicionário esperado pela API"""
        return {
            "code": self.code,
            "customer": {
                "name": self.customer.name,
                "email": self.customer.email,
                "document": {
                    "identity": self.customer.document.identity,
                    "type": self.customer.document.type
                },
                **({"address": {
                    "street": self.customer.address.street,
                    "number": self.customer.address.number,
                    "district": self.customer.address.district,
                    "city": self.customer.address.city,
                    "state": self.customer.address.state,
                    "complement": self.customer.address.complement or "N/A",
                    "zip_code": self.customer.address.zip_code
                }} if self.customer.address else {})
            },
            "services": [{
                "name": service.name,
                "description": service.description,
                "amount": int(service.amount * 100)  # Converte para centavos
            } for service in self.services],
            "payment_terms": {
                "due_date": self.payment_terms.due_date,
                **({"interest": self.payment_terms.interest.to_dict()} if self.payment_terms.interest.to_dict() else {}),
                **({"fine": self.payment_terms.fine.to_dict()} if self.payment_terms.fine.to_dict() else {})
            },
            "notification": {
                "name": self.notification.name,
                "channels": [{
                    "channel": channel.channel,
                    "contact": channel.contact,
                    "rules": channel.rules
                } for channel in self.notification.channels]
            },
            "payment_forms": self.payment_forms
        }

class GeradorBoletos:
    def __init__(self, api_url: str, auth: CoraAuth, debug: bool = False):
        """
        Inicializa o gerador de boletos.
        
        Args:
            api_url (str): URL base da API
            auth (CoraAuth): Objeto de autenticação
            debug (bool): Habilita/desabilita logs de debug
        """
        self.api_url = api_url
        self.auth = auth
        self.debug = debug
        self.fine = 500
        self.interest = 1.0
       
        if debug:
            logging.debug("Inicializando GeradorBoletos")
            logging.debug(f"API URL: {api_url}")
            logging.debug(f"Certificado: {auth.cert_path}")
            logging.debug(f"Chave: {auth.key_path}")

    def _formatar_valor_monetario(self, valor) -> float:
        """
        Formata um valor monetário para float, independente do formato de entrada.
        
        Args:
            valor: Valor monetário (pode ser string ou número)
            
        Returns:
            float: Valor convertido para float
        """
        if isinstance(valor, (int, float)):
            return float(valor)
            
        # Se for string, limpa a formatação
        valor_str = str(valor)
        
        # Remove símbolos monetários e espaços
        valor_str = valor_str.replace('R$', '').replace(' ', '')
        
        # Trata diferentes formatos de número
        # Caso 1: 1.234,56 -> 1234.56
        # Caso 2: 1,234.56 -> 1234.56
        if ',' in valor_str and '.' in valor_str:
            if valor_str.find(',') > valor_str.find('.'):
                # Formato brasileiro: 1.234,56
                valor_str = valor_str.replace('.', '').replace(',', '.')
            else:
                # Formato americano: 1,234.56
                valor_str = valor_str.replace(',', '')
        else:
            # Caso 3: 1234,56 -> 1234.56
            valor_str = valor_str.replace(',', '.')
            
        return float(valor_str)

    def _gerar_payload(self, row: pd.Series) -> dict:
        """
        Gera o payload para a requisição de boleto seguindo exatamente o formato da API.
        
        Args:
            row (pd.Series): Linha do DataFrame com os dados do cliente
            
        Returns:
            dict: Payload formatado para a API
        """
        if self.debug:
            logging.debug(f"Gerando payload para cliente: {row['nome']}")
            logging.debug(f"Dados do cliente: {row.to_dict()}")

        # Formata o documento (CPF/CNPJ)
        identity = str(row['documento']).replace('.', '').replace('-', '').replace('/', '')
        # Garante que o documento tenha o tamanho correto com zeros à esquerda
        if len(identity) == 11:  # CPF
            identity = identity.zfill(11)
            type = "CPF"
        elif len(identity) == 14:  # CNPJ
            identity = identity.zfill(14)
            type = "CNPJ"
        else:
            raise ValueError(f"Documento inválido: {row['documento']} (deve ter 11 ou 14 dígitos)")

        # Cria o documento do cliente
        document = CustomerDocument(identity=identity, type=type)

        # Cria o endereço se existir
        address = None
        if all(field in row for field in ['rua', 'numero', 'bairro', 'cidade', 'estado', 'cep']):
            address = CustomerAddress(
                street=str(row['rua']).strip(),
                number=str(row['numero']).strip(),
                district=str(row['bairro']).strip(),
                city=str(row['cidade']).strip(),
                state=str(row['estado']).strip(),
                complement=str(row.get('complemento', 'N/A')).strip(),
                zip_code=str(row['cep']).strip()
            )

        # Cria o cliente
        customer = Customer(
            name=str(row['nome']).strip(),
            email=str(row['email']).strip(),
            document=document,
            address=address
        )

        # Formata a data de vencimento
        data_vencimento = str(row['data_vencimento']).strip()
        try:
            data_vencimento_obj = datetime.strptime(data_vencimento, '%Y-%m-%d')
            data_atual = datetime.now().date()
            
            if data_vencimento_obj.date() < data_atual:
                logging.warning(f"Data de vencimento no passado: {data_vencimento}. Usando data atual + 1 dia.")
                data_vencimento = (data_atual + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        except ValueError:
            logging.warning(f"Formato de data inválido: {data_vencimento}. Usando data atual + 1 dia.")
            data_vencimento = (datetime.now().date() + pd.Timedelta(days=1)).strftime('%Y-%m-%d')

        # Formata o valor monetário
        valor_float = self._formatar_valor_monetario(row['valor'])

        # Cria o serviço
        service = Service(
            name=str(row['servico_nome']).strip(),
            description=str(row['servico_descricao']).strip(),
            amount=valor_float
        )

        # Obtém juros e multa personalizados ou usa os valores padrão
        juros = float(row.get('juros_mensal', self.interest))
        multa = self._formatar_valor_monetario(row.get('multa', self.fine / 100)) * 100  # Converte para centavos
        
        # Cria os termos de pagamento
        payment_terms = PaymentTerms(
            due_date=data_vencimento,
            interest=Interest(rate=juros),
            fine=Fine(date=data_vencimento, amount=multa)
        )

        # Cria os canais de notificação
        channels = [
            NotificationChannel(
                channel="EMAIL",
                contact=str(row['email']).strip(),
                rules=[
                    "NOTIFY_FIVE_DAYS_BEFORE_DUE_DATE",
                    "NOTIFY_TWO_DAYS_BEFORE_DUE_DATE",
                    "NOTIFY_ON_DUE_DATE",
                    "NOTIFY_WHEN_PAID"
                ]
            )
        ]

        # Adiciona SMS se houver telefone
        if 'telefone' in row and pd.notna(row['telefone']) and str(row['telefone']).strip():
            telefone = str(row['telefone']).replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
            if telefone.startswith('55'):
                telefone = '+' + telefone
            elif not telefone.startswith('+55'):
                telefone = '+55' + telefone

            channels.append(
                NotificationChannel(
                    channel="SMS",
                    contact=telefone,
                    rules=[
                        "NOTIFY_FIVE_DAYS_BEFORE_DUE_DATE",
                        "NOTIFY_TWO_DAYS_BEFORE_DUE_DATE",
                        "NOTIFY_ON_DUE_DATE",
                        "NOTIFY_WHEN_PAID"
                    ]
                )
            )

        # Cria a notificação
        notification = Notification(
            name=str(row['nome']).strip(),
            channels=channels
        )

        # Cria o objeto BoletoData
        boleto_data = BoletoData(
            code=str(row['codigo']).strip(),
            customer=customer,
            services=[service],
            payment_terms=payment_terms,
            notification=notification
        )

        return boleto_data.to_dict()

    def gerar_boleto(self, dados_boleto: Union[dict, BoletoData]) -> dict:
        """
        Gera um boleto através da API.
        
        Args:
            dados_boleto: Pode ser um dicionário com os dados do boleto ou um objeto BoletoData
            
        Returns:
            dict: Resposta da API
        """
        try:
            # Converte para payload se necessário
            payload = dados_boleto.to_dict() if isinstance(dados_boleto, BoletoData) else dados_boleto

            if self.debug:
                logging.debug(f"Payload para geração do boleto: {json.dumps(payload, indent=2, ensure_ascii=False)}")

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
            headers['Content-Type'] = 'application/json'
            headers['accept'] = 'application/json'
            
            # Gera chave de idempotência
            import uuid
            idempotency_key = str(uuid.uuid4())
            headers['Idempotency-Key'] = idempotency_key
            if self.debug:
                logging.debug(f"Idempotency-Key: {idempotency_key}")

            # Log detalhado da requisição
            logging.info("=== DETALHES DA REQUISIÇÃO ===")
            logging.info(f"URL: {self.api_url}")
            logging.info("Headers:")
            for key, value in headers.items():
                if key == 'Authorization':
                    logging.info(f"  {key}: Bearer {value[:20]}...")
                else:
                    logging.info(f"  {key}: {value}")
            logging.info("Payload:")
            logging.info(json.dumps(payload, indent=2, ensure_ascii=False))

            # Faz a requisição
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                cert=(cert_path, key_path),
                verify=True
            )

            # Log da resposta
            logging.info(f"Status code: {response.status_code}")
            logging.info("Headers da resposta:")
            for key, value in response.headers.items():
                logging.info(f"  {key}: {value}")

            if response.status_code == 200:
                logging.info(f"Boleto gerado com sucesso para: {payload['customer']['name']}")
                if self.debug:
                    logging.debug("Resposta da API:")
                    logging.debug(json.dumps(response.json(), indent=2, ensure_ascii=False))
                return response.json()
            else:
                error_msg = f"Erro ao gerar boleto para {payload['customer']['name']}: {response.status_code} {response.reason} for url: {self.api_url}"
                logging.error(error_msg)
                if response.text:
                    logging.error(f"Resposta da API: {response.text}")
                raise Exception(error_msg)

        except Exception as e:
            logging.error(f"Erro ao gerar boleto: {str(e)}")
          
         

    def processar_arquivo(self, excel_file: str):
        """
        Processa o arquivo Excel/CSV e gera os boletos.
        
        Args:
            excel_file (str): Caminho do arquivo Excel/CSV
        """
        try:
            if self.debug:
                logging.debug(f"Processando arquivo: {excel_file}")

            try:
                # Tenta ler como Excel
                df = pd.read_excel(excel_file, engine='openpyxl')
            except Exception as excel_error:
                if self.debug:
                    logging.debug(f"Erro ao ler como Excel: {str(excel_error)}")
                    logging.debug("Tentando ler como CSV...")
                
                # Se falhar, tenta ler como CSV
                df = pd.read_csv(excel_file)

            if self.debug:
                logging.debug(f"Arquivo lido com sucesso")
                logging.debug(f"Total de registros: {len(df)}")
                logging.debug(f"Colunas: {df.columns.tolist()}")
                logging.debug(f"Primeiros registros:\n{df.head()}")

            # Processa cada linha
            for index, row in df.iterrows():
                try:
                    if self.debug:
                        logging.debug(f"\nProcessando linha {index + 1}")
                        logging.debug(f"Dados da linha:\n{row.to_dict()}")

                    # Gera o payload
                    payload = self._gerar_payload(row)
                    
                    # Gera o boleto
                    response = self.gerar_boleto(payload)
                    
                    logging.info(f"Boleto gerado com sucesso para {row['nome']}")
                    if self.debug:
                        logging.debug(f"Resposta completa: {response}")

                except Exception as e:
                    logging.error(f"Erro ao processar linha {index + 1}: {str(e)}")
                    

        except Exception as e:
            logging.error(f"Erro ao processar arquivo {excel_file}: {str(e)}")
            
        finally:
            logging.info("Processamento concluído!") 

    def gerar_boleto_individual(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera um boleto individual a partir de um dicionário de dados.
        
        Args:
            dados (Dict[str, Any]): Dicionário com os dados do boleto
            
        Returns:
            Dict[str, Any]: Resposta da API com os dados do boleto gerado
        """
        if self.debug:
            logging.info(f"Gerando boleto para {dados['nome']}")
            
        # Converte o dicionário para um formato similar ao DataFrame
        row = pd.Series(dados)
        
        # Gera o payload
        payload = self._gerar_payload(row)
        
        # Usa o método gerar_boleto existente
        return self.gerar_boleto(payload) 