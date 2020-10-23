FROM docker.pkg.github.com/novaweb-mobi/connexion-api-docker/novaapi:0.2.0-rc.1-postgres
ADD app .
ENV APIS user_api.yml
