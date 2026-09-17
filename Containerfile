ARG CONTAINER_REGISTRY
FROM ${CONTAINER_REGISTRY}/library/python-base:3.12-slim

WORKDIR /app

COPY server.py /app/server.py

RUN useradd -m -u 1001 demo
USER demo

ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["python3", "/app/server.py"]
