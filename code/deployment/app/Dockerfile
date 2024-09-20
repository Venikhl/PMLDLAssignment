# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Streamlit app to the container
COPY ./app.py /app

# Install required Python packages
RUN pip install streamlit requests Pillow

# Expose the port Streamlit will run on
EXPOSE 8501

# Command to run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
