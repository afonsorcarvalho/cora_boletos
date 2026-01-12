# 🌐 Aplicação Web - Consulta de Boletos Cora

Aplicação web em Flask que permite que clientes busquem e visualizem seus boletos através do navegador.

## 📋 Funcionalidades

- ✅ **Busca de Boletos**: Interface web para buscar boletos por ID (invoice_id)
- ✅ **Visualização de Boletos**: Exibição completa dos detalhes do boleto
- ✅ **Status de Pagamento**: Verificação se o boleto está pago ou pendente
- ✅ **Formas de Pagamento**: Visualização de boleto bancário e PIX
- ✅ **Interface Responsiva**: Design moderno e responsivo

## 🚀 Instalação

### Instalação Automática (Recomendado)

Execute o script de instalação automática:

```bash
python setup_app.py
```

O script irá:
- ✅ Verificar versão do Python
- ✅ Criar/verificar ambiente virtual
- ✅ Instalar todas as dependências
- ✅ Criar arquivo `.env` automaticamente
- ✅ Verificar configurações básicas
- ✅ Criar diretórios necessários

### Instalação Manual

Se preferir instalar manualmente:

#### 1. Instalar Dependências

Certifique-se de que todas as dependências estão instaladas:

```bash
# Ativar ambiente virtual (se usar)
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

A aplicação requer Flask e outras dependências já listadas no `requirements.txt`.

### 2. Configuração

A aplicação utiliza dois arquivos de configuração:

#### Arquivo `.env` (Variáveis de Ambiente)

Copie o arquivo de exemplo e ajuste conforme necessário:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure as variáveis:

```env
# Porta do servidor
PORT=5000

# Host do servidor
HOST=0.0.0.0

# Modo debug (false em produção)
DEBUG=false

# Chave secreta (obrigatório em produção)
SECRET_KEY=sua-chave-secreta-aqui

# Arquivo de configuração da API
CONFIG_FILE=config.yaml
```

#### Arquivo `config.yaml` (Configuração da API Cora)

Certifique-se de que o arquivo `config.yaml` está configurado corretamente na raiz do projeto:

```yaml
api:
  auth_url: https://matls-clients.api.cora.com.br/token
  base_url: https://matls-clients.api.cora.com.br/v2/invoices

credentials:
  client_id: SEU_CLIENT_ID_AQUI

certificates:
  cert_path: certificados/certificate.pem
  key_path: certificados/private-key.key

debug: false
```

⚠️ **Importante**: O arquivo `.env` é carregado automaticamente pelo `python-dotenv`. As variáveis de ambiente podem ser configuradas via arquivo `.env` ou diretamente no sistema operacional.

## 🏃 Como Executar

### Primeira Execução

Na primeira vez que executar, o `app.py` fará verificações automáticas:

```bash
python app.py
```

Se alguma dependência estiver faltando, o sistema tentará instalar automaticamente ou exibirá instruções.

💡 **Dica**: Para uma instalação completa e verificada, execute primeiro:
```bash
python setup_app.py
```

### Modo de Desenvolvimento

```bash
python app.py
```

A aplicação será iniciada em `http://localhost:5000` por padrão.

### Configuração via Arquivo `.env` (Recomendado)

1. Copie o arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```

2. Edite o arquivo `.env` e ajuste as configurações

3. Execute a aplicação:
   ```bash
   python app.py
   ```

### Configuração via Variáveis de Ambiente do Sistema

Alternativamente, você pode configurar as variáveis diretamente no sistema:

```bash
# Linux/Mac
export PORT=5000
export HOST=0.0.0.0
export DEBUG=True
export SECRET_KEY=sua-chave-secreta-aqui
export CONFIG_FILE=config.yaml

python app.py
```

```bash
# Windows (PowerShell)
$env:PORT=5000
$env:HOST="0.0.0.0"
$env:DEBUG="True"
$env:SECRET_KEY="sua-chave-secreta-aqui"
$env:CONFIG_FILE="config.yaml"

python app.py
```

### Executar com Variáveis de Ambiente Inline

```bash
PORT=8000 DEBUG=True python app.py
```

## 📱 Uso da Aplicação

### 1. Página Inicial

Acesse `http://localhost:5000` no navegador.

Você verá um formulário para buscar um boleto por ID (invoice_id).

### 2. Buscar Boleto

1. Digite o ID do boleto no campo de busca
2. Clique em "Buscar Boleto"
3. A aplicação buscará o boleto na API do Cora

### 3. Visualizar Boleto

Após buscar o boleto, você verá:

- **Status do Pagamento**: Se o boleto está pago ou pendente
- **Informações do Boleto**: ID, código, valor, data de vencimento
- **Dados do Cliente**: Nome, CPF/CNPJ, email
- **Formas de Pagamento**: Boleto bancário e/ou PIX
- **QR Code PIX**: Se disponível, exibido como imagem
- **Código de Barras**: Do boleto bancário
- **Link para Visualizar Boleto**: Link direto para o boleto

## 🔌 API REST

A aplicação também expõe uma API REST para consulta programática:

### GET /api/boleto/<invoice_id>

Consulta um boleto e retorna os dados em JSON.

**Exemplo de Requisição:**

```bash
curl http://localhost:5000/api/boleto/inv_123456789
```

**Exemplo de Resposta:**

```json
{
  "id": "inv_123456789",
  "code": "BOL001",
  "status": "PENDING",
  "esta_pago": false,
  "amount": 150000,
  "due_date": "2024-02-15",
  "customer": {
    "name": "João da Silva",
    "document": "12345678909"
  },
  "payment_forms": [
    {
      "type": "BANK_SLIP",
      "url": "https://api.cora.com.br/boleto/123456789",
      "barcode": "12345678901234567890123456789012345678901234"
    }
  ]
}
```

## 🛠️ Estrutura da Aplicação

```
cora_boletos/
├── app.py                    # Aplicação Flask principal
├── libs/
│   ├── auth.py              # Autenticação (já existente)
│   ├── consulta.py          # Módulo de consulta de boletos (novo)
│   └── gerador.py           # Geração de boletos (já existente)
└── templates/
    ├── base.html            # Template base
    ├── index.html           # Página inicial (busca)
    └── visualizar.html      # Página de visualização do boleto
```

## 🔐 Segurança

### Em Produção

⚠️ **IMPORTANTE**: Para uso em produção, configure:

1. **SECRET_KEY**: Defina uma chave secreta forte através da variável de ambiente `SECRET_KEY`
2. **HTTPS**: Configure um proxy reverso (nginx, Apache) com SSL/TLS
3. **Firewall**: Restrinja o acesso à aplicação
4. **Autenticação**: Considere adicionar autenticação de usuários se necessário

### Exemplo de Configuração com Nginx

```nginx
server {
    listen 443 ssl;
    server_name seu-dominio.com;
    
    ssl_certificate /caminho/para/certificado.crt;
    ssl_certificate_key /caminho/para/chave.key;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🐛 Troubleshooting

### Erro: "Arquivo de configuração não encontrado"

Certifique-se de que o arquivo `config.yaml` existe na raiz do projeto ou configure a variável de ambiente `CONFIG_FILE`.

### Erro: "Erro ao inicializar sistema"

Verifique:
- Se os certificados estão no caminho correto
- Se o `client_id` está correto
- Se as URLs da API estão corretas
- Se há conectividade com a API do Cora

### Erro: "Boleto não encontrado"

Verifique se o ID do boleto está correto. O ID deve ser o `invoice_id` retornado pela API quando o boleto foi criado.

### Porta já em uso

Se a porta 5000 já estiver em uso, configure outra porta através da variável de ambiente `PORT`:

```bash
PORT=8000 python app.py
```

## 📝 Logs

A aplicação registra logs de todas as operações. Em modo debug, logs mais detalhados são exibidos.

Os logs incluem:
- Requisições de busca de boletos
- Erros de autenticação
- Erros de consulta à API
- Status das requisições

## 🔄 Integração com o Sistema Existente

A aplicação web utiliza os mesmos módulos de autenticação e configuração do sistema existente:

- **libs.auth.CoraAuth**: Para autenticação com a API
- **config.yaml**: Mesmo arquivo de configuração
- **Certificados**: Mesmos certificados mTLS

Isso garante consistência e facilita a manutenção.

## 📚 Endpoints da API Cora Utilizados

A aplicação utiliza o seguinte endpoint da API do Cora:

- **GET /v2/invoices/{invoice_id}**: Consulta um boleto específico por ID

Para mais informações sobre a API do Cora, consulte a documentação em `docs/API.md`.

---

**Desenvolvido para facilitar a consulta de boletos pelos clientes**
