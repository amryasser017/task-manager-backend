FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --index-url https://pypi.org/simple/ --retries 10 -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]