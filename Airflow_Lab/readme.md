# Customer Segmentation with K-Means Clustering

This lab demonstrates how to create a machine learning workflow using Apache Airflow that automates customer segmentation using K-Means clustering and the elbow method to determine the optimal number of clusters.

## Overview

The workflow performs the following steps:
1. **Load Data**: Reads customer data from a CSV file
2. **Data Preprocessing**: Cleans and scales the data using MinMax scaling
3. **Model Building**: Trains K-Means clustering models for different values of k (1-10)
4. **Model Evaluation**: Uses the elbow method to determine the optimal number of clusters
5. **Prediction**: Applies the trained model to test data

## Project Structure
```
Airflow_Lab/
├── dags/
│   ├── data/
│   │   ├── file.csv          # Training data (200 customers)
│   │   └── test.csv          # Test data (50 customers)
│   ├── model/
│   │   ├── model.sav         # Saved K-Means model (generated)
│   │   └── scaler.pkl        # Saved MinMax scaler (generated)
│   ├── src/
│   │   ├── __init__.py
│   │   └── lab.py            # ML functions
│   └── airflow.py            # DAG definition
├── logs/                     # Airflow logs (auto-generated)
├── plugins/                  # Airflow plugins
├── config/                   # Airflow config
├── .env                      # Environment variables
└── docker-compose.yaml       # Docker Compose configuration
```

## Prerequisites

- **Docker Desktop** installed and running
- **At least 8GB RAM** allocated to Docker
- **MacOS, Linux, or Windows** (with WSL2)

## Dataset

### Customer Segmentation Data
The dataset contains customer transaction information with the following features:

- `customer_id`: Unique customer identifier
- `total_spent`: Total lifetime purchase value ($)
- `purchase_frequency`: Number of purchases made
- `average_order_value`: Average amount per order ($)
- `days_since_last_purchase`: Recency metric (days)
- `recency_score`: Engagement score (1-10)


##  Running the DAG

1. Open your browser and go to: **http://localhost:8080**
2. Login with:
   - **Username**: `airflow2`
   - **Password**: `airflow2`
3. Find the DAG named **`Airflow_Lab1`**
4. Toggle the switch to **ON** (enable the DAG)
5. Click the **▶️ Play button** (Trigger DAG)
6. Watch the workflow execute!

## 📈 Viewing Results

To see the optimal number of clusters:

1. Click on **`Airflow_Lab1`** DAG
2. Click the **Graph** tab
3. Click on **`load_model_task`** (the last task)
4. Click the **Logs** tab
5. Look for: `Optimal number of clusters: X`


## Stopping Airflow

Open a new terminal and run:
```bash
cd Airflow_Lab
docker compose down
```

To completely reset (removes all data):
```bash
docker compose down --volumes --remove-orphans
```

## Key Dependencies

The following Python packages are installed automatically via Docker:
- `pandas` - Data manipulation
- `scikit-learn` - K-Means clustering and preprocessing
- `kneed` - Elbow method implementation

## Troubleshooting

### Docker Memory Issues
If you see memory warnings, increase Docker memory:
1. Docker Desktop → Settings → Resources
2. Set Memory to **8GB**
3. Click **Apply & Restart**

### Port 8080 Already in Use
```bash
lsof -ti:8080 | xargs kill -9
```

## 📄 License

This project is part of the MLOps course curriculum.

---

**Note**: This lab uses Docker to run Airflow, so no virtual environment or local package installation is required!
