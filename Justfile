fmt:
  just backend/format
  just frontend/format

run:
  docker compose down
  docker compose up -d --build