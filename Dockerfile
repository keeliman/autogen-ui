# Utilisez une image de base Python 3.9
FROM python:3.9-slim

# Env variables
ENV AUTOGENUI_HOST=0.0.0.0
ENV AUTOGENUI_PORT=8081
ENV OPENAI_API_KEY=xxxxx
# Définissez le répertoire de travail dans le conteneur
WORKDIR /app



# Copiez les fichiers locaux dans le conteneur
COPY . .

# Installez les dépendances Python
RUN pip install -e .

# Installez les dépendances nécessaires pour node
RUN apt-get update && apt-get install -y nodejs npm

# Installez les dépendances pour le frontend
RUN npm install

# Exposez le port 8081 pour le serveur UI
EXPOSE 8081

# Commande pour démarrer le serveur UI
CMD ["autogenui", "--port", "8081"]