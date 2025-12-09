# Dockerfile — use Python 3.10 runtime so TensorFlow works reliably
FROM python:3.10-slim

# avoid interactive prompts and ensure pip is usable
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# system deps needed for some Python wheels (and for gdown)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    curl \
    git \
    ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# copy only requirements first for better caching
COPY requirements.txt .

# use pip to install dependencies (tensorflow-cpu already in requirements)
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# copy rest of the app
COPY . .

# create model folder (download logic in main.py will fill it)
RUN mkdir -p /app/model

# expose port
EXPOSE 8000

# default command (Render will use this)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
