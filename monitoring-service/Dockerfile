# Use Python as the base image
FROM python:3.14-slim


# Create application folder inside container
WORKDIR /app


# Copy dependency file
COPY requirements.txt .


# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt


# Copy monitoring service files
COPY . .


# Monitoring service uses port 8001
EXPOSE 8001


# Start FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]