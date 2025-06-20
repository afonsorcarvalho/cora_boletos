# 🏦 Sistema de Geração de Boletos Cora

Sistema robusto e completo para geração automatizada de boletos utilizando a API da Cora, com validações avançadas, testes automatizados e documentação detalhada.

## 🚀 Características Principais

- ✅ **Validações Automáticas**: CPF/CNPJ, email, CEP, datas e valores monetários
- ✅ **Testes Abrangentes**: Cobertura completa com pytest
- ✅ **Documentação Detalhada**: Guias de uso e exemplos práticos
- ✅ **Estrutura Organizada**: Código modular e bem estruturado
- ✅ **Tratamento de Erros**: Mensagens claras e tratamento robusto
- ✅ **Configuração Flexível**: Suporte a diferentes formatos de dados

## 📁 Estrutura do Projeto

```
cora_boletos/
├── 📚 docs/                    # Documentação detalhada
│   ├── API.md                 # Documentação da API Cora
│   ├── CONFIGURACAO.md        # Guia de configuração
│   ├── EXEMPLOS.md            # Exemplos de uso
│   └── TROUBLESHOOTING.md     # Solução de problemas
├── 🧪 tests/                  # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py            # Configuração do pytest
│   ├── test_validacoes.py     # Testes de validação
│   ├── test_gerador.py        # Testes do gerador
│   ├── test_auth.py           # Testes de autenticação
│   └── README.md              # Documentação dos testes
├── 📖 examples/               # Exemplos práticos
│   ├── gerar_boleto_direto.py # Exemplo sem Excel
│   └── README.md              # Guia dos exemplos
├── 🔧 libs/                   # Biblioteca principal
│   ├── __init__.py
│   ├── auth.py                # Autenticação com a API
│   └── gerador.py             # Geração de boletos
├── ⚙️ scripts/                # Scripts executáveis
├── 📄 config.yaml             # Configuração centralizada
├── 📋 requirements.txt        # Dependências do projeto
└── 🚫 .gitignore              # Arquivos ignorados pelo Git
```

## 📋 Requisitos

- **Python**: 3.8 ou superior
- **Certificado Digital**: Da Cora (arquivos .pem e .key)
- **Configuração**: Arquivo `config.yaml` com credenciais

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/cora_boletos.git
cd cora_boletos
```

### 2. Crie um ambiente virtual
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Configure o arquivo `config.yaml`
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

### 2. Adicione seus certificados
```bash
mkdir certificados
# Copie seus arquivos de certificado para a pasta certificados/
```

## 🚀 Como Usar

### Método 1: Geração Direta (Recomendado para testes)
```bash
python examples/gerar_boleto_direto.py
```

### Método 2: Com arquivo Excel
```bash
python scripts/gerar_boletos.py arquivo_clientes.xlsx
```

### Método 3: Programaticamente
```python
from libs.gerador import GeradorBoletos
from libs.auth import CoraAuth

# Configure a autenticação
auth = CoraAuth(
    auth_url="https://matls-clients.api.cora.com.br/token",
    client_id="seu_client_id",
    cert_path="certificados/certificate.pem",
    key_path="certificados/private-key.key"
)

# Crie o gerador
gerador = GeradorBoletos(
    api_url="https://matls-clients.api.cora.com.br/v2/invoices",
    auth=auth,
    debug=True
)

# Gere um boleto
dados = {
    "codigo": "BOL001",
    "nome": "João Silva",
    "email": "joao@email.com",
    "documento": "123.456.789-09",
    "servico_nome": "Consultoria",
    "servico_descricao": "Serviço mensal",
    "valor": 1500.00,
    "data_vencimento": "2025-07-15"
}

resultado = gerador.gerar_boleto_individual(dados)
print(f"Boleto gerado: {resultado}")
```

## 🧪 Testes

### Executar todos os testes
```bash
pytest tests/ -v
```

### Executar testes específicos
```bash
# Apenas testes de validação
pytest tests/ -m validation

# Apenas testes unitários
pytest tests/ -m unit

# Teste específico
pytest tests/test_validacoes.py::TestCustomerDocument::test_cpf_valido
```

### Relatório de cobertura
```bash
pytest tests/ --cov=libs --cov-report=html
open htmlcov/index.html
```

## ✅ Validações Implementadas

### 📄 Documentos
- **CPF**: Validação completa com algoritmo oficial
- **CNPJ**: Validação completa com algoritmo oficial
- **Formatação**: Remoção automática de pontuação

### 📧 Email
- **Formato**: Validação de formato válido
- **Domínio**: Verificação de domínio válido

### 📍 Endereço
- **CEP**: Validação de formato brasileiro
- **Campos obrigatórios**: Rua, número, cidade, estado
- **Formatação**: Normalização automática

### 💰 Valores Monetários
- **Juros**: 0% a 100% ao mês
- **Multa**: Valores não negativos
- **Formatação**: Suporte a múltiplos formatos (R$ 1.234,56, 1234.56, etc.)

### 📅 Datas
- **Formato**: YYYY-MM-DD obrigatório
- **Vencimento**: Não pode estar no passado
- **Validação**: Verificação de data válida

## 🔧 Funcionalidades Avançadas

### 📊 Geração em Lote
- Processamento de múltiplos boletos
- Relatório de sucessos e falhas
- Tratamento de erros individual

### 🔔 Notificações
- **Email**: Notificação automática
- **SMS**: Integração com WhatsApp
- **Regras**: Configuração de quando notificar

### 💳 Formas de Pagamento
- **Boleto Bancário**: Geração automática
- **PIX**: Código QR integrado

### 🛡️ Segurança
- **Certificados**: Autenticação mTLS
- **Tokens**: Cache inteligente de tokens
- **Validação**: Verificação de certificados

## 📚 Documentação

- **[API.md](docs/API.md)**: Documentação completa da API Cora
- **[CONFIGURACAO.md](docs/CONFIGURACAO.md)**: Guia detalhado de configuração
- **[EXEMPLOS.md](docs/EXEMPLOS.md)**: Exemplos práticos de uso
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**: Solução de problemas comuns

## 🐛 Solução de Problemas

### Erro de certificado
```bash
# Verifique se os certificados existem
ls -la certificados/

# Verifique as permissões
chmod 600 certificados/private-key.key
```

### Erro de validação
```python
# Use documentos válidos
"documento": "123.456.789-09"  # ✅ CPF válido
"documento": "11.222.333/0001-81"  # ✅ CNPJ válido
```

### Erro de data
```python
# Use formato correto
"data_vencimento": "2025-07-15"  # ✅ Formato YYYY-MM-DD
```

## 🤝 Contribuição

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. **Commit** suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. **Push** para a branch (`git push origin feature/nova-feature`)
5. **Crie** um Pull Request

### Padrões de Código
- Use **type hints** em todas as funções
- Documente com **docstrings** em português
- Siga o padrão **PEP 8**
- Escreva **testes** para novas funcionalidades

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/cora_boletos/issues)
- **Documentação**: [docs/](docs/)
- **Exemplos**: [examples/](examples/)

---

**Desenvolvido com ❤️ para facilitar a geração de boletos com a API da Cora** 