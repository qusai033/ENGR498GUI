import pandas as pd
import matplotlib.pyplot as plt

# Load your voltage decay data
data = pd.read_csv('voltage_data.csv')  # Replace with your file
data['Time Difference'] = data['Time (s)'].diff()  # Compute time difference
data['Voltage Difference'] = data['Voltage (V)'].diff()  # Compute voltage difference

# Calculate cumulative voltage difference
data['Cumulative Voltage Loss'] = data['Voltage Difference'].cumsum()

# Normalize FD to fit a 0-1 range
max_loss = data['Cumulative Voltage Loss'].max()
data['Feature Data (FD)'] = data['Cumulative Voltage Loss'] / max_loss

# Save processed data for ARULE
data[['Time (s)', 'Voltage (V)', 'Feature Data (FD)']].to_csv('arule_input.csv', index=False)

print("Feature Data (FD) calculated and saved to arule_input.csv.")

# Plot Voltage vs. Time and Time vs. FD
plt.figure(figsize=(12, 10))

# Subplot 1: Voltage vs. Time
plt.subplot(2, 1, 1)  # 2 rows, 1 column, plot 1
plt.plot(data['Time (s)'], data['Voltage (V)'], label='Voltage (V)', color='orange', linewidth=2)
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Voltage (V)', fontsize=12)
plt.title('Voltage vs. Time', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10)

# Subplot 2: Feature Data (FD) vs. Time
plt.subplot(2, 1, 2)  # 2 rows, 1 column, plot 2
plt.plot(data['Time (s)'], data['Feature Data (FD)'], label='Feature Data (FD)', color='blue', linewidth=2)
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Feature Data (FD)', fontsize=12)
plt.title('Time vs. Feature Data (FD)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10)

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()
