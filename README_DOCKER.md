# 🐳 Docker - Consulta de Boletos Cora

Este documento descreve como executar a aplicação usando Docker.

## 📋 Pré-requisitos

- Docker instalado (versão 20.10 ou superior)
- Docker Compose instalado (versão 1.29 ou superior) - opcional, mas recomendado

## 🚀 Execução Rápida

### Opção 1: Docker Compose (Recomendado)

1. **Configure os arquivos necessários:**
   - Crie/configure `config.yaml` na raiz do projeto
   - Coloque os certificados na pasta `certificados/`
   - Crie um arquivo `.env` (opcional, mas recomendado) com as variáveis de ambiente

2. **Execute com Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Acesse a aplicação:**
   - Abra o navegador em: `http://localhost:5000`

4. **Parar a aplicação:**
   ```bash
   docker-compose down
   ```

5. **Ver logs:**
   ```bash
   docker-compose logs -f
   ```

### Opção 2: Docker direto

1. **Construir a imagem:**
   ```bash
   docker build -t cora-boletos:latest .
   ```

2. **Executar o container:**
   ```bash
   docker run -d \
     --name cora-boletos-app \
     -p 5000:5000 \
     -v $(pwd)/config.yaml:/app/config.yaml:ro \
     -v $(pwd)/certificados:/app/certificados:ro \
     -v $(pwd)/.env:/app/.env:ro \
     -e PORT=5000 \
     -e SECRET_KEY=sua-chave-secreta-aqui \
     cora-boletos:latest
   ```

3. **Acessar a aplicação:**
   - Abra o navegador em: `http://localhost:5000`

4. **Parar o container:**
   ```bash
   docker stop cora-boletos-app
   docker rm cora-boletos-app
   ```

## 📁 Estrutura de Arquivos Necessários

Antes de executar, certifique-se de ter:

```
cora_boletos/
├── config.yaml          # Configuração da API Cora (obrigatório)
├── certificados/        # Certificados mTLS (obrigatório)
│   ├── certificate.pem
│   └── private-key.key
├── .env                 # Variáveis de ambiente (opcional)
└── docker-compose.yml   # Configuração Docker Compose
```

## 🔧 Configuração

### Arquivo config.yaml

O arquivo `config.yaml` deve estar configurado conforme a documentação. Exemplo mínimo:

```yaml
api:
  auth_url: https://matls-clients.api.cora.com.br/token
  base_url: https://matls-clients.api.cora.com.br/v2/invoices
credentials:
  client_id: seu_client_id
certificates:
  cert_path: certificados/certificate.pem
  key_path: certificados/private-key.key
```

**Importante**: O `config.yaml` é montado como volume, então você pode alterá-lo sem precisar fazer rebuild da imagem. Após alterar o arquivo, basta reiniciar o container:

```bash
docker-compose restart
```

### Variáveis de Ambiente

Você pode configurar via arquivo `.env` ou variáveis de ambiente do sistema:

```env
PORT=5000
HOST=0.0.0.0
DEBUG=false
SECRET_KEY=sua-chave-secreta-aqui
CONFIG_FILE=config.yaml
```

### Certificados

Os certificados devem estar na pasta `certificados/` e são montados como volume somente leitura no container.

## 🛠️ Comandos Úteis

### Docker Compose

```bash
# Iniciar em background
docker-compose up -d

# Iniciar em primeiro plano (ver logs)
docker-compose up

# Parar
docker-compose down

# Reconstruir e reiniciar
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Ver logs apenas do serviço app
docker-compose logs -f app

# Executar comando no container
docker-compose exec app bash

# Parar e remover volumes
docker-compose down -v
```

### Docker direto

```bash
# Construir imagem
docker build -t cora-boletos:latest .

# Executar
docker run -d --name cora-boletos-app -p 5000:5000 cora-boletos:latest

# Ver logs
docker logs -f cora-boletos-app

# Executar comando no container
docker exec -it cora-boletos-app bash

# Parar
docker stop cora-boletos-app

# Remover
docker rm cora-boletos-app

# Remover imagem
docker rmi cora-boletos:latest
```

## 🌐 Portas

Por padrão, a aplicação roda na porta 5000. Você pode alterar:

- No `docker-compose.yml`: modifique `"${PORT:-5000}:5000"`
- No comando Docker: use `-p 8080:5000` para mapear para a porta 8080
- Via variável de ambiente `PORT`

## 🔒 Segurança

- **Nunca** commite arquivos sensíveis (`.env`, `config.yaml`, certificados) no repositório
- Use variáveis de ambiente para informações sensíveis em produção
- Certificados devem ser montados como volumes somente leitura (`:ro`)
- Em produção, considere usar secrets do Docker ou um gerenciador de secrets

## 🔄 Atualização sem Rebuild

Os seguintes arquivos são montados como volumes e podem ser alterados **sem rebuild** da imagem:

- **`config.yaml`**: Após alterar, reinicie o container: `docker-compose restart`
- **Certificados** (pasta `certificados/`): Após renovar, reinicie o container: `docker-compose restart`
- **`.env`**: Após alterar variáveis de ambiente, reinicie o container: `docker-compose restart`

**Não é necessário rebuild** da imagem Docker para alterar esses arquivos!

## 📝 Notas

- A aplicação espera que `config.yaml` e os certificados estejam disponíveis como volumes
- O `.env` é opcional, mas recomendado para configurações locais
- A pasta `certificados/` será criada automaticamente no container se não existir
- Logs da aplicação podem ser visualizados com `docker-compose logs -f`

## 🐛 Troubleshooting

### Erro: "config.yaml not found"
- Certifique-se de que o arquivo `config.yaml` existe e está sendo montado como volume
- Verifique o caminho no `docker-compose.yml`

### Erro: "Certificate not found"
- Verifique se os certificados estão na pasta `certificados/`
- Confirme que os caminhos no `config.yaml` estão corretos
- Verifique as permissões dos arquivos

### Erro de porta já em uso
- Altere a porta no `docker-compose.yml` ou use `-p 8080:5000` no Docker
- Verifique se há outro processo usando a porta 5000: `lsof -i :5000`

### Container para imediatamente
- Verifique os logs: `docker-compose logs` ou `docker logs cora-boletos-app`
- Verifique se todas as dependências estão configuradas corretamente
