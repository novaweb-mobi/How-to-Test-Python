FROM docker.pkg.github.com/novaweb-mobi/connexion-api-docker/novaapi:0.2.0-rc.1-postgres
ENV APIS user_api.yml
ENV DB_URL 172.18.0.2
ADD app .
