FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py .
COPY config.py .
COPY API/ ./API/
COPY Model/ ./Model/
COPY pk_db/ ./pk_db/
COPY Rag/ ./Rag/
EXPOSE 8084
CMD ["gunicorn", "-w", "1", "--timeout", "120", "-b", "0.0.0.0:8084", "server:app"]