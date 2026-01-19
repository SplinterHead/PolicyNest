# ----------------------------
# STAGE 1: Build Frontend
# ----------------------------
FROM node:22-alpine AS frontend-build
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build


# ----------------------------
# STAGE 2: Setup Backend & Serve
# ----------------------------
FROM python:3.14-slim

WORKDIR /app

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh .
COPY backend/ ./backend

COPY --from=frontend-build /app/frontend/dist ./frontend/dist

RUN mkdir -p backend/uploads

WORKDIR /app/backend
CMD [ "/app/docker-entrypoint.sh"]