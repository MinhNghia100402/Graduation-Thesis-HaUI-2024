FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y bash
WORKDIR /app/
COPY . /app/
RUN pip install -r requirements.txt
# RUN bash scripts/start.sh
