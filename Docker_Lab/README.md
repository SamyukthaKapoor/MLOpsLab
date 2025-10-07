# Lab 2 - Docker FastAPI Application

## Overview
This lab demonstrates building and running a FastAPI application using Docker containers. The application is a simple Coffee Shops API that performs CRUD operations.

## Application Details
This is a RESTful API for managing Boston coffee shops with the following endpoints:

- `GET /coffee-shops` - Get all coffee shops
- `POST /coffee-shops` - Add a new coffee shop
- `GET /coffee-shops/{id}` - Get a specific coffee shop
- `PUT /coffee-shops/{id}` - Update a coffee shop
- `DELETE /coffee-shops/{id}` - Delete a coffee shop

## Prerequisites
- Docker installed on your machine
- Basic understanding of Docker and FastAPI

## How to Run

### 1. Build the Docker Image
```bash
docker build -t coffee-shop-api .

2. Run the Container
bashdocker run -d -p 8080:8080 coffee-shop-api
3. Access the API

API Base URL: http://localhost:8080
Interactive API Docs: http://localhost:8080/docs
