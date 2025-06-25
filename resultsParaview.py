import pandas as pd
import matplotlib.pyplot as plt

# === USER INPUT ===
csv_file = "pressure_aorta.csv"  # Replace with your CSV filename

# === Load CSV data ===
df = pd.read_csv(csv_file)

# Extract the pressure column name (assuming it's the first column)
pressure_col = df.columns[0]

# Generate a time column based on the row index (starting from 1)
df['Time'] = range(1, len(df) + 1)

# === Plot ===
plt.figure(figsize=(8, 4))
plt.plot(df['Time'], df[pressure_col], label='Pressure')
plt.xlabel("Time [s]")
plt.ylabel("Pressure [Pa]")
plt.title("Pressure vs Time")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
