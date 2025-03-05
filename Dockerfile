FROM python:3.13-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les requirements et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source
COPY . .

# Créer les répertoires de données
RUN mkdir -p /app/data/input /app/data/output

# Définir le point d'entrée
ENTRYPOINT ["python", "-m", "drug_mentions_pipeline.main"]