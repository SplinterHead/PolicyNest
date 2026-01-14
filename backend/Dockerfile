FROM python:3.14-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app

# Create uploads directory
RUN mkdir /app/uploads

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]