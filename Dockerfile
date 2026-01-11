FROM python:3.12

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose ports for both services
EXPOSE 8000 7860

# Default command (can be overridden in docker-compose)
CMD ["python", "main_api.py"]
