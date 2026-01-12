# Dockerfile para aplicação Flask de Consulta de Boletos Cora

# Usar imagem base do Python (não slim para evitar problemas com compilação)
FROM python:3.9

# Definir diretório de trabalho
WORKDIR /app

# Configurar variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Copiar arquivo de dependências
COPY requirements.txt .

# Instalar dependências Python
# Desabilitar barra de progresso para evitar problemas de threading no Docker
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para certificados (se necessário)
RUN mkdir -p certificados

# Expor porta (padrão 5000, pode ser alterada via variável de ambiente)
EXPOSE 5000

# Variáveis de ambiente padrão
ENV PORT=5000
ENV HOST=0.0.0.0
ENV DEBUG=false

# Limitar threading de bibliotecas numéricas para evitar problemas no Docker
ENV OPENBLAS_NUM_THREADS=1
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
