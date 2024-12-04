import pandas as pd
import matplotlib.pyplot as plt

# Load your voltage decay data
file_path = "voltage_decay.csv"  # Replace with your file name
data = pd.read_csv(file_path)

# Ensure the required columns are present
if "Time" not in data.columns or "Voltage" not in data.columns:
    raise ValueError("The input file must contain 'Time' and 'Voltage' columns.")

# Sort data by Time if not already sorted
data = data.sort_values(by="Time").reset_index(drop=True)

# Calculate delta t (time differences)
data['Delta T'] = data['Time'].diff()  # Difference between consecutive times

# Fill missing or negative values in Delta T
data['Delta T'].fillna(0.0, inplace=True)
data['Delta T'] = data['Delta T'].clip(lower=0)  # Ensure no negative delta T

# Add a Sample column for indexing (1-based indexing)
data['Sample'] = data.index + 1

# Calculate cumulative change in voltage to inspect for non-monotonic behavior
data['Cumulative Voltage Change'] = data['Voltage'].diff().cumsum().fillna(0)

# Check if Delta T is monotonically increasing
delta_t_values = data['Delta T'].to_numpy()
increasing = all(delta_t_values[1:] >= delta_t_values[:-1])  # Compare consecutive values

if increasing:
    print("Delta T values are increasing as expected.")
else:
    print("Delta T values are NOT strictly increasing. Consider reviewing the data.")

# Plot Sample vs Delta T to visualize the curve
plt.figure(figsize=(12, 8))
plt.plot(data['Sample'], data['Delta T'], marker='o', label='Delta T Curve')
plt.title('Sample vs Delta T')
plt.xlabel('Sample')
plt.ylabel('Delta T')
plt.grid()
plt.legend()
plt.show()

# Save the result to a new CSV file
output_file = "sample_vs_delta_t.csv"
data[['Sample', 'Delta T']].to_csv(output_file, index=False)

print(f"Sample vs Delta T data saved to: {output_file}")

# Generate the Node Definition dynamically based on data insights
node_definition = f"""
% NODE_VOLTAGE_DECAY: Generated Node for Voltage Decay
%** Feature Data: FD = FDZ*(dP/P)^FDNV + DC + NOISE
FDNM = 1.0; % F: Noise margin - % of FDZ: 0.0 to 25.0
FDC = {data['Delta T'].max():.2f}; % F: Nominal DC Feature Data (FD)value: positive
FDZ = {data['Delta T'].mean():.2f}; % F: Nominal AC Feature Data (FD)value: positive
FDCPTS = 0; % I: # data points to average for FDZ: up to 25
FDPTS = 5; % I: # data points to average for FD: up to 5
FDNV = 1.0; % F: n value     
%** Prognostic Information
FFPFAIL = 70.0; % F: Failure margin - percent above nominal
PITTFF = 500.0; % F: Default RUL = TTFF value
PIFFSMOD = 2; % I: 1=Convex, 2=Linear, 3=Concave, 
%                         4=convex-concave, 5=concave-convex, 6=convex-concave 
%** File Dependent Parameters
INFILE = 'sample_vs_delta_t'; % S: In filename, _OUT appended for output
INTYPE = '.csv';     % S: .txt or csv Input file type
OUTTYPE = '.csv';    % also .txt Output file type 
%**
ENDDEF = -9;     % end of node definition
"""

# Save the Node Definition to a File
node_file = "node_definition.txt"
with open(node_file, "w") as f:
    f.write(node_definition)

print(f"Node definition saved to: {node_file}")
