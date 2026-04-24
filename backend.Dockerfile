# Use official Python image
FROM python:3.11

# Set working directory inside container
WORKDIR /app

# Copy backend code
COPY backend/ .

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "app.py"]
