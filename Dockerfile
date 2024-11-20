FROM node:22 AS build
WORKDIR /var/app
COPY . .
RUN npm run build

FROM unit:1.33.0-python3.11


WORKDIR /var/app
COPY --from=build /var/app/dist /www/static
RUN chown -R unit:unit .
COPY unit.config.json /docker-entrypoint.d/
COPY tellmewhattodo .
COPY requirements.txt requirements.txt
COPY tellmewhattodo tellmewhattodo
RUN pip install -r requirements.txt
ENV API_ROOT_PATH=/api

EXPOSE 8000