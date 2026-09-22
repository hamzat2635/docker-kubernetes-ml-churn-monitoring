# Use Python as the base image
FROM python:3.14-slim


# Create application folder inside the container
WORKDIR /app


# Copy dependency file first
COPY requirements.txt .


# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt


# Copy the application files
COPY . .


# The inference service uses port 8000
EXPOSE 8000


# Start the FastAPI service
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]