import pandas as pd

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
