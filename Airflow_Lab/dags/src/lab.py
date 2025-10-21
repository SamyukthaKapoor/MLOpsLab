import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
import pickle
import os
import base64

def load_data():
    """
    Loads data from a CSV file, serializes it, and returns the serialized data.
    Returns:
        str: Base64-encoded serialized data (JSON-safe).
    """
    print("Loading data from file.csv")
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv"))
    print(f"Loaded {len(df)} rows from file.csv")
    serialized_data = pickle.dumps(df)
    return base64.b64encode(serialized_data).decode("ascii")

def data_preprocessing(data_b64: str):
    """
    Deserializes base64-encoded pickled data, performs preprocessing,
    and returns base64-encoded pickled clustered data AND the scaler.
    """
    print("Preprocessing data...")
    data_bytes = base64.b64decode(data_b64)
    df = pickle.loads(data_bytes)

    df = df.dropna()
    print(f"After dropping NAs: {len(df)} rows")
    
    # Select only the numeric columns for clustering (excluding customer_id)
    clustering_data = df[["total_spent", "purchase_frequency", "average_order_value", 
                          "days_since_last_purchase", "recency_score"]]

    min_max_scaler = MinMaxScaler()
    clustering_data_minmax = min_max_scaler.fit_transform(clustering_data)
    print(f"Data scaled successfully. Shape: {clustering_data_minmax.shape}")

    # Return both the scaled data AND the scaler
    result = {
        'data': clustering_data_minmax,
        'scaler': min_max_scaler
    }
    
    clustering_serialized_data = pickle.dumps(result)
    return base64.b64encode(clustering_serialized_data).decode("ascii")


def build_save_model(data_b64: str, filename: str):
    """
    Builds a KMeans model on the preprocessed data and saves it along with the scaler.
    Returns the SSE list (JSON-serializable).
    """
    print("Building and saving model...")
    data_bytes = base64.b64decode(data_b64)
    result = pickle.loads(data_bytes)
    
    df = result['data']
    scaler = result['scaler']

    kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300, "random_state": 42}
    sse = []
    
    # Test k from 1 to 10
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(df)
        sse.append(kmeans.inertia_)
        print(f"k={k}, SSE={kmeans.inertia_:.2f}")

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(output_dir, filename)
    with open(model_path, "wb") as f:
        pickle.dump(kmeans, f)
    print(f"Model saved to {model_path}")
    
    # Save scaler separately
    scaler_path = os.path.join(output_dir, "scaler.pkl")
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)
    print(f"Scaler saved to {scaler_path}")

    return sse


def load_model_elbow(filename: str, sse: list):
    """
    Loads the saved model and scaler, uses the elbow method to report k.
    Returns the optimal number of clusters.
    """
    print("Loading model and determining optimal clusters...")
    
    # Load the saved model
    model_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    loaded_model = pickle.load(open(model_path, "rb"))
    print(f"Model loaded from {model_path}")
    
    # Load the saved scaler
    scaler_path = os.path.join(os.path.dirname(__file__), "../model", "scaler.pkl")
    scaler = pickle.load(open(scaler_path, "rb"))
    print(f"Scaler loaded from {scaler_path}")

    # Use elbow method to find optimal k
    kl = KneeLocator(range(1, len(sse) + 1), sse, curve="convex", direction="decreasing")
    optimal_k = kl.elbow if kl.elbow else 4
    print(f" Optimal number of clusters: {optimal_k}")

    # Load test data
    test_path = os.path.join(os.path.dirname(__file__), "../data/test.csv")
    df_test = pd.read_csv(test_path)
    print(f"Loaded {len(df_test)} rows from test.csv")
    
    df_test = df_test.dropna()
    
    # Select the same columns as training data (excluding customer_id)
    test_data = df_test[["total_spent", "purchase_frequency", "average_order_value", 
                         "days_since_last_purchase", "recency_score"]]
    
    # Scale the test data using the SAME scaler from training
    test_data_scaled = scaler.transform(test_data)
    print(f"Test data scaled successfully. Shape: {test_data_scaled.shape}")
    
    # Predict clusters for test data
    predictions = loaded_model.predict(test_data_scaled)
    
    print(f"Test data predictions (first 10): {predictions[:10]}")
    
    # Count how many in each cluster
    unique, counts = pd.Series(predictions).value_counts().sort_index().index, pd.Series(predictions).value_counts().sort_index().values
    print(f"Cluster distribution:")
    for cluster, count in zip(unique, counts):
        print(f"  Cluster {cluster}: {count} customers")
    
    return int(optimal_k)