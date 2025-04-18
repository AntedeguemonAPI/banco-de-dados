FROM python:3.12.7-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia todos os arquivos do projeto
COPY . .

# Instala dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expõe a porta usada pelo app
EXPOSE 5003

# Comando correto para iniciar a aplicação Flask
CMD ["python", "app.py"]
