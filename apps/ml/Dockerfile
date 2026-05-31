FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed for OpenCV and ML libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8001

CMD ["uvicorn", "api.analyse_image:app", "--host", "0.0.0.0", "--port", "8001"]
