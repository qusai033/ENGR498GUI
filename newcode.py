import pandas as pd

# Load your voltage decay data
data = pd.read_csv('voltage_data.csv')  # Replace 'voltage_data.csv' with your actual file name

# Compute time differences and voltage differences
data['Time Difference'] = data['Time (s)'].diff()  # Time intervals
data['Voltage Difference'] = data['Voltage (V)'].diff()  # Voltage changes

# Handle cases where the first row might have NaN after diff()
data['Time Difference'].fillna(0, inplace=True)
data['Voltage Difference'].fillna(0, inplace=True)

# Calculate cumulative voltage loss
data['Cumulative Voltage Loss'] = data['Voltage Difference'].cumsum()

# Normalize Cumulative Voltage Loss to fit the 0-1 range (Feature Data)
max_loss = data['Cumulative Voltage Loss'].max()
if max_loss > 0:
    data['Feature Data (FD)'] = data['Cumulative Voltage Loss'] / max_loss
else:
    data['Feature Data (FD)'] = 0  # If no loss, FD is 0

# Smooth Feature Data (optional)
data['Feature Data (FD)'] = data['Feature Data (FD)'].rolling(window=3, min_periods=1).mean()

# Save the necessary data for ARULE
output_file = 'arule_input.csv'
data[['Time (s)', 'Feature Data (FD)']].to_csv(output_file, index=False)

print(f"Data processed and saved to {output_file}.")

# Optional: Plot the data for verification
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

# Plot Voltage Decay
plt.subplot(2, 1, 1)
plt.plot(data['Time (s)'], data['Voltage (V)'], label='Voltage Decay', color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Voltage Decay Over Time')
plt.legend()

# Plot Feature Data (FD)
plt.subplot(2, 1, 2)
plt.plot(data['Time (s)'], data['Feature Data (FD)'], label='Feature Data (FD)', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Feature Data (FD)')
plt.title('Feature Data (FD) Over Time')
plt.legend()

plt.tight_layout()
plt.show()
