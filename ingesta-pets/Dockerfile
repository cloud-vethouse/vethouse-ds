FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema para mysql si fueran necesarias
RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev pkg-config && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ingesta.py .

CMD ["python", "ingesta.py"]
