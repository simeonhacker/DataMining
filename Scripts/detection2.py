import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from scipy.stats import zscore

# Load data from SQLite
def load_data(db_path, table_name):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# Preprocess: Convert timestamps, scale numerical data
def preprocess_data(df):
    df["TimeStamp"] = pd.to_datetime(df["TimeStamp"])  # Convert to datetime
    df.set_index("TimeStamp", inplace=True)  # Set as time index
    
    # Select numerical columns
    num_cols = ["ActualPos", "ActualForce", "LaserPwr"]
    
    for col in num_cols:
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

    # Handle missing or invalid data
    df.dropna(subset=num_cols, inplace=True)
    
    # Standardize data (mean 0, std 1)
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])

    return df, num_cols

# Z-Score Method (Quick Outlier Detection)
def detect_zscore_anomalies(df, num_cols, threshold=3):
    df["zscore"] = df[num_cols].apply(zscore).abs().max(axis=1)
    return df[df["zscore"] > threshold]

# Isolation Forest for Multivariate Anomaly Detection
def detect_isolation_forest_anomalies(df, num_cols, contamination=0.01):
    model = IsolationForest(contamination=contamination, random_state=42)
    df["anomaly"] = model.fit_predict(df[num_cols])
    return df[df["anomaly"] == -1]  # Only anomalies

# Visualization
def plot_anomalies(df, anomalies, feature):
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df[feature], label=feature, color="blue", alpha=0.6)
    plt.scatter(anomalies.index, anomalies[feature], color="red", label="Anomalies", marker="x")
    plt.legend()
    plt.show()

# Main Execution
def main():
    db_path = '/Users/simeon/Documents/Studium/Semester 6/DataMining /anlage1.db'  # Update with actual DB path
    table_name = "rohdaten"

    df = load_data(db_path, table_name)
    df, num_cols = preprocess_data(df)

    # Run anomaly detection methods
    zscore_anomalies = detect_zscore_anomalies(df, num_cols)
    isolation_anomalies = detect_isolation_forest_anomalies(df, num_cols)

    print("Z-Score Anomalies Found:", len(zscore_anomalies))
    print("Isolation Forest Anomalies Found:", len(isolation_anomalies))

    # Plot anomalies in 'actualForce' (you can change to other features)
    plot_anomalies(df, isolation_anomalies, "ActualPos")

if __name__ == "__main__":
    main()
