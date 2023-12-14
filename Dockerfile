# Utilisation d'une image Python officielle basée sur Debian
FROM python:3.9

# Installation des dépendances
RUN pip install Flask redis psycopg2-binary psutil prometheus_client prometheus-flask-exporter
#RUN pip install Flask redis psycopg2-binary

# Configuration de l'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copie du code source dans le conteneur
COPY ./app.py /app/app.py

# Définition du répertoire de travail
WORKDIR /app

# Commande pour exécuter l'application
CMD ["python", "./app.py"]
