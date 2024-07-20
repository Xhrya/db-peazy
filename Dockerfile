# Stage 1: Build React app
FROM node:14 as build

WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy React source code and build the app
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup Flask backend and serve React build
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install Flask dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app code
COPY backend/ ./backend

# Create static directory and copy React build artifacts
RUN mkdir -p backend/static
COPY --from=build /app/frontend/build/ backend/static/

# Expose port for the Flask app
EXPOSE 8080

# Set working directory to the backend directory
WORKDIR /app/backend

# Run the Flask app
CMD ["python", "main.py"]
