FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Copy the entire build context into /app
COPY . /app/

# Install dependencies 
RUN pip install --no-cache-dir -r backend/requirements.txt

EXPOSE 8000

# Run the app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]