# 1. Imagem Base: Python 3.11 leve (Slim)
# Escolhemos uma versão estável e pequena (Linux Debian por baixo)
FROM python:3.11-slim

# 2. Configurações de Ambiente
# Evita que o Python crie arquivos .pyc e força o log a sair no terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Instalar dependências do sistema (necessárias pro C++ do FAISS/Numpy)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Definir pasta de trabalho dentro do container
WORKDIR /app

# 5. Copiar e Instalar dependências Python
# Copiamos SÓ o requirements primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar o código fonte do projeto
COPY src/ src/
COPY data/ data/ 
# (Crie uma pasta data vazia se não tiver, pro comando não falhar)

# 7. Comando padrão ao iniciar o container
# Vai rodar nosso motor vetorial
CMD ["python", "src/vector_engine.py"]