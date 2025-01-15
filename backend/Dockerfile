# Use a base image, e.g., Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port your backend runs on (e.g., 8000)
EXPOSE 8000

# Run the application
CMD ["python", "src/app.py"]
