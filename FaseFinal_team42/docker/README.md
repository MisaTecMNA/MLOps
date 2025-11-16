# Docker Setup for FastAPI ML Service

## Overview
This directory contains the Dockerfile used to containerize the FastAPI-based machine learning inference service.  
The Docker image bundles the API, model artifact, and all required dependencies to run the model via HTTP endpoints.

## Contents
- **Dockerfile**  
  Defines the environment, installs dependencies, copies project files, and starts the FastAPI application using Uvicorn.

## Building the Docker Image

### 1. Build the Image
Run the following command **from the project root directory**:

```
docker build -t team42-mlops2025-ml-service -f docker/Dockerfile .
```

### 2. Run the Container

```
docker run -p 9000:9000 team42-mlops2025-ml-service
```

After the container starts, access the API at:

- **Swagger UI:** http://localhost:9000/docs  
- **Root Endpoint:** http://localhost:9000/

## Dockerfile Overview

### Base Image
A lightweight Python 3.10 image is used:

```
FROM python:3.10-slim
```

### What the Dockerfile Does
- Sets `/app` as the working directory  
- Installs necessary system-level dependencies  
- Installs Python requirements from `requirements.txt`  
- Copies the entire project into the container  
- Launches the FastAPI service using Uvicorn:

```
CMD ["uvicorn", "FastAPI.main:app", "--host", "0.0.0.0", "--port", "9000"]
```

## Requirements
The following files/directories must exist in the project root (since they are copied during build):

- `FastAPI/main.py` – entrypoint of the FastAPI service  
- `models/final_model_GradBoost.joblib` – trained ML model artifact  
- `requirements.txt` – Python dependency list  

## Notes
- After modifying the API code or model artifact, rebuild the Docker image.  
- The model path is resolved automatically using relative paths inside the container.  
- If the model location changes, update the path logic in `FastAPI/main.py`.

## Optional: Push Image to Docker Hub

### Tag the image:

```
docker tag team42-mlops2025-ml-service <your_dockerhub_user>/team42-mlops2025-ml-service:latest
```

### Push it:

```
docker push <your_dockerhub_user>/team42-mlops2025-ml-service:latest
```
