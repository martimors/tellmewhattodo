FROM node:22 AS build
WORKDIR /var/app
COPY . .
RUN npm run build

FROM unit:python3.12


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