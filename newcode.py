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




% XFD4_BPS04 : Ripple voltage, half pi 
%**Feature Data: FD = FDZ*(dP/P)^FDNV + DC + NOISE  
FDNM = 2.0;    % F: Noise margin - % of FDZ: 0.0 to 25.0
FDC = 0.1;     % F: Nominal DC Value of FD
FDZ = 0.85;     % F: Nominal AC Value of FD
FDCPTS = 0;    % I: # data points to average for FDZ: up to 25
FDPTS = 5 ;     % I: # data points to average for FDZ: up to 25
FFPFAIL = 65.0; % F: Failure margin - percent above nominal
FDNV = 2.75;      % F: n or lambda (life = P0) value        
%**Prognostic Information
PITTFF = 40.0;   % F: Default RUL = TTFF value
PIFFSMOD = 5;       % I: model 1=Convex, 2=Linear, 3=Concave, 
%                         4=convex-concave, 5=concave-convex, 6=convex-concave  
%**File Dependent Parameters
INFILE = 'BPS03'; % S: In filename, _OUT appended for output
INTYPE = '.txt';     % S: also .csv Input file type
OUTTYPE   = '.csv' ;    % also .txt Output file type 
%**
ENDDEF    = -9;     % end of node definition


100,101
103,103
105,105
108,104
110,103
112,103.5
115,104
117,104.5
120,105
122,105.5
125,106
128,105
130,104
132,106
135,108
137,109
140,110
142,112
145,115
148,119
150,124
152,122
155,120
157,120.5
160,121
162,120
165,118
168,121
170,122
175,125
177,130
180,135
183,134
185,133
188,135
190,138
192,139
195,140
198,142
200,145
203,144.5
205,144
207,152
210,160
213,159
215,160
218,165
220,168
223,171
225,175
228,181
230,187
232,195
235,204
238,214
240,225
243,223
245,220
247,228
250,236
252,248
255,260
258,295
260,335
263,323
265,310
267,312
270,315
273,314
275,313
278,310
280,315
