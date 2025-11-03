# FastAPI Lab

A RESTful API built with FastAPI for exploring and analyzing wine quality data. This lab demonstrates fundamental API development concepts including data loading, CRUD operations, filtering, and data visualization endpoints.

## Overview

This project provides a FastAPI-based interface for the Wine Quality dataset, allowing users to query wine characteristics, filter by quality ratings, and retrieve statistical insights through RESTful endpoints.

## Project Structure

```
.
├── model/              # Data models and schemas
├── src/                # Source code and business logic
├── API Landing.png     # API documentation screenshot
├── Example.png         # Example output/response
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Key dependencies include:
   - `fastapi` - Modern web framework for building APIs
   - `uvicorn` - ASGI server for running FastAPI
   - `pandas` - Data manipulation and analysis
   - `scikit-learn` (optional) - For wine dataset loading

## Running the API

1. **Start the development server:**
   ```bash
   uvicorn main:app --reload
   ```

   The `--reload` flag enables auto-reload on code changes (useful for development).

2. **Access the API:**
   - **Interactive API Documentation (Swagger UI):** http://localhost:8000/docs
   - **Alternative Documentation (ReDoc):** http://localhost:8000/redoc
   - **API Base URL:** http://localhost:8000

## 📡 API Endpoints

### Example Endpoints (Based on Wine Dataset)

#### GET `/wines`
Retrieve all wine records
```bash
curl http://localhost:8000/wines
```

#### GET `/wines/{id}`
Get a specific wine by ID
```bash
curl http://localhost:8000/wines/1
```

#### GET `/wines/quality/{rating}`
Filter wines by quality rating (e.g., rating between 1-10)
```bash
curl http://localhost:8000/wines/quality/7
```

#### POST `/wines`
Add a new wine record
```bash
curl -X POST http://localhost:8000/wines \
  -H "Content-Type: application/json" \
  -d '{
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.7,
    "citric_acid": 0.0,
    "residual_sugar": 1.9,
    "chlorides": 0.076,
    "free_sulfur_dioxide": 11,
    "total_sulfur_dioxide": 34,
    "density": 0.9978,
    "pH": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4,
    "quality": 5
  }'
```

#### GET `/stats`
Get statistical summary of the wine dataset
```bash
curl http://localhost:8000/stats
```

## Dataset Information

The Wine Quality dataset contains physicochemical properties and quality ratings for wines:

**Features:**
- `fixed_acidity` - Fixed acidity level
- `volatile_acidity` - Volatile acidity level
- `citric_acid` - Citric acid concentration
- `residual_sugar` - Residual sugar content
- `chlorides` - Chloride concentration
- `free_sulfur_dioxide` - Free sulfur dioxide
- `total_sulfur_dioxide` - Total sulfur dioxide
- `density` - Wine density
- `pH` - pH level
- `sulphates` - Sulphate concentration
- `alcohol` - Alcohol percentage
- `quality` - Quality rating (score between 0-10)

## Technologies Used

- **FastAPI** - Modern, fast web f
