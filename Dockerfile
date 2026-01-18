# -------------------------------------------------
# Base image (lightweight, stable, production-ready)
# -------------------------------------------------
FROM python:3.10-slim

# -------------------------------------------------
# Set working directory inside container
# -------------------------------------------------
WORKDIR /app

# -------------------------------------------------
# Copy dependency list first (better layer caching)
# -------------------------------------------------
COPY requirements.txt .

# -------------------------------------------------
# Install Python dependencies
# -------------------------------------------------
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------------------------
# Copy application code and model artifacts
# -------------------------------------------------
COPY app.py .
COPY models/ models/

# -------------------------------------------------
# Expose FastAPI port
# -------------------------------------------------
EXPOSE 8000

# -------------------------------------------------
# Run FastAPI using Uvicorn
# -------------------------------------------------
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
