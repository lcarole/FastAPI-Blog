# Utiliser une image officielle Python (version 3.13-slim pour un résultat léger)
FROM python:3.13-slim

# Empêcher Python d'écrire des fichiers .pyc et d'utiliser le buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires (par exemple, pour psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances et installer les packages Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copier l'intégralité du projet dans le conteneur
COPY . .

# Exposer le port 8000 (celui utilisé par uvicorn)
EXPOSE 8000

# Commande pour démarrer l'application via uvicorn
CMD ["fastapi", "run"]

# Commande à lancer dans le terminal pour build et déployer l'image
# docker buildx build --platform linux/amd64,linux/arm64 -t lcarole/blogapi --push .
