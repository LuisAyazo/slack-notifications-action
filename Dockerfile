## Imagen del contenedor que ejecuta tu código
#FROM alpine:3.10

## Copias tu archivo de código de tu repositorio de acción a la ruta `/`del contenedor
#COPY entrypoint.sh /entrypoint.sh

## Archivo del código a ejecutar cuando comienza el contedor del docker (`entrypoint.sh`)
#ENTRYPOINT ["/entrypoint.sh"]




FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app requests

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/script.py"]
