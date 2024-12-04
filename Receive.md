If the indices being read from the second file are incorrect, the issue likely lies in how the data is being parsed or interpreted. Here’s a systematic approach to debug and fix the problem:

---

### 1. **Verify the Data Format**
Check that the `bd` and `eol` columns in the second file are formatted correctly. For instance:
- Ensure the values are numerical and not strings.
- Confirm there are no extra spaces or special characters in the columns.

You can log the raw data to see if there’s a parsing issue:
```javascript
fetch(`/data/${device}/rulData.csv`)
    .then(response => response.json())
    .then(data => {
        console.log("Fetched Data:", data); // Log raw data for inspection
        const bdIndex = data.bd.findIndex(value => value !== 0);
        const eolIndex = data.eol.findIndex(value => value !== 0);
        console.log("BD Index:", bdIndex, "EOL Index:", eolIndex); // Log indices
    })
    .catch(error => console.error('Error loading data:', error));
```

---

### 2. **Check the Logic for Identifying Indices**
Ensure the logic for identifying `bd` and `eol` indices is consistent across datasets:
```javascript
const bdIndex = data.bd.findIndex(value => value !== 0);
const eolIndex = data.eol.findIndex(value => value !== 0);
```

If `data.bd` or `data.eol` has multiple non-zero values, this will only return the first occurrence. If you expect multiple values, adjust the logic to account for this.

For example, to get all non-zero indices:
```javascript
const bdIndices = data.bd.reduce((indices, value, index) => {
    if (value !== 0) indices.push(index);
    return indices;
}, []);

const eolIndices = data.eol.reduce((indices, value, index) => {
    if (value !== 0) indices.push(index);
    return indices;
}, []);

console.log("BD Indices:", bdIndices, "EOL Indices:", eolIndices);
```

---

### 3. **Match Indices to `time`**
After finding the indices, ensure they correctly map to the `time` array:
```javascript
if (bdIndex >= 0 && bdIndex < data.time.length) {
    console.log("BD Time:", data.time[bdIndex]);
}

if (eolIndex >= 0 && eolIndex < data.time.length) {
    console.log("EOL Time:", data.time[eolIndex]);
}
```

If the `time` array is not aligned with `bd` and `eol`, it could cause incorrect mapping. Ensure all arrays (`time`, `bd`, `eol`) are the same length.

---

### 4. **Manually Validate the CSV File**
Manually open the CSV file and verify:
- The values in the `bd` and `eol` columns.
- Corresponding `time` values for the expected indices.

---

### 5. **Debugging and Correcting the Logic**
If the logic for identifying `bd` and `eol` is incorrect, you can refine it. For example:
- Check for the largest non-zero value instead of the first:
```javascript
const bdIndex = data.bd.lastIndexOf(Math.max(...data.bd.filter(value => value !== 0)));
const eolIndex = data.eol.lastIndexOf(Math.max(...data.eol.filter(value => value !== 0)));
```

---

### 6. **Handle Specific Cases**
If the second file is formatted differently or contains edge cases, handle them explicitly:
```javascript
fetch(`/data/${device}/rulData.csv`)
    .then(response => response.json())
    .then(data => {
        console.log("Fetched Data:", data);

        let bdIndex = null, eolIndex = null;

        if (Array.isArray(data.bd) && Array.isArray(data.eol)) {
            bdIndex = data.bd.findIndex(value => value !== 0);
            eolIndex = data.eol.findIndex(value => value !== 0);
        }

        if (bdIndex === -1 || eolIndex === -1) {
            console.warn("BD or EOL index not found in data");
        } else {
            console.log("BD Index:", bdIndex, "EOL Index:", eolIndex);
        }

        // Pass indices to chart update functions
        updateRulChart(data, bdIndex, eolIndex);
        updateSoHChart(data, bdIndex, eolIndex);
        updateFDChart(data, bdIndex, eolIndex);
    })
    .catch(error => console.error('Error loading data:', error));
```

---

### 7. **Add Fallback for Missing Data**
If indices cannot be found, fallback gracefully:
```javascript
const bdIndex = data.bd.findIndex(value => value !== 0);
const eolIndex = data.eol.findIndex(value => value !== 0);

if (bdIndex === -1 || eolIndex === -1) {
    console.warn(`Device ${device} is missing valid BD or EOL values.`);
    return; // Skip further processing for this dataset
}
```

---

### Updated `showGraphsForDevice`
Here’s the refined function:
```javascript
function showGraphsForDevice(device) {
    fetch(`/data/${device}/voltageData.csv`)
        .then(response => response.json())
        .then(data => updateVoltageChart(data))
        .catch(error => console.error('Error loading voltage data:', error));

    fetch(`/data/${device}/rulData.csv`)
        .then(response => response.json())
        .then(data => {
            console.log("Fetched RUL Data:", data);

            const bdIndex = data.bd ? data.bd.findIndex(value => value !== 0) : -1;
            const eolIndex = data.eol ? data.eol.findIndex(value => value !== 0) : -1;

            console.log("BD Index:", bdIndex, "EOL Index:", eolIndex);

            if (bdIndex === -1 || eolIndex === -1) {
                console.warn("Missing valid BD or EOL values.");
            }

            updateRulChart(data, bdIndex, eolIndex);
            updateSoHChart(data, bdIndex, eolIndex);
            updateFDChart(data, bdIndex, eolIndex);
        })
        .catch(error => console.error('Error loading RUL data:', error));
}
```

---

### Testing
1. Ensure the CSV files for all devices are correctly formatted.
2. Add logging to validate the parsed data and indices.
3. Verify that the correct indices are identified for each file.

Let me know how this works!
