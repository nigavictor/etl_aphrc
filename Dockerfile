# Dockerfile

# Start from a minimal Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 5000

# Run the FastAPI app on container start
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]
