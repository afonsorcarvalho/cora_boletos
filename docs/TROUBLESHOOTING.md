# 🐛 Solução de Problemas

Guia completo para resolver problemas comuns no sistema de geração de boletos Cora.

## 🚨 Problemas Críticos

### 1. Erro de Autenticação

#### Sintoma
```
ValueError: Certificado não encontrado: certificados/certificate.pem
```

#### Causa
- Arquivo de certificado não existe
- Caminho incorreto no config.yaml
- Permissões incorretas

#### Solução
```bash
# 1. Verificar se os arquivos existem
ls -la certificados/

# 2. Corrigir permissões
chmod 600 certificados/private-key.key
chmod 644 certificados/certificate.pem

# 3. Verificar config.yaml
cat config.yaml | grep -A 5 certificates
```

#### Prevenção
- Sempre use o script de validação antes de executar
- Mantenha backup dos certificados
- Configure permissões corretas

### 2. Erro de Token Expirado

#### Sintoma
```
401 Unauthorized: Token expired
```

#### Causa
- Token de acesso expirou
- Problema na renovação automática
- Certificado expirado

#### Solução
```python
# Forçar renovação do token
auth = CoraAuth(...)
auth._token = None  # Limpar token cache
auth._token_expiry = None
token = auth.get_access_token()
```

#### Prevenção
- Configure logs para monitorar expiração
- Use certificados com validade adequada
- Implemente retry automático

### 3. Erro de Rate Limit

#### Sintoma
```
429 Too Many Requests
```

#### Causa
- Muitas requisições em pouco tempo
- Limite da API excedido

#### Solução
```python
import time

def gerar_com_retry(dados, max_tentativas=3):
    for tentativa in range(max_tentativas):
        try:
            return gerador.gerar_boleto_individual(dados)
        except Exception as e:
            if "429" in str(e):
                delay = 2 ** tentativa  # Backoff exponencial
                print(f"Aguardando {delay} segundos...")
                time.sleep(delay)
            else:
                raise
```

## 🔍 Problemas de Validação

### 1. CPF/CNPJ Inválido

#### Sintoma
```
ValueError: CPF inválido: 123.456.789-10
```

#### Causa
- Documento com dígitos incorretos
- Formato inválido
- Documento inexistente

#### Solução
```python
# Usar documentos válidos para teste
documentos_validos = {
    "cpf": "123.456.789-09",
    "cnpj": "11.222.333/0001-81"
}

# Validar antes de usar
from libs.gerador import CustomerDocument
try:
    doc = CustomerDocument("123.456.789-09", "CPF")
    print("✅ CPF válido")
except ValueError as e:
    print(f"❌ CPF inválido: {e}")
```

#### Prevenção
- Use geradores de CPF/CNPJ válidos para testes
- Implemente validação no frontend
- Mantenha lista de documentos válidos

### 2. Email Inválido

#### Sintoma
```
ValueError: Email inválido: email-invalido
```

#### Causa
- Formato de email incorreto
- Domínio inexistente
- Caracteres especiais

#### Solução
```python
import re

def validar_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Testar
emails_teste = [
    "usuario@email.com",      # ✅ Válido
    "usuario@dominio.com.br", # ✅ Válido
    "email-invalido",         # ❌ Inválido
    "@dominio.com",           # ❌ Inválido
]

for email in emails_teste:
    print(f"{email}: {'✅' if validar_email(email) else '❌'}")
```

### 3. Data de Vencimento Inválida

#### Sintoma
```
ValueError: Data de vencimento não pode estar no passado
```

#### Causa
- Data anterior ao dia atual
- Formato incorreto
- Timezone incorreto

#### Solução
```python
from datetime import datetime, timedelta

# Data válida (futura)
data_valida = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')

# Validar formato
def validar_data(data_str):
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d')
        if data.date() <= datetime.now().date():
            return False, "Data deve ser futura"
        return True, "Data válida"
    except ValueError:
        return False, "Formato deve ser YYYY-MM-DD"
```

## 💰 Problemas de Valores Monetários

### 1. Valor Negativo

#### Sintoma
```
ValueError: Valor deve ser maior que zero
```

#### Causa
- Valor negativo no arquivo
- Erro de cálculo
- Formato incorreto

#### Solução
```python
def formatar_valor(valor):
    """Formata valor monetário corretamente"""
    if isinstance(valor, str):
        # Remove R$ e espaços
        valor = valor.replace('R$', '').replace(' ', '')
        # Converte vírgula para ponto
        valor = valor.replace(',', '.')
    
    valor_float = float(valor)
    
    if valor_float <= 0:
        raise ValueError("Valor deve ser maior que zero")
    
    return valor_float
```

### 2. Formato de Valor Incorreto

#### Sintoma
```
ValueError: Formato de valor inválido
```

#### Causa
- Separadores incorretos
- Múltiplas vírgulas/pontos
- Caracteres especiais

#### Solução
```python
import re

def limpar_valor_monetario(valor_str):
    """Limpa e converte valor monetário"""
    # Remove caracteres não numéricos exceto vírgula e ponto
    valor_limpo = re.sub(r'[^\d,.]', '', str(valor_str))
    
    # Se tem vírgula e ponto, assume que vírgula é separador de milhar
    if ',' in valor_limpo and '.' in valor_limpo:
        valor_limpo = valor_limpo.replace(',', '')
    
    # Converte vírgula para ponto
    valor_limpo = valor_limpo.replace(',', '.')
    
    return float(valor_limpo)
```

## 📁 Problemas de Arquivos

### 1. Arquivo Excel Não Encontrado

#### Sintoma
```
FileNotFoundError: [Errno 2] No such file or directory: 'arquivo.xlsx'
```

#### Causa
- Arquivo não existe
- Caminho incorreto
- Permissões de leitura

#### Solução
```python
import os
from pathlib import Path

def verificar_arquivo(caminho):
    """Verifica se arquivo existe e é legível"""
    arquivo = Path(caminho)
    
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {caminho}")
        return False
    
    if not arquivo.is_file():
        print(f"❌ Não é um arquivo: {caminho}")
        return False
    
    if not os.access(arquivo, os.R_OK):
        print(f"❌ Sem permissão de leitura: {caminho}")
        return False
    
    print(f"✅ Arquivo válido: {caminho}")
    return True
```

### 2. Formato de Excel Incorreto

#### Sintoma
```
KeyError: 'nome' - Coluna não encontrada
```

#### Causa
- Colunas com nomes diferentes
- Arquivo vazio
- Formato incorreto

#### Solução
```python
import pandas as pd

def verificar_excel(arquivo):
    """Verifica estrutura do arquivo Excel"""
    try:
        df = pd.read_excel(arquivo)
        
        # Verificar se está vazio
        if df.empty:
            print("❌ Arquivo Excel está vazio")
            return False
        
        # Verificar colunas obrigatórias
        colunas_obrigatorias = ['nome', 'email', 'documento', 'valor']
        colunas_faltando = [col for col in colunas_obrigatorias if col not in df.columns]
        
        if colunas_faltando:
            print(f"❌ Colunas faltando: {colunas_faltando}")
            print(f"Colunas encontradas: {list(df.columns)}")
            return False
        
        print(f"✅ Arquivo Excel válido com {len(df)} registros")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler Excel: {e}")
        return False
```

## 🌐 Problemas de Rede

### 1. Timeout de Conexão

#### Sintoma
```
requests.exceptions.ConnectTimeout: HTTPSConnectionPool
```

#### Causa
- Conexão lenta
- Firewall bloqueando
- Servidor indisponível

#### Solução
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def criar_sessao_com_retry():
    """Cria sessão com retry automático"""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session
```

### 2. Erro de DNS

#### Sintoma
```
requests.exceptions.ConnectionError: Name or service not known
```

#### Causa
- DNS não resolve
- URL incorreta
- Problema de rede

#### Solução
```bash
# Testar resolução DNS
nslookup matls-clients.api.cora.com.br

# Testar conectividade
ping matls-clients.api.cora.com.br

# Verificar configuração de proxy
echo $http_proxy
echo $https_proxy
```

## 🔧 Problemas de Configuração

### 1. Configuração Inválida

#### Sintoma
```
yaml.parser.ParserError: while parsing a block mapping
```

#### Causa
- Sintaxe YAML incorreta
- Indentação errada
- Caracteres especiais

#### Solução
```python
import yaml

def validar_yaml(arquivo):
    """Valida arquivo YAML"""
    try:
        with open(arquivo, 'r') as f:
            config = yaml.safe_load(f)
        print("✅ YAML válido")
        return config
    except yaml.YAMLError as e:
        print(f"❌ Erro YAML: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return None
```

### 2. Variáveis de Ambiente

#### Sintoma
```
KeyError: 'COR_CLIENT_ID'
```

#### Causa
- Variável não definida
- Nome incorreto
- Ambiente não carregado

#### Solução
```python
import os
from dotenv import load_dotenv

def carregar_configuracao():
    """Carrega configuração de múltiplas fontes"""
    # 1. Tentar carregar .env
    load_dotenv()
    
    # 2. Verificar variáveis de ambiente
    config = {}
    
    # Configuração da API
    config['client_id'] = os.getenv('CORA_CLIENT_ID')
    config['cert_path'] = os.getenv('CORA_CERT_PATH')
    config['key_path'] = os.getenv('CORA_KEY_PATH')
    
    # 3. Verificar se todas as variáveis estão definidas
    variaveis_faltando = [k for k, v in config.items() if not v]
    
    if variaveis_faltando:
        print(f"❌ Variáveis faltando: {variaveis_faltando}")
        return None
    
    return config
```

## 📊 Problemas de Performance

### 1. Geração Lenta

#### Sintoma
- Geração de muitos boletos demora muito
- Timeout em lotes grandes

#### Causa
- Requisições sequenciais
- Sem cache de token
- Conexões não reutilizadas

#### Solução
```python
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

async def gerar_boletos_paralelo(dados_lista, max_concurrent=5):
    """Gera boletos em paralelo"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def gerar_boleto(dados):
        async with semaphore:
            # Lógica de geração aqui
            return await gerar_boleto_individual(dados)
    
    tasks = [gerar_boleto(dados) for dados in dados_lista]
    resultados = await asyncio.gather(*tasks, return_exceptions=True)
    
    return resultados
```

### 2. Alto Uso de Memória

#### Sintoma
- Processo consome muita RAM
- Sistema fica lento

#### Causa
- Carregar muitos dados na memória
- Não liberar recursos
- Cache muito grande

#### Solução
```python
import gc

def processar_lote_otimizado(arquivo_excel, tamanho_lote=100):
    """Processa arquivo em lotes para economizar memória"""
    for chunk in pd.read_excel(arquivo_excel, chunksize=tamanho_lote):
        # Processar lote
        for _, row in chunk.iterrows():
            gerar_boleto_individual(row.to_dict())
        
        # Limpar memória
        gc.collect()
```

## 🧪 Debugging

### 1. Logs Detalhados

```python
import logging

def configurar_logs_detalhados():
    """Configura logs detalhados para debug"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('debug.log'),
            logging.StreamHandler()
        ]
    )
    
    # Log específico para requests
    logging.getLogger('urllib3').setLevel(logging.DEBUG)
    logging.getLogger('requests').setLevel(logging.DEBUG)
```

### 2. Teste de Conectividade

```python
def teste_conectividade():
    """Testa conectividade com a API"""
    import requests
    
    urls_teste = [
        "https://matls-clients.api.cora.com.br/token",
        "https://matls-clients.api.cora.com.br/v2/invoices"
    ]
    
    for url in urls_teste:
        try:
            response = requests.get(url, timeout=10)
            print(f"✅ {url}: {response.status_code}")
        except Exception as e:
            print(f"❌ {url}: {e}")
```

### 3. Validação de Certificados

```python
def validar_certificados():
    """Valida certificados digitalmente"""
    import subprocess
    
    cert_path = "certificados/certificate.pem"
    key_path = "certificados/private-key.key"
    
    # Verificar certificado
    try:
        result = subprocess.run([
            'openssl', 'x509', '-in', cert_path, 
            '-text', '-noout'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Certificado válido")
        else:
            print(f"❌ Certificado inválido: {result.stderr}")
    except FileNotFoundError:
        print("⚠️  OpenSSL não encontrado")
```

## 🔒 Problemas de SSL/Certbot

### 1. Erro: "Invalid version. The only valid version for X509Req is 0" no Ubuntu 18.04

#### Sintoma
```
ValueError: Invalid version. The only valid version for X509Req is 0.
```

#### Causa
Este erro ocorre devido a uma incompatibilidade entre versões do Certbot e a biblioteca `pyOpenSSL` no Ubuntu 18.04. O `pyOpenSSL` versão 23.2.0 introduziu validações mais rigorosas que conflitam com versões antigas do Certbot.

#### Solução 1: Atualizar Certbot via Snap (Recomendado)

A forma mais confiável de resolver o problema é instalar o Certbot usando o Snap, que sempre terá a versão mais recente e compatível:

```bash
# Remover versão antiga do Certbot (se instalada via apt)
sudo apt remove certbot

# Instalar Certbot via Snap
sudo snap install --classic certbot

# Criar link simbólico (se necessário)
sudo ln -sf /snap/bin/certbot /usr/bin/certbot

# Verificar instalação
certbot --version
```

**Nota**: O Ubuntu 18.04 usa Python 3.6, que não é mais suportado por versões muito recentes do Certbot. Se encontrar problemas, considere a Solução 2.

#### Solução 2: Fazer Downgrade do pyOpenSSL

Se não puder atualizar o Certbot, faça downgrade do `pyOpenSSL` para uma versão compatível:

```bash
# Verificar versão atual do pyOpenSSL
pip3 show pyOpenSSL

# Fazer downgrade para versão compatível
sudo pip3 install pyOpenSSL==23.1.1

# Verificar se o problema foi resolvido
certbot --version
```

#### Solução 3: Usar Certbot via Docker (Alternativa)

Se as soluções acima não funcionarem, você pode usar o Certbot via Docker:

```bash
# Criar diretório para certificados
sudo mkdir -p /etc/letsencrypt

# Executar Certbot via Docker
sudo docker run -it --rm \
  -v /etc/letsencrypt:/etc/letsencrypt \
  -v /var/lib/letsencrypt:/var/lib/letsencrypt \
  -v /tmp/letsencrypt:/var/log/letsencrypt \
  certbot/certbot certonly --standalone \
  -d boletos.jgma.com.br
```

#### Verificação

Após aplicar uma das soluções, teste novamente:

```bash
# Testar obtenção de certificado (modo teste)
sudo certbot certonly --standalone --test-cert -d boletos.jgma.com.br

# Se funcionar, obter certificado real
sudo certbot certonly --standalone -d boletos.jgma.com.br
```

#### Configuração do Nginx após obter certificado

Após obter o certificado com sucesso, configure o Nginx:

```nginx
server {
    listen 80;
    server_name boletos.jgma.com.br;
    
    # Redirecionar HTTP para HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name boletos.jgma.com.br;
    
    # Certificados Let's Encrypt
    ssl_certificate /etc/letsencrypt/live/boletos.jgma.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/boletos.jgma.com.br/privkey.pem;
    
    # Configurações SSL recomendadas
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Proxy para aplicação Flask
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Renovação Automática

Configure renovação automática dos certificados:

```bash
# Testar renovação
sudo certbot renew --dry-run

# Adicionar ao crontab para renovação automática
sudo crontab -e

# Adicionar linha (renova diariamente às 3h da manhã)
0 3 * * * certbot renew --quiet --deploy-hook "systemctl reload nginx"
```

#### Prevenção

- **Atualize o sistema**: Considere atualizar para Ubuntu 20.04 ou superior, que tem melhor suporte
- **Use Snap**: Prefira instalar Certbot via Snap para sempre ter versões atualizadas
- **Monitore renovação**: Configure alertas para verificar se a renovação automática está funcionando

### 2. Certificado Expirado

#### Sintoma
```
SSL certificate problem: certificate has expired
```

#### Solução
```bash
# Renovar certificado manualmente
sudo certbot renew

# Ou renovar certificado específico
sudo certbot renew --cert-name boletos.jgma.com.br

# Recarregar Nginx após renovação
sudo systemctl reload nginx
```

## 📞 Suporte

### Informações para Suporte

Quando precisar de ajuda, forneça:

1. **Logs de erro**:
```bash
tail -n 50 boletos.log > erro_suporte.txt
```

2. **Informações do sistema**:
```bash
python -c "
import sys, platform, requests
print(f'Python: {sys.version}')
print(f'OS: {platform.system()} {platform.release()}')
print(f'Requests: {requests.__version__}')
"
```

3. **Configuração (sem dados sensíveis)**:
```bash
cat config.yaml | grep -v "client_id\|cert_path\|key_path"
```

4. **Teste de conectividade**:
```bash
curl -v https://matls-clients.api.cora.com.br/token
```

### Contatos de Suporte

- **Email**: suporte@cora.com.br
- **Telefone**: (11) 3000-0000
- **Horário**: Segunda a Sexta, 8h às 18h
- **Documentação**: https://docs.cora.com.br

---

**Última atualização**: Junho 2025
**Versão**: 2.0 