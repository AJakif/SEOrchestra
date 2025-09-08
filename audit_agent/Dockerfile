FROM python:3.11-slim

WORKDIR /app

# Set Python path to include the shared module
ENV PYTHONPATH="/app:${PYTHONPATH}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]