FROM python:3.11-slim
WORKDIR /app
# Instalamos dependencias para que psycopg2 funcione bien en Linux
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ingesta.py .
CMD ["python", "ingesta.py"]
