# official base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python packages (Python is already in the image)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY app.py .

# Command to run when container starts
CMD ["python3", "app.py"]