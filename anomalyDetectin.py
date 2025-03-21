import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Step 1: Load your data from SQLite DB
def load_data_from_db(db_path, table_name):
    # Connect to SQLite DB
    conn = sqlite3.connect(db_path)
    
    # Read the data into a pandas dataframe
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    
    # Close the database connection
    conn.close()
    
    return df

# Step 2: Preprocess the data (Standardizing the features)
def preprocess_data(df):
    # For anomaly detection, we often need to scale the data
    # We'll focus on numerical columns only for simplicity
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    
    # Scale the numeric columns to have zero mean and unit variance
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[numeric_columns])
    
    return df_scaled

# Step 3: Detect anomalies using Isolation Forest
def detect_anomalies(df_scaled):
    # Initialize the Isolation Forest model
    model = IsolationForest(contamination=0.001)  # 0.1% of data will be treated as anomalies
    
    # Fit the model on the scaled data
    model.fit(df_scaled)
    
    # Predict anomalies (-1 for anomaly, 1 for normal)
    anomalies = model.predict(df_scaled)
    
    return anomalies

# Step 4: Main function to run the entire process
def main():
    # Path to your SQLite DB and table name
    db_path = '/Users/simeon/Documents/Studium/Semester 6/DataMining/anlage1.db'  # Replace with your SQLite DB path
    table_name = 'rohdaten'  # Replace with your table name
    
    # Load data from the DB
    df = load_data_from_db(db_path, table_name)
    
    # Preprocess the data (scaling)
    df_scaled = preprocess_data(df)
    
    # Detect anomalies
    anomalies = detect_anomalies(df_scaled)
    
    # Add anomaly column to the original dataframe
    df['anomaly'] = anomalies
    
    # Display the anomalies (rows marked as -1)
    print("Anomalies detected:")
    print(df[df['anomaly'] == -1])

if __name__ == "__main__":
    main()
