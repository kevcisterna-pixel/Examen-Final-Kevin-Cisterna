FROM python:3.12-slim

# Directorio de trabajo
WORKDIR /app

# Copiar requerimientos e instalar dependencias
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app/ /app

# Exponer el puerto de Flask
EXPOSE 5000

# Ejecutar la aplicación
CMD ["python", "app.py"]
