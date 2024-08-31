FROM golang:1.23 AS builder

WORKDIR /app

COPY app/ ./
COPY app/go.mod app/go.sum ./

RUN go mod download

COPY scripts/ ./

RUN go build -o main .

FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y \
    bash \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/main .

# Executring pre-start sh scripts.
COPY scripts/insert_openings.sh .
RUN chmod +x insert_openings.sh
RUN ./insert_openings.sh
EXPOSE 8080

CMD ["bash", "./main"]
