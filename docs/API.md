# 📚 Documentação da API Cora

Documentação completa da integração com a API da Cora para geração de boletos bancários.

## 🔗 Endpoints da API

### Autenticação
- **URL**: `https://matls-clients.api.cora.com.br/token`
- **Método**: `POST`
- **Autenticação**: mTLS (certificado digital)

### Geração de Boletos
- **URL**: `https://matls-clients.api.cora.com.br/v2/invoices`
- **Método**: `POST`
- **Autenticação**: Bearer Token

## 🔐 Autenticação

### Requisitos
- **Certificado Digital**: Arquivo `.pem` (certificado público)
- **Chave Privada**: Arquivo `.key` (chave privada)
- **Client ID**: Identificador único fornecido pela Cora

### Processo de Autenticação
1. **Validação de Certificados**: Verifica se os arquivos existem e são válidos
2. **Geração de Token**: Faz requisição POST para `/token`
3. **Cache de Token**: Armazena token por 1 hora para otimização
4. **Renovação Automática**: Renova token quando expira

### Exemplo de Requisição
```bash
curl -X POST https://matls-clients.api.cora.com.br/token \
  --cert certificados/certificate.pem \
  --key certificados/private-key.key \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=SEU_CLIENT_ID"
```

### Resposta de Autenticação
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "invoices:write"
}
```

## 📄 Estrutura do Payload

### Dados do Cliente
```json
{
  "customer": {
    "name": "João da Silva",
    "email": "joao@email.com",
    "document": {
      "identity": "12345678909",
      "type": "CPF"
    },
    "address": {
      "street": "Rua das Flores",
      "number": "123",
      "district": "Centro",
      "city": "São Paulo",
      "state": "SP",
      "zip_code": "01234-567",
      "complement": "Apto 45"
    }
  }
}
```

### Serviços
```json
{
  "services": [
    {
      "name": "Consultoria Técnica",
      "description": "Serviço de consultoria mensal - Janeiro 2024",
      "amount": 150000
    }
  ]
}
```

### Termos de Pagamento
```json
{
  "payment_terms": {
    "due_date": "2024-02-15",
    "interest": {
      "rate": 2.5
    },
    "fine": {
      "date": "2024-02-16",
      "amount": 5000
    }
  }
}
```

### Notificações
```json
{
  "notification": {
    "name": "João da Silva",
    "channels": [
      {
        "channel": "EMAIL",
        "contact": "joao@email.com",
        "rules": ["NOTIFY_ON_DUE_DATE"]
      },
      {
        "channel": "SMS",
        "contact": "+5511987654321",
        "rules": ["NOTIFY_ON_DUE_DATE", "NOTIFY_AFTER_DUE_DATE"]
      }
    ]
  }
}
```

## 📋 Códigos de Status HTTP

### Sucesso
- **200**: Boleto gerado com sucesso
- **201**: Boleto criado (novo recurso)

### Erro do Cliente (4xx)
- **400**: Dados inválidos no payload
- **401**: Token inválido ou expirado
- **403**: Sem permissão para gerar boletos
- **404**: Endpoint não encontrado
- **422**: Dados de validação inválidos

### Erro do Servidor (5xx)
- **500**: Erro interno do servidor
- **502**: Serviço temporariamente indisponível
- **503**: Serviço em manutenção

## 🔍 Validações da API

### Documentos
- **CPF**: 11 dígitos, algoritmo de validação oficial
- **CNPJ**: 14 dígitos, algoritmo de validação oficial
- **Formato**: Apenas números (sem pontuação)

### Email
- **Formato**: Deve ser um email válido
- **Domínio**: Deve ter um domínio válido
- **Obrigatório**: Para notificações

### Valores Monetários
- **Formato**: Centavos (inteiro)
- **Mínimo**: 1 centavo
- **Máximo**: 999.999.999 centavos

### Datas
- **Formato**: YYYY-MM-DD
- **Vencimento**: Deve ser data futura
- **Timezone**: UTC

### CEP
- **Formato**: 00000-000
- **Validação**: Apenas números válidos

## 📊 Resposta da API

### Sucesso
```json
{
  "id": "inv_123456789",
  "code": "BOL001",
  "status": "PENDING",
  "customer": {
    "name": "João da Silva",
    "document": "12345678909"
  },
  "amount": 150000,
  "due_date": "2024-02-15",
  "payment_forms": [
    {
      "type": "BANK_SLIP",
      "url": "https://api.cora.com.br/boleto/123456789",
      "barcode": "12345678901234567890123456789012345678901234"
    },
    {
      "type": "PIX",
      "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
      "qr_code_text": "00020126580014br.gov.bcb.pix0136..."
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Erro
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados inválidos",
    "details": [
      {
        "field": "customer.document.identity",
        "message": "CPF inválido"
      }
    ]
  }
}
```

## 🔄 Rate Limiting

### Limites
- **Requisições por minuto**: 60
- **Requisições por hora**: 1000
- **Requisições por dia**: 10000

### Headers de Rate Limit
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642248600
```

### Tratamento de Rate Limit
```python
if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 60))
    time.sleep(retry_after)
    # Tentar novamente
```

## 🛡️ Segurança

### mTLS (Mutual TLS)
- **Certificado**: Obrigatório para todas as requisições
- **Validação**: Certificado deve ser válido e não expirado
- **Renovação**: Certificado deve ser renovado antes da expiração

### Tokens JWT
- **Expiração**: 1 hora
- **Renovação**: Automática quando necessário
- **Cache**: Local para otimização

### Headers de Segurança
```
Authorization: Bearer <token>
Content-Type: application/json
User-Agent: CoraBoletos/1.0
```

## 📝 Logs e Monitoramento

### Logs de Requisição
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "method": "POST",
  "url": "/v2/invoices",
  "status_code": 201,
  "response_time": 1250,
  "user_agent": "CoraBoletos/1.0"
}
```

### Métricas Importantes
- **Taxa de Sucesso**: > 99%
- **Tempo de Resposta**: < 2 segundos
- **Disponibilidade**: > 99.9%

## 🔧 Configuração de Ambiente

### Produção
```yaml
api:
  auth_url: https://matls-clients.api.cora.com.br/token
  base_url: https://matls-clients.api.cora.com.br/v2/invoices
  timeout: 30
  retries: 3
```

### Sandbox (Desenvolvimento)
```yaml
api:
  auth_url: https://sandbox-matls-clients.api.cora.com.br/token
  base_url: https://sandbox-matls-clients.api.cora.com.br/v2/invoices
  timeout: 30
  retries: 3
```

## 📞 Suporte

### Contato Técnico
- **Email**: api-support@cora.com.br
- **Telefone**: (11) 3000-0000
- **Horário**: Segunda a Sexta, 8h às 18h

### Documentação Adicional
- **Swagger**: https://api.cora.com.br/docs
- **Postman Collection**: Disponível no portal do desenvolvedor
- **SDKs**: Python, Node.js, Java, .NET

---

**Última atualização**: Junho 2025
**Versão da API**: v2 