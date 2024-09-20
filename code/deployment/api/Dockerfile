# Use the base Python image
FROM python:3.9-slim

# Install dependencies
RUN pip install fastapi tensorflow Pillow python-multipart uvicorn

# Set the working directory
WORKDIR /app

# Copy the application
COPY ./app.py /app
COPY ./models /app/models

# Expose port
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
