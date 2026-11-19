install:
  just backend/install
  just frontend/install

fmt:
  just backend/format
  just frontend/format

stop:
  docker compose down

run: stop
  docker compose up -d --build