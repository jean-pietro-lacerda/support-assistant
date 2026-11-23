FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY services/ ./services/
COPY prompts/ ./prompts/
COPY data/customers.json data/history.json ./data/
COPY PROMPT_ENGINEERING_NOTES.md ./

EXPOSE 8001
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8001"]
