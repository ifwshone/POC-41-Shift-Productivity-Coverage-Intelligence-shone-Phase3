FROM python:3.11-slim

WORKDIR /app

# Ensure /app is in Python's module search path
ENV PYTHONPATH=/app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend, assistant, and data-science outputs keeping the package structure
COPY backend/ ./backend/
COPY assistant/ ./assistant/
COPY data-science/outputs/ ./data-science/outputs/

EXPOSE 8000

# Run uvicorn targeting the module path
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]