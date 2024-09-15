FROM golang:1.23-alpine AS build

WORKDIR /app

COPY app/ .

RUN go mod download
RUN go build -o fiber-app main.go

FROM ubuntu:20.04

# RUN apk --no-cache add ca-certificates
COPY --from=build /app/fiber-app .

RUN apt-get update && \
    apt-get install -y postgresql-client

EXPOSE 8080

# Runing scripts for preparing db.
COPY app/.env .env
COPY scripts/ /app/scripts/

# Make the shell scripts executable
RUN chmod +x /app/scripts/*.sh

# Execute the shell scripts
# Scripts run will be there.

CMD ["./fiber-app"]
