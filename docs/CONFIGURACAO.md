# ⚙️ Guia de Configuração

Guia completo para configurar o sistema de geração de boletos Cora.

## 📋 Pré-requisitos

### Software Necessário
- **Python**: 3.8 ou superior
- **Git**: Para clonar o repositório
- **Editor de código**: VS Code, PyCharm, etc.

### Conta na Cora
- **Cadastro**: Conta ativa na Cora
- **Certificado Digital**: Arquivos `.pem` e `.key`
- **Client ID**: Identificador único fornecido pela Cora

## 🚀 Instalação Inicial

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/cora_boletos.git
cd cora_boletos
```

### 2. Ambiente Virtual
```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente (Linux/Mac)
source .venv/bin/activate

# Ativar ambiente (Windows)
.venv\Scripts\activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Verificar Instalação
```bash
python -c "import pandas, requests, yaml; print('✅ Dependências instaladas com sucesso!')"
```

## 🔧 Configuração do Sistema

### 1. Arquivo de Configuração

Crie o arquivo `config.yaml` na raiz do projeto:

```yaml
# Configurações da API Cora
api:
  auth_url: https://matls-clients.api.cora.com.br/token
  base_url: https://matls-clients.api.cora.com.br/v2/invoices
  timeout: 30
  retries: 3

# Credenciais de acesso
credentials:
  client_id: SEU_CLIENT_ID_AQUI

# Certificados digitais
certificates:
  cert_path: certificados/certificate.pem
  key_path: certificados/private-key.key

# Configurações de log
logging:
  level: INFO
  file: boletos.log
  max_size: 10MB
  backup_count: 5

# Configurações padrão
defaults:
  juros_mensal: 1.0  # 1% ao mês
  multa: 5.00        # R$ 5,00
  dias_vencimento: 10
  formas_pagamento: ["BANK_SLIP", "PIX"]

# Configurações de notificação
notifications:
  email_enabled: true
  sms_enabled: true
  whatsapp_enabled: false
```

### 2. Estrutura de Certificados

Crie a pasta de certificados:
```bash
mkdir certificados
```

Adicione seus arquivos de certificado:
```
certificados/
├── certificate.pem    # Certificado público
└── private-key.key    # Chave privada
```

### 3. Permissões de Arquivos

Configure as permissões corretas:
```bash
# Linux/Mac
chmod 600 certificados/private-key.key
chmod 644 certificados/certificate.pem

# Windows (PowerShell)
icacls certificados/private-key.key /inheritance:r /grant:r "%USERNAME%:F"
```

## 🔐 Configuração de Segurança

### 1. Validação de Certificados

O sistema valida automaticamente:
- ✅ Existência dos arquivos
- ✅ Formato correto dos certificados
- ✅ Permissões adequadas
- ✅ Data de expiração

### 2. Variáveis de Ambiente (Opcional)

Para maior segurança, você pode usar variáveis de ambiente:

```bash
# Linux/Mac
export CORA_CLIENT_ID="seu_client_id"
export CORA_CERT_PATH="certificados/certificate.pem"
export CORA_KEY_PATH="certificados/private-key.key"

# Windows
set CORA_CLIENT_ID=seu_client_id
set CORA_CERT_PATH=certificados/certificate.pem
set CORA_KEY_PATH=certificados/private-key.key
```

### 3. Arquivo .env (Alternativo)

Crie um arquivo `.env` na raiz:
```env
CORA_CLIENT_ID=seu_client_id
CORA_CERT_PATH=certificados/certificate.pem
CORA_KEY_PATH=certificados/private-key.key
CORA_API_URL=https://matls-clients.api.cora.com.br/v2/invoices
CORA_AUTH_URL=https://matls-clients.api.cora.com.br/token
```

## 📁 Estrutura de Diretórios

### Organização Recomendada
```
cora_boletos/
├── config.yaml              # Configuração principal
├── certificados/            # Certificados digitais
│   ├── certificate.pem
│   └── private-key.key
├── dados/                   # Arquivos de entrada
│   ├── clientes.xlsx
│   └── boletos_pendentes.csv
├── saida/                   # Arquivos gerados
│   ├── boletos_gerados/
│   ├── logs/
│   └── relatorios/
└── backups/                 # Backups automáticos
    └── certificados/
```

### Scripts de Configuração

Crie scripts para facilitar a configuração:

#### `setup.sh` (Linux/Mac)
```bash
#!/bin/bash
echo "🔧 Configurando sistema de boletos Cora..."

# Criar diretórios
mkdir -p certificados dados saida/boletos_gerados saida/logs saida/relatorios backups

# Configurar permissões
chmod 600 certificados/private-key.key
chmod 644 certificados/certificate.pem

# Verificar Python
python3 --version

# Verificar dependências
pip list | grep -E "(pandas|requests|pyyaml)"

echo "✅ Configuração concluída!"
```

#### `setup.bat` (Windows)
```batch
@echo off
echo 🔧 Configurando sistema de boletos Cora...

REM Criar diretórios
mkdir certificados dados saida\boletos_gerados saida\logs saida\relatorios backups

REM Verificar Python
python --version

REM Verificar dependências
pip list | findstr "pandas requests pyyaml"

echo ✅ Configuração concluída!
pause
```

## 🧪 Configuração de Testes

### 1. Ambiente de Teste

Para desenvolvimento, use o ambiente sandbox:

```yaml
# config_sandbox.yaml
api:
  auth_url: https://sandbox-matls-clients.api.cora.com.br/token
  base_url: https://sandbox-matls-clients.api.cora.com.br/v2/invoices
  timeout: 30
  retries: 3

credentials:
  client_id: SEU_CLIENT_ID_SANDBOX

certificates:
  cert_path: certificados/certificate_sandbox.pem
  key_path: certificados/private-key_sandbox.key
```

### 2. Executar Testes
```bash
# Todos os testes
pytest tests/ -v

# Apenas testes de configuração
pytest tests/ -k "config" -v

# Com cobertura
pytest tests/ --cov=libs --cov-report=html
```

## 🔍 Validação da Configuração

### 1. Script de Verificação

Crie um script para validar a configuração:

```python
#!/usr/bin/env python3
"""
Script para validar a configuração do sistema.
"""

import os
import yaml
from pathlib import Path

def validar_configuracao():
    """Valida toda a configuração do sistema"""
    
    print("🔍 Validando configuração...")
    
    # Verificar arquivo config.yaml
    if not os.path.exists('config.yaml'):
        print("❌ Arquivo config.yaml não encontrado")
        return False
    
    # Carregar configuração
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print("✅ config.yaml carregado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao carregar config.yaml: {e}")
        return False
    
    # Verificar certificados
    cert_path = config.get('certificates', {}).get('cert_path')
    key_path = config.get('certificates', {}).get('key_path')
    
    if not os.path.exists(cert_path):
        print(f"❌ Certificado não encontrado: {cert_path}")
        return False
    
    if not os.path.exists(key_path):
        print(f"❌ Chave privada não encontrada: {key_path}")
        return False
    
    print("✅ Certificados encontrados")
    
    # Verificar permissões (Linux/Mac)
    if os.name != 'nt':  # Não Windows
        key_stat = os.stat(key_path)
        if key_stat.st_mode & 0o777 != 0o600:
            print(f"⚠️  Permissões da chave privada devem ser 600")
            print(f"   Execute: chmod 600 {key_path}")
    
    # Verificar Python e dependências
    try:
        import pandas
        import requests
        import yaml
        print("✅ Dependências Python OK")
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False
    
    # Verificar estrutura de diretórios
    diretorios = ['certificados', 'dados', 'saida', 'backups']
    for dir in diretorios:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f"📁 Diretório criado: {dir}")
    
    print("✅ Configuração válida!")
    return True

if __name__ == "__main__":
    validar_configuracao()
```

### 2. Executar Validação
```bash
python scripts/validar_config.py
```

## 🔄 Configurações Avançadas

### 1. Logs Detalhados

Para debug, configure logs mais detalhados:

```yaml
logging:
  level: DEBUG
  file: boletos_debug.log
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  max_size: 50MB
  backup_count: 10
```

### 2. Timeouts Personalizados

Para conexões lentas:

```yaml
api:
  timeout: 60
  retries: 5
  retry_delay: 2
```

### 3. Configuração de Proxy

Se necessário usar proxy:

```yaml
proxy:
  enabled: true
  http: http://proxy.empresa.com:8080
  https: https://proxy.empresa.com:8080
  username: usuario
  password: senha
```

## 🚨 Troubleshooting

### Problemas Comuns

#### 1. Certificado Inválido
```bash
# Verificar formato
openssl x509 -in certificados/certificate.pem -text -noout

# Verificar data de expiração
openssl x509 -in certificados/certificate.pem -noout -dates
```

#### 2. Permissões Incorretas
```bash
# Corrigir permissões
chmod 600 certificados/private-key.key
chmod 644 certificados/certificate.pem
```

#### 3. Client ID Inválido
- Verifique se o Client ID está correto
- Confirme se a conta está ativa na Cora
- Teste a autenticação manualmente

#### 4. Problemas de Rede
```bash
# Testar conectividade
curl -v https://matls-clients.api.cora.com.br/token

# Verificar DNS
nslookup matls-clients.api.cora.com.br
```

## 📞 Suporte

### Contatos
- **Email**: suporte@cora.com.br
- **Telefone**: (11) 3000-0000
- **Documentação**: https://docs.cora.com.br

### Logs para Suporte
```bash
# Coletar logs
tail -n 100 boletos.log > logs_suporte.txt

# Informações do sistema
python -c "import sys, platform; print(f'Python: {sys.version}'); print(f'OS: {platform.system()}')"
```

---

**Última atualização**: Junho 2025
**Versão**: 2.0 