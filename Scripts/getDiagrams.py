import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Load data from SQLite
def load_data(db_path, table_name):
    print(db_path)
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# Plot scatter of actualForce against unique commands
def plot_force_vs_command(df):
        
      
    
    # Find unique commands where force exceeded thresholds
    unique_commands = df["Befehl"].unique()
    command_map = {cmd: idx for idx, cmd in enumerate(unique_commands)}

    # Map commands to x-axis positions
    df["CommandIndex"] = df["Befehl"].map(command_map)
    
    # Create scatter plot
    plt.figure(figsize=(12, 6))
    plt.scatter(df["CommandIndex"], df["ActualForce"], alpha=0.5, color="blue", s=10)
    
    # Improve readability
    plt.xticks(ticks=range(len(unique_commands)), labels=unique_commands, rotation=90, ha="right")
    plt.xlabel("Command")
    plt.ylabel("Actual Force")
    plt.title("Actual Force vs. Command")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Show plot
    plt.show()

def plot_laserPWR_vs_command(df):

    # Find unique commands where force exceeded thresholds
    unique_commands = df["Befehl"].unique()
    command_map = {cmd: idx for idx, cmd in enumerate(unique_commands)}

    # Map commands to x-axis positions
    df["CommandIndex"] = df["Befehl"].map(command_map)
    
    # Create scatter plot
    plt.figure(figsize=(30, 6))
    plt.scatter(df["CommandIndex"], df["LaserPwr"], alpha=0.5, color="blue", s=10)
    
    # Improve readability
    plt.xticks(ticks=range(len(unique_commands)), labels=unique_commands, rotation=90, ha="right")
    plt.xlabel("Command")
    plt.ylabel("Laser Power")
    plt.title("Laser Power vs. Command")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Show plot
    plt.show()

def plot_ActualPos_vs_command(df):

    # Find unique commands where force exceeded thresholds
    unique_commands = df["Befehl"].unique()
    command_map = {cmd: idx for idx, cmd in enumerate(unique_commands)}

    # Map commands to x-axis positions
    df["CommandIndex"] = df["Befehl"].map(command_map)
    
    # Create scatter plot
    plt.figure(figsize=(30, 6))
    plt.scatter(df["CommandIndex"], df["ActualPos"], alpha=0.5, color="blue", s=10)
    
    # Improve readability
    plt.xticks(ticks=range(len(unique_commands)), labels=unique_commands, rotation=90, ha="right")
    plt.xlabel("Command")
    plt.ylabel("Actual Position")
    plt.title("Actual Position vs. Command")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Show plot
    plt.show()

# Comparing seam number vs captured data:
def plot_ActualPos_vs_seam(df):
    # Find unique commands where force exceeded thresholds
    unique_seams = df["Nahtnummer"].unique()
    seam_map = {seam: idx for idx, seam in enumerate(unique_seams)}

    # Map commands to x-axis positions
    df["SeamIndex"] = df["Nahtnummer"].map(seam_map)
    
    # Create scatter plot
    plt.figure(figsize=(30, 6))
    plt.scatter(df["SeamIndex"], df["ActualPos"], alpha=0.5, color="blue", s=10)
    
    # Improve readability
    plt.xticks(ticks=range(len(unique_seams)), labels=unique_seams, rotation=90, ha="right")
    plt.xlabel("Seam")
    plt.ylabel("Actual Position")
    plt.title("Actual Position vs. Seam")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Show plot
    plt.show()


# Main Execution
def main():
    db_path = '/Users/simeon/Documents/Studium/Semester 6/DataMining/anlage1.db'  # Update with actual DB path
    table_name = "rohdaten_AP_bereinigt_nur_norm"  # Update with actual table name
		
    df = load_data(db_path, table_name)

    if "ActualForce" not in df.columns or "Befehl" not in df.columns:
        print("Error: Columns 'ActualForce' or 'Befehl' not found in database.")
        return

    plot_ActualPos_vs_seam(df)

if __name__ == "__main__":
    main()
