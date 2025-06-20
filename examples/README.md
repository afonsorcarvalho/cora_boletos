# Exemplos de Uso

## gerar_boleto_direto.py

Este script demonstra como gerar boletos passando os dados diretamente para o gerador, sem necessidade de arquivo Excel.

### Como usar

1. **Modo Demonstração (Recomendado para testes):**
   ```bash
   python3 examples/gerar_boleto_direto.py
   ```
   
   Este modo funciona sem certificados reais e mostra os dados que seriam enviados para a API.

2. **Modo Produção (Com certificados reais):**
   
   Primeiro, configure o arquivo `config.yaml` na raiz do projeto:
   ```yaml
   api:
     auth_url: https://matls-clients.api.cora.com.br/token
     base_url: https://matls-clients.api.cora.com.br/v2/invoices
   
   credentials:
     client_id: SEU_CLIENT_ID_AQUI
   
   certificates:
     cert_path: certificados/certificate.pem
     key_path: certificados/private-key.key
   ```
   
   Depois, crie o diretório `certificados` e adicione seus arquivos de certificado:
   ```bash
   mkdir certificados
   # Adicione seus certificados aqui
   ```
   
   Execute o script:
   ```bash
   python3 examples/gerar_boleto_direto.py
   ```

### Estrutura dos dados

O script cria dados de exemplo com a seguinte estrutura:

```python
{
    "codigo": "BOL001",
    "nome": "João da Silva",
    "email": "joao@email.com",
    "documento": "123.456.789-10",
    "telefone": "(11) 98765-4321",
    "servico_nome": "Consultoria",
    "servico_descricao": "Consultoria mensal - Janeiro 2024",
    "valor": 1500.50,
    "data_vencimento": "2025-07-09",
    "juros_mensal": 2.5,  # 2.5% ao mês
    "multa": 10.00,  # R$ 10,00 de multa
}
```

### Campos obrigatórios

- `codigo`: Código único do boleto
- `nome`: Nome do cliente
- `email`: Email do cliente
- `documento`: CPF ou CNPJ do cliente
- `telefone`: Telefone do cliente
- `servico_nome`: Nome do serviço
- `servico_descricao`: Descrição do serviço
- `valor`: Valor do boleto
- `data_vencimento`: Data de vencimento

### Campos opcionais

- `juros_mensal`: Percentual de juros mensal (padrão: 1%)
- `multa`: Valor da multa por atraso (padrão: R$ 2,00)

### Saída

O script mostrará:
- Código de barras do boleto
- Link para visualização do boleto
- Link do QR Code PIX (se disponível)

## teste_validacoes.py

Este script demonstra as validações implementadas nos dataclasses.

### Como usar

```bash
python3 examples/teste_validacoes.py
```

### Validações implementadas

#### 1. **CustomerDocument (CPF/CNPJ)**
- ✅ Validação de CPF usando algoritmo oficial
- ✅ Validação de CNPJ usando algoritmo oficial
- ✅ Formatação automática (remove pontos, traços, barras)
- ✅ Preenchimento com zeros à esquerda

#### 2. **CustomerAddress (Endereço)**
- ✅ Validação de campos obrigatórios
- ✅ Validação de CEP (formato brasileiro)
- ✅ Formatação automática do CEP (XXXXX-XXX)
- ✅ Normalização de estado (maiúsculas)

#### 3. **Customer (Cliente)**
- ✅ Validação de nome obrigatório
- ✅ Validação de email (formato regex)
- ✅ Normalização de email (minúsculas)

#### 4. **Service (Serviço)**
- ✅ Validação de nome obrigatório
- ✅ Validação de descrição obrigatória
- ✅ Validação de valor positivo

#### 5. **NotificationChannel (Canal de Notificação)**
- ✅ Validação de canais válidos (EMAIL, SMS, WHATSAPP)
- ✅ Validação de contato obrigatório
- ✅ Validação de regras válidas
- ✅ Normalização de canal (maiúsculas)

#### 6. **Interest (Juros)**
- ✅ Validação de taxa entre 0% e 100%
- ✅ Método `to_dict()` para serialização

#### 7. **Fine (Multa)**
- ✅ Validação de valor não negativo
- ✅ Validação de formato de data (YYYY-MM-DD)
- ✅ Método `to_dict()` para serialização

#### 8. **PaymentTerms (Termos de Pagamento)**
- ✅ Validação de data de vencimento no futuro
- ✅ Validação de formato de data (YYYY-MM-DD)

### Exemplos de validação

```python
# ✅ CPF válido
doc = CustomerDocument("123.456.789-09", "CPF")

# ❌ CPF inválido
doc = CustomerDocument("123.456.789-10", "CPF")  # ValueError

# ✅ Email válido
customer = Customer("João", "joao@email.com", doc)

# ❌ Email inválido
customer = Customer("João", "email-invalido", doc)  # ValueError

# ✅ CEP válido
address = CustomerAddress("Rua A", "123", "Centro", "SP", "SP", "01234-567")

# ❌ CEP inválido
address = CustomerAddress("Rua A", "123", "Centro", "SP", "SP", "12345")  # ValueError
```

### Benefícios das validações

1. **Detecção precoce de erros**: Validações acontecem na criação dos objetos
2. **Dados consistentes**: Garantia de que os dados estão no formato correto
3. **Melhor experiência do desenvolvedor**: Mensagens de erro claras e específicas
4. **Prevenção de bugs**: Evita problemas na API por dados malformados
5. **Documentação viva**: As validações servem como documentação dos requisitos 