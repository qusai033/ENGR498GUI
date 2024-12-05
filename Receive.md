To ensure the graphs display even when the data contains all zeros or `NaN` values, you need to preprocess the data to handle these cases and update the JavaScript and server-side logic accordingly.

---

### **Key Updates**

1. **Preprocess Data on the Server**:
   - Replace all `NaN` and `-NaN` values with `0`.
   - Ensure data arrays contain at least one valid point.

2. **Update JavaScript**:
   - Modify the chart logic to handle zero-filled data gracefully.

---

### **Server-Side Updates**
In your Flask server, ensure `NaN` values are replaced with `0` in the `/data/<device>/rulData.csv` endpoint:

```python
@app.route('/data/<device>/rulData.csv', methods=['GET'])
def get_rul_fd_soh_data(device):
    file_path = os.path.join(DATA_DIRECTORY, device, 'rulData.csv')
    
    if not os.path.exists(file_path):
        return abort(404, description="RUL data file not found.")
    
    try:
        df = pd.read_csv(file_path)
        
        # Replace NaN and negative NaN with 0
        df.fillna(0, inplace=True)
        df.replace(-float('nan'), 0, inplace=True)

        # Ensure all required columns exist
        required_columns = ['DT', 'RUL', 'PH', 'FD', 'SOH']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return abort(400, description=f"Missing columns: {', '.join(missing_columns)}")
        
        # Prepare JSON response
        data = {
            "time": df['DT'].tolist(),
            "rul": df['RUL'].tolist(),
            "ph": df['PH'].tolist(),
            "fd": df['FD'].tolist(),
            "eol": df['EOL'].tolist() if 'EOL' in df.columns else [0] * len(df),
            "bd": df['BD'].tolist() if 'BD' in df.columns else [0] * len(df),
            "soh": df['SOH'].tolist()
        }
        return jsonify(data)
    except Exception as e:
        print("Error:", e)  # Debug error
        return jsonify({"error": str(e)}), 500
```

---

### **JavaScript Updates**
In the `showGraphsForDevice` function, ensure it handles zero-filled data:

```javascript
function showGraphsForDevice(device) {
    console.log("Switching to Device:", device);

    fetch(`/data/${device}/voltageData.csv`)
        .then(response => response.json())
        .then(data => {
            // Ensure data arrays are non-empty
            if (!data.time || data.time.length === 0) {
                data.time = [0]; // Default to a single zero entry
                data.voltage = [0]; // Default voltage value
            }
            updateVoltageChart(data);
        })
        .catch(error => console.error('Error loading voltage data:', error));

    fetch(`/data/${device}/rulData.csv`)
        .then(response => response.json())
        .then(data => {
            console.log("Fetched RUL Data for Device:", device);

            // Ensure non-empty arrays and replace `-NaN` or `NaN` with `0`
            Object.keys(data).forEach(key => {
                if (Array.isArray(data[key])) {
                    data[key] = data[key].map(value => isNaN(value) ? 0 : value);
                }
            });

            // Default to zero if BD/EOL indices are missing
            const bdIndex = data.bd.findIndex(value => value !== 0) || 0;
            const eolIndex = data.eol.findIndex(value => value !== 0) || 0;

            // Update charts
            updateRulChart(data, bdIndex, eolIndex);
            updateSoHChart(data, bdIndex, eolIndex);
            updateFDChart(data, bdIndex, eolIndex);
        })
        .catch(error => console.error('Error loading RUL data:', error));
}
```

---

### **Graph Behavior with Zero Data**
Ensure charts handle zero values:

1. **Voltage Chart**:
   ```javascript
   updateVoltageChart({
       time: [0],
       voltage: [0]
   });
   ```

2. **RUL Chart**:
   ```javascript
   updateRulChart({
       time: [0],
       rul: [0],
       ph: [0],
       eol: [0],
       bd: [0]
   }, 0, 0);
   ```

3. **SoH Chart**:
   ```javascript
   updateSoHChart({
       time: [0],
       soh: [0]
   }, 0, 0);
   ```

4. **FD Chart**:
   ```javascript
   updateFDChart({
       time: [0],
       fd: [0],
       bd: [0],
       eol: [0]
   }, 0, 0);
   ```

---

### **Testing Zero-Data Handling**
- Upload a file with all `0` values or introduce `NaN` values.
- Verify that graphs still display.
- Check if vertical lines appear correctly based on `0` or default indices.

Would you like additional logic to differentiate between "valid zero data" and "missing data"?
