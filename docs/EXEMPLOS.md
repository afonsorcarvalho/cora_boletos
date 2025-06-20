# 📖 Exemplos Práticos de Uso

Guia completo com exemplos práticos para usar o sistema de geração de boletos Cora.

## 🚀 Exemplos Básicos

### 1. Geração Simples de Boleto

```python
#!/usr/bin/env python3
"""
Exemplo básico de geração de boleto.
"""

from libs.gerador import GeradorBoletos
from libs.auth import CoraAuth
import yaml

def exemplo_basico():
    """Exemplo básico de geração de boleto"""
    
    # Carregar configuração
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Configurar autenticação
    auth = CoraAuth(
        auth_url=config['api']['auth_url'],
        client_id=config['credentials']['client_id'],
        cert_path=config['certificates']['cert_path'],
        key_path=config['certificates']['key_path']
    )
    
    # Criar gerador
    gerador = GeradorBoletos(
        api_url=config['api']['base_url'],
        auth=auth,
        debug=True
    )
    
    # Dados do boleto
    dados = {
        "codigo": "BOL001",
        "nome": "João Silva",
        "email": "joao@email.com",
        "documento": "123.456.789-09",
        "servico_nome": "Consultoria",
        "servico_descricao": "Serviço de consultoria mensal",
        "valor": 1500.00,
        "data_vencimento": "2024-02-15"
    }
    
    # Gerar boleto
    resultado = gerador.gerar_boleto_individual(dados)
    print(f"Boleto gerado: {resultado}")

if __name__ == "__main__":
    exemplo_basico()
```

### 2. Geração com Endereço Completo

```python
def exemplo_com_endereco():
    """Exemplo com endereço completo do cliente"""
    
    dados = {
        "codigo": "BOL002",
        "nome": "Maria Santos",
        "email": "maria@empresa.com",
        "documento": "987.654.321-00",
        "telefone": "(11) 98765-4321",
        "servico_nome": "Desenvolvimento Web",
        "servico_descricao": "Desenvolvimento de site institucional",
        "valor": 5000.00,
        "data_vencimento": "2024-02-20",
        "rua": "Rua das Flores",
        "numero": "123",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01234-567",
        "complemento": "Sala 45"
    }
    
    resultado = gerador.gerar_boleto_individual(dados)
    print(f"Boleto com endereço: {resultado}")
```

### 3. Geração com Juros e Multa

```python
def exemplo_com_juros_multa():
    """Exemplo com juros e multa personalizados"""
    
    dados = {
        "codigo": "BOL003",
        "nome": "Empresa ABC Ltda",
        "email": "contato@empresa.com",
        "documento": "11.222.333/0001-81",
        "servico_nome": "Serviço Empresarial",
        "servico_descricao": "Pacote empresarial mensal",
        "valor": 2500.00,
        "data_vencimento": "2024-02-25",
        "juros_mensal": 2.5,  # 2.5% ao mês
        "multa": "50.00"      # R$ 50,00 de multa
    }
    
    resultado = gerador.gerar_boleto_individual(dados)
    print(f"Boleto com juros e multa: {resultado}")
```

## 📊 Exemplos Avançados

### 1. Geração em Lote com Excel

```python
import pandas as pd
from datetime import datetime, timedelta

def exemplo_lote_excel():
    """Exemplo de geração em lote usando arquivo Excel"""
    
    # Criar dados de exemplo
    dados_exemplo = [
        {
            "codigo": "BOL001",
            "nome": "João Silva",
            "email": "joao@email.com",
            "documento": "123.456.789-09",
            "servico_nome": "Consultoria",
            "servico_descricao": "Consultoria mensal - Janeiro",
            "valor": 1500.00,
            "data_vencimento": (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        },
        {
            "codigo": "BOL002",
            "nome": "Maria Santos",
            "email": "maria@email.com",
            "documento": "987.654.321-00",
            "servico_nome": "Desenvolvimento",
            "servico_descricao": "Desenvolvimento de sistema",
            "valor": 3000.00,
            "data_vencimento": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        },
        {
            "codigo": "BOL003",
            "nome": "Empresa ABC Ltda",
            "email": "contato@empresa.com",
            "documento": "11.222.333/0001-81",
            "servico_nome": "Serviço Empresarial",
            "servico_descricao": "Pacote empresarial",
            "valor": 5000.00,
            "data_vencimento": (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d')
        }
    ]
    
    # Criar DataFrame
    df = pd.DataFrame(dados_exemplo)
    
    # Salvar como Excel
    df.to_excel('dados/boletos_exemplo.xlsx', index=False)
    
    # Gerar boletos em lote
    resultados = gerador.gerar_boletos_em_lote('dados/boletos_exemplo.xlsx')
    
    print(f"Boletos gerados: {len(resultados['sucessos'])}")
    print(f"Erros: {len(resultados['erros'])}")
    
    return resultados
```

### 2. Geração com Notificações Personalizadas

```python
def exemplo_notificacoes_personalizadas():
    """Exemplo com configuração de notificações personalizadas"""
    
    dados = {
        "codigo": "BOL004",
        "nome": "Carlos Oliveira",
        "email": "carlos@email.com",
        "documento": "111.222.333-44",
        "telefone": "(11) 91234-5678",
        "servico_nome": "Manutenção",
        "servico_descricao": "Manutenção preventiva mensal",
        "valor": 800.00,
        "data_vencimento": "2024-02-28",
        "notificar_email": True,
        "notificar_sms": True,
        "notificar_whatsapp": True
    }
    
    resultado = gerador.gerar_boleto_individual(dados)
    print(f"Boleto com notificações: {resultado}")
```

### 3. Geração com Diferentes Formatos de Valor

```python
def exemplo_formatos_valor():
    """Exemplo com diferentes formatos de valor monetário"""
    
    formatos_teste = [
        {"valor": 1500.00, "descricao": "Decimal"},
        {"valor": "R$ 1.500,00", "descricao": "Formato brasileiro"},
        {"valor": "1500,00", "descricao": "Com vírgula"},
        {"valor": "1.500.00", "descricao": "Com ponto"},
        {"valor": "1500", "descricao": "Inteiro"}
    ]
    
    for formato in formatos_teste:
        dados = {
            "codigo": f"BOL_{formato['descricao'].upper()}",
            "nome": "Teste Formato",
            "email": "teste@email.com",
            "documento": "123.456.789-09",
            "servico_nome": "Teste de Formato",
            "servico_descricao": f"Teste: {formato['descricao']}",
            "valor": formato['valor'],
            "data_vencimento": "2024-03-01"
        }
        
        try:
            resultado = gerador.gerar_boleto_individual(dados)
            print(f"✅ {formato['descricao']}: {resultado['amount']} centavos")
        except Exception as e:
            print(f"❌ {formato['descricao']}: {e}")
```

## 🔧 Exemplos de Configuração

### 1. Configuração Dinâmica

```python
def exemplo_configuracao_dinamica():
    """Exemplo de configuração dinâmica do sistema"""
    
    # Configuração base
    config_base = {
        "api": {
            "auth_url": "https://matls-clients.api.cora.com.br/token",
            "base_url": "https://matls-clients.api.cora.com.br/v2/invoices",
            "timeout": 30
        },
        "credentials": {
            "client_id": "seu_client_id"
        },
        "certificates": {
            "cert_path": "certificados/certificate.pem",
            "key_path": "certificados/private-key.key"
        }
    }
    
    # Configuração de ambiente
    import os
    ambiente = os.getenv('ENVIRONMENT', 'production')
    
    if ambiente == 'sandbox':
        config_base['api']['auth_url'] = "https://sandbox-matls-clients.api.cora.com.br/token"
        config_base['api']['base_url'] = "https://sandbox-matls-clients.api.cora.com.br/v2/invoices"
    
    # Salvar configuração
    with open('config.yaml', 'w') as f:
        yaml.dump(config_base, f, default_flow_style=False)
    
    print(f"Configuração salva para ambiente: {ambiente}")
```

### 2. Configuração com Validações

```python
def exemplo_configuracao_validada():
    """Exemplo de configuração com validações"""
    
    def validar_config(config):
        """Valida a configuração"""
        erros = []
        
        # Verificar URLs
        if not config.get('api', {}).get('auth_url'):
            erros.append("auth_url é obrigatório")
        
        if not config.get('api', {}).get('base_url'):
            erros.append("base_url é obrigatório")
        
        # Verificar credenciais
        if not config.get('credentials', {}).get('client_id'):
            erros.append("client_id é obrigatório")
        
        # Verificar certificados
        cert_path = config.get('certificates', {}).get('cert_path')
        key_path = config.get('certificates', {}).get('key_path')
        
        if not cert_path or not os.path.exists(cert_path):
            erros.append(f"Certificado não encontrado: {cert_path}")
        
        if not key_path or not os.path.exists(key_path):
            erros.append(f"Chave privada não encontrada: {key_path}")
        
        return erros
    
    # Carregar configuração
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Validar
    erros = validar_config(config)
    
    if erros:
        print("❌ Erros na configuração:")
        for erro in erros:
            print(f"  - {erro}")
        return False
    
    print("✅ Configuração válida!")
    return True
```

## 📝 Exemplos de Tratamento de Erros

### 1. Tratamento de Erros de Validação

```python
def exemplo_tratamento_erros():
    """Exemplo de tratamento de erros de validação"""
    
    dados_invalidos = [
        {
            "codigo": "BOL_ERRO1",
            "nome": "",  # Nome vazio
            "email": "email-invalido",  # Email inválido
            "documento": "123",  # Documento inválido
            "valor": -100,  # Valor negativo
            "data_vencimento": "2020-01-01"  # Data no passado
        }
    ]
    
    for dados in dados_invalidos:
        try:
            resultado = gerador.gerar_boleto_individual(dados)
            print(f"✅ Boleto gerado: {resultado}")
        except ValueError as e:
            print(f"❌ Erro de validação: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
```

### 2. Retry Automático

```python
import time
from requests.exceptions import RequestException

def exemplo_retry_automatico():
    """Exemplo de retry automático em caso de erro de rede"""
    
    max_tentativas = 3
    delay = 2  # segundos
    
    dados = {
        "codigo": "BOL_RETRY",
        "nome": "Teste Retry",
        "email": "teste@email.com",
        "documento": "123.456.789-09",
        "servico_nome": "Teste",
        "servico_descricao": "Teste de retry",
        "valor": 100.00,
        "data_vencimento": "2024-03-01"
    }
    
    for tentativa in range(max_tentativas):
        try:
            resultado = gerador.gerar_boleto_individual(dados)
            print(f"✅ Boleto gerado na tentativa {tentativa + 1}")
            return resultado
        except RequestException as e:
            print(f"❌ Tentativa {tentativa + 1} falhou: {e}")
            if tentativa < max_tentativas - 1:
                print(f"⏳ Aguardando {delay} segundos...")
                time.sleep(delay)
                delay *= 2  # Backoff exponencial
            else:
                print("❌ Todas as tentativas falharam")
                raise
```

## 📊 Exemplos de Relatórios

### 1. Relatório de Geração

```python
def exemplo_relatorio_geracao():
    """Exemplo de relatório de geração de boletos"""
    
    # Gerar alguns boletos
    resultados = exemplo_lote_excel()
    
    # Criar relatório
    relatorio = {
        "data_geracao": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total_boletos": len(resultados['sucessos']) + len(resultados['erros']),
        "sucessos": len(resultados['sucessos']),
        "erros": len(resultados['erros']),
        "taxa_sucesso": f"{(len(resultados['sucessos']) / (len(resultados['sucessos']) + len(resultados['erros']))) * 100:.1f}%",
        "valor_total": sum(boleto.get('amount', 0) for boleto in resultados['sucessos']),
        "detalhes_sucessos": resultados['sucessos'],
        "detalhes_erros": resultados['erros']
    }
    
    # Salvar relatório
    import json
    with open('saida/relatorio_geracao.json', 'w') as f:
        json.dump(relatorio, f, indent=2, default=str)
    
    # Exibir resumo
    print("📊 Relatório de Geração:")
    print(f"  Total: {relatorio['total_boletos']}")
    print(f"  Sucessos: {relatorio['sucessos']}")
    print(f"  Erros: {relatorio['erros']}")
    print(f"  Taxa de Sucesso: {relatorio['taxa_sucesso']}")
    print(f"  Valor Total: R$ {relatorio['valor_total'] / 100:.2f}")
    
    return relatorio
```

### 2. Relatório de Validação

```python
def exemplo_relatorio_validacao():
    """Exemplo de relatório de validação de dados"""
    
    # Dados para validar
    dados_para_validar = [
        {"nome": "João", "email": "joao@email.com", "documento": "123.456.789-09"},
        {"nome": "", "email": "email-invalido", "documento": "123"},
        {"nome": "Maria", "email": "maria@email.com", "documento": "987.654.321-00"}
    ]
    
    relatorio_validacao = {
        "data_validacao": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total_registros": len(dados_para_validar),
        "validos": 0,
        "invalidos": 0,
        "erros_por_campo": {},
        "registros_validos": [],
        "registros_invalidos": []
    }
    
    for i, dados in enumerate(dados_para_validar):
        erros_registro = []
        
        # Validar nome
        if not dados.get('nome'):
            erros_registro.append("Nome é obrigatório")
            relatorio_validacao['erros_por_campo']['nome'] = relatorio_validacao['erros_por_campo'].get('nome', 0) + 1
        
        # Validar email
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, dados.get('email', '')):
            erros_registro.append("Email inválido")
            relatorio_validacao['erros_por_campo']['email'] = relatorio_validacao['erros_por_campo'].get('email', 0) + 1
        
        # Validar documento
        doc = dados.get('documento', '').replace('.', '').replace('-', '').replace('/', '')
        if len(doc) not in [11, 14]:
            erros_registro.append("Documento deve ter 11 ou 14 dígitos")
            relatorio_validacao['erros_por_campo']['documento'] = relatorio_validacao['erros_por_campo'].get('documento', 0) + 1
        
        # Classificar registro
        if erros_registro:
            relatorio_validacao['invalidos'] += 1
            relatorio_validacao['registros_invalidos'].append({
                "indice": i,
                "dados": dados,
                "erros": erros_registro
            })
        else:
            relatorio_validacao['validos'] += 1
            relatorio_validacao['registros_validos'].append({
                "indice": i,
                "dados": dados
            })
    
    # Salvar relatório
    with open('saida/relatorio_validacao.json', 'w') as f:
        json.dump(relatorio_validacao, f, indent=2, default=str)
    
    # Exibir resumo
    print("📊 Relatório de Validação:")
    print(f"  Total: {relatorio_validacao['total_registros']}")
    print(f"  Válidos: {relatorio_validacao['validos']}")
    print(f"  Inválidos: {relatorio_validacao['invalidos']}")
    print(f"  Erros por campo: {relatorio_validacao['erros_por_campo']}")
    
    return relatorio_validacao
```

## 🚀 Exemplos de Integração

### 1. Integração com Sistema de Contabilidade

```python
def exemplo_integracao_contabilidade():
    """Exemplo de integração com sistema de contabilidade"""
    
    # Simular dados do sistema de contabilidade
    dados_contabilidade = [
        {
            "cliente_id": "CLI001",
            "cliente_nome": "João Silva",
            "cliente_email": "joao@email.com",
            "cliente_documento": "123.456.789-09",
            "fatura_id": "FAT001",
            "fatura_descricao": "Fatura mensal - Janeiro 2024",
            "fatura_valor": 1500.00,
            "fatura_vencimento": "2024-02-15",
            "centro_custo": "CONSULTORIA",
            "projeto": "PROJ001"
        }
    ]
    
    # Converter para formato do sistema de boletos
    boletos_para_gerar = []
    
    for fatura in dados_contabilidade:
        boleto = {
            "codigo": f"BOL_{fatura['fatura_id']}",
            "nome": fatura['cliente_nome'],
            "email": fatura['cliente_email'],
            "documento": fatura['cliente_documento'],
            "servico_nome": fatura['centro_custo'],
            "servico_descricao": fatura['fatura_descricao'],
            "valor": fatura['fatura_valor'],
            "data_vencimento": fatura['fatura_vencimento'],
            "metadata": {
                "cliente_id": fatura['cliente_id'],
                "fatura_id": fatura['fatura_id'],
                "projeto": fatura['projeto']
            }
        }
        boletos_para_gerar.append(boleto)
    
    # Gerar boletos
    resultados = []
    for boleto in boletos_para_gerar:
        try:
            resultado = gerador.gerar_boleto_individual(boleto)
            resultados.append({
                "status": "sucesso",
                "boleto_id": resultado.get('id'),
                "fatura_id": boleto['metadata']['fatura_id'],
                "dados": resultado
            })
        except Exception as e:
            resultados.append({
                "status": "erro",
                "fatura_id": boleto['metadata']['fatura_id'],
                "erro": str(e)
            })
    
    return resultados
```

### 2. Integração com CRM

```python
def exemplo_integracao_crm():
    """Exemplo de integração com sistema CRM"""
    
    # Simular dados do CRM
    clientes_crm = [
        {
            "id": "CRM001",
            "nome": "Maria Santos",
            "email": "maria@empresa.com",
            "telefone": "(11) 98765-4321",
            "documento": "987.654.321-00",
            "endereco": {
                "rua": "Rua das Flores",
                "numero": "123",
                "bairro": "Centro",
                "cidade": "São Paulo",
                "estado": "SP",
                "cep": "01234-567"
            },
            "segmento": "EMPRESARIAL",
            "valor_contrato": 5000.00,
            "frequencia_pagamento": "MENSAL"
        }
    ]
    
    # Gerar boletos recorrentes
    from datetime import datetime, timedelta
    
    boletos_recorrentes = []
    data_inicio = datetime.now()
    
    for mes in range(12):  # 12 meses
        data_vencimento = data_inicio + timedelta(days=30 * mes)
        
        for cliente in clientes_crm:
            boleto = {
                "codigo": f"BOL_{cliente['id']}_{data_vencimento.strftime('%Y%m')}",
                "nome": cliente['nome'],
                "email": cliente['email'],
                "documento": cliente['documento'],
                "telefone": cliente['telefone'],
                "servico_nome": f"Serviço {cliente['segmento']}",
                "servico_descricao": f"Serviço mensal - {data_vencimento.strftime('%B %Y')}",
                "valor": cliente['valor_contrato'],
                "data_vencimento": data_vencimento.strftime('%Y-%m-%d'),
                "rua": cliente['endereco']['rua'],
                "numero": cliente['endereco']['numero'],
                "bairro": cliente['endereco']['bairro'],
                "cidade": cliente['endereco']['cidade'],
                "estado": cliente['endereco']['estado'],
                "cep": cliente['endereco']['cep'],
                "metadata": {
                    "cliente_crm_id": cliente['id'],
                    "segmento": cliente['segmento'],
                    "mes_referencia": data_vencimento.strftime('%Y-%m')
                }
            }
            boletos_recorrentes.append(boleto)
    
    return boletos_recorrentes
```

---

**Última atualização**: Junho 2025
**Versão**: 2.0 