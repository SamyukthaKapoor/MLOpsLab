
# Stage 1: Build stage
FROM python:3.13 AS builder
WORKDIR /app

# Copy requirements first for better caching
COPY src/requirements.txt /app/
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.13-slim AS runtime
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy the application code
COPY src/main.py /app/

# Expose port 8080
EXPOSE 8080

# Run the FastAPI application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]