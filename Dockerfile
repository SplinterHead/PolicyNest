# ----------------------------
# STAGE 1: Build Frontend
# ----------------------------
FROM node:26-alpine AS frontend-build
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
ARG APP_VERSION=""
ENV VITE_APP_VERSION=${APP_VERSION}
RUN npm run build


# ----------------------------
# STAGE 2: Setup Backend & Serve
# ----------------------------
FROM python:3.15-slim AS requirements-stage
WORKDIR /tmp
RUN pip install --no-cache-dir poetry poetry-plugin-export
COPY backend/pyproject.toml backend/poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.15-slim

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh .
COPY backend/ ./backend

COPY --from=frontend-build /app/frontend/dist ./frontend/dist

RUN mkdir -p backend/uploads

WORKDIR /app/backend
CMD [ "/app/docker-entrypoint.sh"]