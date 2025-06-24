# Step 1: Use official Python base image
FROM python:3.11-slim

# Step 2: Set work directory
WORKDIR /app

# Step 3: Copy dependency files and install
COPY requirements.txt .

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends gcc && \
	pip install --no-cache-dir -r requirements.txt && \
	apt-get purge -y --auto-remove gcc && \
	rm -rf /var/lib/apt/lists/*

# Step 4: Copy all project files
COPY . .

# Step 5: Expose port and define command
EXPOSE 8003

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
