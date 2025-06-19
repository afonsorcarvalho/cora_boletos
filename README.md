# Gerador de Boletos Cora

Sistema para geração automatizada de boletos utilizando a API da Cora.

## Estrutura do Projeto

```
cora_boletos/
├── docs/               # Documentação detalhada
├── examples/           # Arquivos de exemplo
│   └── exemplo_clientes.xlsx
├── libs/              # Biblioteca principal
│   ├── __init__.py
│   ├── auth.py        # Autenticação com a API
│   └── gerador.py     # Geração de boletos
├── scripts/           # Scripts executáveis
│   └── gerar_boletos.py
└── tests/             # Testes unitários
    ├── __init__.py
    ├── conftest.py
    ├── test_auth.py
    └── test_gerador.py
```

## Requisitos

- Python 3.8+
- Certificado digital da Cora
- Arquivo .env com as credenciais

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração

1. Copie o arquivo `.env.example` para `.env`
2. Configure as variáveis de ambiente no `.env`:
   ```
   CORA_CLIENT_ID=seu_client_id
   CORA_CERT_PATH=caminho/para/certificado.pem
   CORA_KEY_PATH=caminho/para/chave.key
   ```

## Uso

1. Prepare um arquivo Excel seguindo o modelo em `examples/exemplo_clientes.xlsx`
2. Execute o script de geração:
   ```bash
   python scripts/gerar_boletos.py examples/exemplo_clientes.xlsx
   ```

## Testes

Execute os testes com:
```bash
python -m pytest tests/ -v
```

## Funcionalidades

- Geração de boletos em lote
- Suporte a CPF e CNPJ
- Configuração de juros e multa por cliente
- Notificações por email e SMS
- Validação automática de dados
- Tratamento de erros robusto

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request 