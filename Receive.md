Here's the Python code for generating Feature Data (FD) from the voltage decay file and adding plot statements to visualize the results:

### Updated Code with Plotting

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load voltage decay data
data = pd.read_csv('voltage_decay.csv')  # Replace with actual file path

# Assume columns are "Time" and "Voltage"
data['Delta T'] = data['Time'].diff().fillna(0)

# Calculate Feature Data (FD) using a basic model
baseline_voltage = data['Voltage'].iloc[0]  # Initial voltage as baseline
data['FD'] = (baseline_voltage - data['Voltage']) / baseline_voltage  # Example FD calculation

# Calculate statistics for NDEF
fdz = data['FD'].mean()
fdc = data['FD'].iloc[0]  # Initial FD as FDC

# Output results
print(f"FDZ (Mean FD): {fdz:.2f}")
print(f"FDC (Initial FD): {fdc:.2f}")

# Save feature data for ARULE
data.to_csv('feature_data.csv', index=False)

# Plotting
plt.figure(figsize=(12, 6))

# Plot voltage decay
plt.subplot(2, 1, 1)
plt.plot(data['Time'], data['Voltage'], label='Voltage Decay', color='blue')
plt.xlabel('Time')
plt.ylabel('Voltage (V)')
plt.title('Voltage Decay Over Time')
plt.grid(True)
plt.legend()

# Plot Feature Data (FD)
plt.subplot(2, 1, 2)
plt.plot(data['Time'], data['FD'], label='Feature Data (FD)', color='orange')
plt.axhline(y=fdz, color='green', linestyle='--', label=f'FDZ (Mean): {fdz:.2f}')
plt.axhline(y=fdc, color='red', linestyle='--', label=f'FDC (Initial): {fdc:.2f}')
plt.xlabel('Time')
plt.ylabel('Feature Data (FD)')
plt.title('Feature Data (FD) Over Time')
plt.grid(True)
plt.legend()

# Show the plots
plt.tight_layout()
plt.show()
```

### Explanation of the Code
1. **Voltage Decay Calculation**:
   - Calculates `Delta T` using differences in consecutive time steps.
   - Generates `FD` as a normalized feature based on voltage decay.

2. **Feature Data Statistics**:
   - Computes `FDZ` (mean FD) and `FDC` (initial FD value).

3. **Plotting**:
   - The first subplot shows the **Voltage Decay** over time.
   - The second subplot shows the **Feature Data (FD)** with horizontal lines indicating `FDZ` and `FDC`.

4. **Output**:
   - Saves the processed data with `Delta T` and `FD` into `feature_data.csv`.
   - Displays plots for visualizing the data and ensuring correctness.

Let me know if you need further refinements!
