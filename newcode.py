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


1	0.083740831
1.1	0.083740831
1.2	0.083740831
1.3	0.083740831
1.4	0.083740831
1.5	0.083129584
1.6	0.084352078
1.7	0.083129584
1.8	0.083740831
1.9	0.084352078
2	0.092298289
2.1	0.094132029
2.2	0.095354523
2.3	0.096577017
2.4	0.089242054
2.5	0.08801956
2.6	0.08801956
2.7	0.091687042
2.8	0.091687042
2.9	0.091687042
3	0.101589242
3.1	0.101466993
3.2	0.101466993
3.3	0.101466993
3.4	0.101466993
3.5	0.10207824
3.6	0.101711491
3.7	0.101589242
3.8	0.101466993
3.9	0.101344743
4	0.111858191
4.1	0.111246944
4.2	0.112469438
4.3	0.111858191
4.4	0.111246944
4.5	0.112836186
4.6	0.112836186
4.7	0.112897311
4.8	0.112775061
4.9	0.112836186
5	0.12408313
5.1	0.124694377
5.2	0.123471883
5.3	0.124694377
5.4	0.123728606
5.5	0.123753056
5.6	0.123728606
5.7	0.124938875
5.8	0.124938875
5.9	0.125061125
6	0.135574572
6.1	0.135696822
6.2	0.135696822
6.3	0.135696822
6.4	0.135696822
6.5	0.137334963
6.6	0.137469438
6.7	0.137408313
6.8	0.137347188
6.9	0.137408313
7	0.149388753
7.1	0.149144254
7.2	0.14792176
7.3	0.149144254
7.4	0.14792176
7.5	0.149877751
7.6	0.149144254
7.7	0.149144254
7.8	0.149144254
7.9	0.149144254
8	0.164914425
8.1	0.161369193
8.2	0.162591687
8.3	0.161369193
8.4	0.161369193
8.5	0.163325183
8.7	0.161369193
8.8	0.160757946
8.9	0.161369193
9	0.184596577
9.1	0.185819071
9.2	0.187041565
9.3	0.187041565
9.4	0.185819071
9.5	0.188264059
9.6	0.187041565
9.7	0.188264059
9.8	0.188264059
9.9	0.189486553
10	0.202322738
10.1	0.204156479
10.2	0.204156479
10.3	0.205378973
10.4	0.205378973
10.5	0.212713936
10.6	0.213381418
10.7	0.212713936
10.8	0.212836186
10.9	0.213080685
11	0.227640587
11.1	0.227383863
11.2	0.228606357
11.3	0.227383863
11.4	0.22799511
11.5	0.228606357
11.6	0.22799511
11.7	0.22799511
11.8	0.227628362
11.9	0.227628362
12	0.251344743
12.1	0.253056235
12.2	0.253056235
12.3	0.256723716
12.4	0.25794621
12.5	0.259168704
12.6	0.259168704
12.7	0.259168704
12.8	0.261613692
12.9	0.26405868
13	0.282273839
13.1	0.277506112
13.2	0.281173594
13.3	0.283618582
13.4	0.283618582
13.5	0.284841076
13.6	0.284841076
13.7	0.28606357
13.8	0.287286064
13.9	0.289731051
14	0.319070905
14.1	0.320293399
14.2	0.320293399
14.3	0.321515892
14.4	0.32396088
14.5	0.325183374
14.6	0.325183374
14.7	0.326405868
14.8	0.326405868
14.9	0.33007335
15	0.363691932
15.1	0.366748166
15.2	0.369193154
15.3	0.369193154
15.4	0.369193154
15.5	0.373227384
15.6	0.37408313
15.7	0.375305623
15.8	0.375305623
15.9	0.375305623
16	0.418948655
16.1	0.419315403
16.2	0.419315403
16.3	0.420537897
16.4	0.420537897
16.5	0.424205379
16.6	0.425427873
16.7	0.426650367
16.8	0.429095355
16.9	0.430317848
17	0.489364303
17.1	0.491442543
17.2	0.491442543
17.3	0.503667482
17.4	0.503667482
17.5	0.504889976
17.6	0.503667482
17.7	0.501222494
17.8	0.503667482
17.9	0.506112469
18	0.582885086
18.1	0.583129584
18.2	0.584352078
18.3	0.585574572
18.4	0.585574572
18.5	0.586797066
18.6	0.58801956
18.7	0.58801956
18.8	0.589242054
18.9	0.589242054
19	0.713447433
19.1	0.717603912
19.2	0.7200489
19.3	0.723716381
19.4	0.724938875
19.5	0.727383863
19.6	0.728606357
19.7	0.729828851
19.8	0.732273839
19.9	0.73594132
20	0.911491443
20.1	0.823716381
20.2	0.862860635
20.3	0.832273839
20.4	0.889242054
20.5	0.917823960
20.6	0.88801956
20.7	0.88801956
20.8	0.903667482
20.9	0.913667482
21	0.855867971
