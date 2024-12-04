The issue might not be related to the indices themselves but how the data for the second device is being processed or retained. Let's systematically debug and resolve the problem.

---

### Potential Causes
1. **Device Switching Data Retention Issue**:
   - The data from the first device might not be fully cleared before loading the second device, causing overlapping or incorrect indices.

2. **Data Type Mismatch**:
   - The second device's data might not be in the expected numerical format during the `findIndex` operation.

3. **Incorrect Data in Arrays**:
   - The `findIndex` operation might stop prematurely due to unexpected non-zero values earlier in the array.

4. **Caching or Old State**:
   - Some old state from the first device might be interfering with the second device's data.

---

### Debugging Steps

1. **Log Entire Process for Both Devices**
   Add detailed logs to verify the data for both devices, ensuring the indices are computed correctly.

   ```javascript
   console.log("Device Selected:", device);
   console.log("BD Array (Raw):", data.bd);
   console.log("EOL Array (Raw):", data.eol);
   ```

2. **Ensure Clean Switching**
   Before fetching data for the new device, clear any cached or lingering state:
   ```javascript
   verticalLines[0].x = null; // Clear EOL
   verticalLines[1].x = null; // Clear BD
   ```

3. **Force Data Conversion**
   Convert all `data.bd` and `data.eol` values to numbers before processing:
   ```javascript
   const cleanBd = data.bd.map(value => Number(value)).filter(value => !isNaN(value));
   const cleanEol = data.eol.map(value => Number(value)).filter(value => !isNaN(value));
   ```

4. **Check for Array Boundaries**
   If the indices seem incorrect, check for limits or conditions that might prevent higher indices:
   ```javascript
   if (bdIndex < 0 || eolIndex < 0) {
       console.warn("BD or EOL not found in dataset for device:", device);
   }
   ```

---

### Updated Code for `showGraphsForDevice`

Replace the relevant portion in your `showGraphsForDevice` function:

```javascript
fetch(`/data/${device}/rulData.csv`)
    .then(response => response.json())
    .then(data => {
        console.log("Device Selected:", device);
        console.log("Fetched BD Array (Raw):", data.bd);
        console.log("Fetched EOL Array (Raw):", data.eol);
        console.log("Fetched Time Array:", data.time);

        // Clear old states
        verticalLines[0].x = null; // Clear EOL
        verticalLines[1].x = null; // Clear BD

        // Clean and convert data
        const cleanBd = data.bd.map(value => Number(value)).filter(value => !isNaN(value));
        const cleanEol = data.eol.map(value => Number(value)).filter(value => !isNaN(value));

        console.log("Clean BD Array:", cleanBd);
        console.log("Clean EOL Array:", cleanEol);

        // Find indices dynamically
        const bdIndex = cleanBd.findIndex(value => value !== 0);
        const eolIndex = cleanEol.findIndex(value => value !== 0);

        console.log("Computed BD Index:", bdIndex, "EOL Index:", eolIndex);

        // Validate indices
        if (bdIndex === -1 || eolIndex === -1) {
            console.warn("BD or EOL not found in dataset for device:", device);
            return;
        }

        // Update vertical lines based on indices
        verticalLines[1].x = data.time[bdIndex];
        verticalLines[0].x = data.time[eolIndex];

        console.log("Updated Vertical Lines:", verticalLines);

        // Update the charts
        updateRulChart(data);
    })
    .catch(error => console.error("Error loading RUL data for device:", device, error));
```

---

### Verify
1. Test this code with both devices and confirm:
   - The raw arrays (`data.bd`, `data.eol`) are fetched correctly.
   - The cleaned arrays (`cleanBd`, `cleanEol`) contain the correct values.
   - The computed indices match the expected values.

2. Pay attention to:
   - Whether the arrays are being processed correctly after device switching.
   - Any unusual behavior when fetching or processing the second device's data.

---

If the issue persists, share the exact debug logs for `data.bd`, `data.eol`, and their computed indices for further analysis.
