import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def train_and_save():
    # 1. Load dataset
    df = pd.read_csv("music_listeners.csv")
    
    # 2. Select specific features
    features = ['listening_hours_per_week', 'songs_per_day', 'skip_rate', 'playlist_count']
    X = df[features]
    
    # 3. Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 4. Fit K-Means with k=3
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    
    # 5. Map clusters dynamically based on listening_hours_per_week center
    # Find original feature center values for interpretation
    centers = scaler.inverse_transform(kmeans.cluster_centers_)
    hours_index = features.index('listening_hours_per_week')
    
    # Sort cluster IDs by listening hours ascending
    sorted_cluster_ids = np.argsort(centers[:, hours_index])
    
    cluster_mapping = {
        sorted_cluster_ids[0]: "Casual Listener",
        sorted_cluster_ids[1]: "Music Explorer",
        sorted_cluster_ids[2]: "Heavy Listener"
    }
    
    # Save artifacts
    joblib.dump(kmeans, "model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    joblib.dump(cluster_mapping, "cluster_mapping.pkl")
    
    print("Model training complete.")
    print("Cluster Interpretations (Centers):")
    for orig_id, label in cluster_mapping.items():
        print(f"Cluster {orig_id} -> Label: {label} | Centers: {centers[orig_id]}")

if __name__ == "__main__":
    train_and_save()