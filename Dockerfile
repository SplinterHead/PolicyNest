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

COPY backend/ ./backend

COPY --from=frontend-build /app/frontend/dist ./frontend/dist

RUN mkdir -p backend/uploads

WORKDIR /app/backend
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]