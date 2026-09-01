# Docker Support

This application can be containerized using Docker for easy deployment.

## Dockerfile (Backend)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ .

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Docker Compose

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: metrology_user
      POSTGRES_PASSWORD: metrology_pass
      POSTGRES_DB: metrology_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    environment:
      DATABASE_URL: postgresql://metrology_user:metrology_pass@db:5432/metrology_db
      JWT_SECRET_KEY: your_jwt_secret_key
      FLASK_ENV: production
    ports:
      - "5000:5000"
    depends_on:
      - db
    volumes:
      - ./backend/uploads:/app/uploads

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

## Running with Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```
