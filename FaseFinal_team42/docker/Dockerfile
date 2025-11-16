# Imagen base ligera con Python 3.10
FROM python:3.10-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema si hiciera falta compilar algo pesado
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo requirements primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto donde correrá FastAPI
EXPOSE 9000

# Comando para levantar la app
# FastAPI/main.py  →  módulo FastAPI.main, objeto app
CMD ["uvicorn", "FastAPI.main:app", "--host", "0.0.0.0", "--port", "9000"]
