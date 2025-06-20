# Testes do Sistema de Geração de Boletos Cora

Este diretório contém os testes automatizados para o sistema de geração de boletos integrado com a API da Cora.

## 📁 Estrutura dos Testes

```
tests/
├── __init__.py              # Pacote Python
├── conftest.py              # Configuração do pytest
├── test_validacoes.py       # Testes de validação dos dataclasses
└── README.md               # Este arquivo
```

## 🧪 Executando os Testes

### Pré-requisitos
```bash
pip install pytest pytest-cov
```

### Executar todos os testes
```bash
pytest tests/
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

### Executar com cobertura
```bash
pytest tests/ --cov=libs --cov-report=html
```

## 📋 Tipos de Testes

### 1. **Testes de Validação** (`@pytest.mark.validation`)
- Validação de CPF/CNPJ
- Validação de email
- Validação de CEP
- Validação de datas
- Validação de valores monetários

### 2. **Testes Unitários** (`@pytest.mark.unit`)
- Funcionalidade individual de cada classe
- Métodos específicos
- Conversões de formato

### 3. **Testes de Integração** (`@pytest.mark.integration`)
- Fluxo completo de criação de boletos
- Interação entre diferentes classes
- Conversão para JSON

## 🎯 Classes Testadas

### CustomerDocument
- ✅ Validação de CPF
- ✅ Validação de CNPJ
- ✅ Formatação automática
- ✅ Detecção de tipo de documento

### CustomerAddress
- ✅ Validação de CEP
- ✅ Campos obrigatórios
- ✅ Formatação de endereço

### Customer
- ✅ Validação de email
- ✅ Nome obrigatório
- ✅ Integração com documento

### Service
- ✅ Validação de valor
- ✅ Campos obrigatórios
- ✅ Formatação de descrição

### NotificationChannel
- ✅ Canais válidos (EMAIL, SMS, WHATSAPP)
- ✅ Regras válidas
- ✅ Contato obrigatório

### Interest
- ✅ Taxa de juros válida (0-100%)
- ✅ Conversão para dicionário
- ✅ Valores nulos

### Fine
- ✅ Valor da multa válido
- ✅ Data da multa válida
- ✅ Conversão para dicionário

### PaymentTerms
- ✅ Data de vencimento futura
- ✅ Formato de data válido
- ✅ Integração com juros e multa

### BoletoData
- ✅ Criação completa de boleto
- ✅ Conversão para JSON
- ✅ Campos opcionais

## 🔧 Configuração do Pytest

O arquivo `conftest.py` configura:
- **PYTHONPATH**: Adiciona o diretório raiz para importar módulos
- **Marcadores**: Define marcadores personalizados para categorizar testes
- **Configuração automática**: Aplica marcadores baseados no nome do teste

## 📊 Relatórios de Cobertura

Para gerar relatórios detalhados de cobertura:

```bash
# Relatório HTML (abre no navegador)
pytest tests/ --cov=libs --cov-report=html
open htmlcov/index.html

# Relatório no terminal
pytest tests/ --cov=libs --cov-report=term-missing

# Relatório XML (para CI/CD)
pytest tests/ --cov=libs --cov-report=xml
```

## 🚀 Boas Práticas

1. **Nomes descritivos**: Use nomes que descrevem o que está sendo testado
2. **Um assert por teste**: Cada teste deve verificar uma coisa específica
3. **Setup e teardown**: Use fixtures do pytest para configuração
4. **Dados de teste**: Use dados realistas mas fictícios
5. **Documentação**: Documente casos de teste complexos

## 🐛 Debugging

Para debugar testes:

```bash
# Executar com mais detalhes
pytest tests/ -v

# Parar no primeiro erro
pytest tests/ -x

# Mostrar output completo
pytest tests/ -s

# Executar teste específico com debug
pytest tests/test_validacoes.py::TestCustomerDocument::test_cpf_valido -s -v
``` 