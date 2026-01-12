# 🚀 Guia de Instalação Rápida

Guia rápido para instalar e configurar a aplicação web de consulta de boletos Cora.

## 📋 Instalação Automática (Recomendado)

### 1. Executar o Instalador

```bash
python setup_app.py
```

O instalador irá:
- ✅ Verificar versão do Python
- ✅ Criar/verificar ambiente virtual (se necessário)
- ✅ Instalar todas as dependências
- ✅ Criar arquivo `.env` automaticamente
- ✅ Verificar configurações básicas
- ✅ Criar diretórios necessários

### 2. Configurar Credenciais

Edite o arquivo `config.yaml` com suas credenciais da API Cora:

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

### 3. Adicionar Certificados

Coloque seus certificados na pasta `certificados/`:
- `certificate.pem` - Certificado público
- `private-key.key` - Chave privada

### 4. Configurar .env (Opcional)

Edite o arquivo `.env` se necessário (já foi criado automaticamente):

```env
PORT=5000
HOST=0.0.0.0
DEBUG=false
SECRET_KEY=sua-chave-secreta-aqui
CONFIG_FILE=config.yaml
```

### 5. Executar a Aplicação

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## 📋 Instalação Manual

Se preferir instalar manualmente:

### 1. Criar Ambiente Virtual

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Arquivos

- Copie `.env.example` para `.env`
- Configure `config.yaml` com suas credenciais
- Adicione certificados em `certificados/`

### 4. Executar

```bash
python app.py
```

## 🔧 Verificação Automática

O `app.py` possui verificação automática que:
- Cria o arquivo `.env` se não existir
- Verifica se as dependências estão instaladas
- Tenta instalar dependências faltantes automaticamente
- Exibe avisos se algo estiver faltando

## ❓ Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"

**Solução**: Execute o instalador:
```bash
python setup_app.py
```

Ou instale manualmente:
```bash
pip install -r requirements.txt
```

### Erro: "Arquivo de configuração não encontrado"

**Solução**: Crie o arquivo `config.yaml` na raiz do projeto. Veja `examples/config.example.yaml` para um exemplo.

### Erro: "Ambiente virtual não está ativado"

**Solução**: Ative o ambiente virtual:
```bash
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

Ou execute o instalador que verifica isso automaticamente.

## 📚 Documentação Completa

Para mais informações, consulte:
- `docs/APP_WEB.md` - Documentação completa da aplicação web
- `docs/CONFIGURACAO.md` - Guia detalhado de configuração
- `docs/TROUBLESHOOTING.md` - Solução de problemas
