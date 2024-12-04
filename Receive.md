This discrepancy suggests that the issue lies in the parsing or indexing logic after switching devices. Specifically, the `findIndex` method may be operating on incorrect or misaligned data arrays. Here’s how you can debug and resolve the problem:

---

### Step 1: Validate the Raw Data
Before `findIndex` runs, ensure that the raw data for `bd`, `eol`, and `time` are correctly parsed for **Device 2**.

Add these logs right after fetching the data:
```javascript
fetch(`/data/${device}/rulData.csv`)
    .then(response => response.json())
    .then(data => {
        console.log("Fetched RUL Data for Device:", device, data); // Log raw data

        const bdIndex = data.bd.findIndex(value => value !== 0);
        const eolIndex = data.eol.findIndex(value => value !== 0);

        console.log("BD Array:", data.bd); // Log full array
        console.log("EOL Array:", data.eol); // Log full array
        console.log("Time Array:", data.time); // Log time array

        console.log("BD Index:", bdIndex, "EOL Index:", eolIndex); // Log computed indices
    })
    .catch(error => console.error('Error loading RUL data:', error));
```

Check the console for:
1. Whether the `data.bd`, `data.eol`, and `data.time` arrays have the expected lengths.
2. Whether the correct non-zero values exist at the expected indices.

---

### Step 2: Verify Array Alignment
Ensure that all arrays (`data.bd`, `data.eol`, `data.time`) are correctly aligned:
- The lengths of `bd`, `eol`, and `time` should match.
- Misalignment could occur if one array is truncated or padded.

You can enforce alignment by filtering `bd` and `eol` with their corresponding `time` values:
```javascript
if (data.bd.length !== data.time.length || data.eol.length !== data.time.length) {
    console.warn("Misaligned data arrays:", {
        bd: data.bd.length,
        eol: data.eol.length,
        time: data.time.length
    });
    return; // Abort processing for this device
}
```

---

### Step 3: Fix the Indexing Logic
Sometimes, `findIndex` may behave unexpectedly if:
- There are subtle data issues (e.g., whitespace, unexpected types).
- There are multiple non-zero values, and you only need the **first significant value**.

Here’s how to ensure robust index detection:
```javascript
const bdIndex = data.bd.findIndex(value => Number(value) !== 0); // Explicitly ensure numerical comparison
const eolIndex = data.eol.findIndex(value => Number(value) !== 0);

console.log("BD Index:", bdIndex, "EOL Index:", eolIndex);

if (bdIndex === -1 || eolIndex === -1) {
    console.warn("BD or EOL not found for Device:", device);
    return; // Exit if indices are not found
}
```

---

### Step 4: Check for Persistent State Issues
Switching devices might not fully reset the state of your charts. For example:
- Residual data from the previous device may interfere with the new device's data.
- `bdIndex` and `eolIndex` might incorrectly carry over values.

Ensure that all relevant states are reset when switching devices:
```javascript
function showGraphsForDevice(device) {
    console.log("Switching to Device:", device);

    // Reset global variables or states
    verticalLines[0].x = null; // Reset BD line
    verticalLines[1].x = null; // Reset EOL line

    fetch(`/data/${device}/rulData.csv`)
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Data:", data);

            // Ensure BD and EOL are recalculated for the new device
            const bdIndex = data.bd.findIndex(value => value !== 0);
            const eolIndex = data.eol.findIndex(value => value !== 0);

            if (bdIndex !== -1) verticalLines[1].x = data.time[bdIndex]; // Update BD line
            if (eolIndex !== -1) verticalLines[0].x = data.time[eolIndex]; // Update EOL line

            console.log("BD Index:", bdIndex, "EOL Index:", eolIndex);
            updateRulChart(data, bdIndex, eolIndex);
        })
        .catch(error => console.error('Error loading RUL data:', error));
}
```

---

### Step 5: Cross-Verify with Hardcoded Indices
If you suspect `findIndex` is still not returning the correct results, hardcode the expected indices (e.g., `128` and `255`) for testing:
```javascript
const bdIndex = 128; // Replace with known correct index
const eolIndex = 255; // Replace with known correct index
console.log("Hardcoded BD Index:", bdIndex, "Hardcoded EOL Index:", eolIndex);
```

Compare the results of `findIndex` with the hardcoded indices to identify discrepancies.

---

### Final Debug Function
Here’s the full `showGraphsForDevice` with all fixes:
```javascript
function showGraphsForDevice(device) {
    console.log("Switching to Device:", device);

    // Reset state
    verticalLines[0].x = null;
    verticalLines[1].x = null;

    fetch(`/data/${device}/rulData.csv`)
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Data:", data);

            // Validate and align arrays
            if (data.bd.length !== data.time.length || data.eol.length !== data.time.length) {
                console.warn("Misaligned arrays for Device:", device);
                return;
            }

            // Detect BD and EOL
            const bdIndex = data.bd.findIndex(value => Number(value) !== 0);
            const eolIndex = data.eol.findIndex(value => Number(value) !== 0);

            if (bdIndex === -1 || eolIndex === -1) {
                console.warn("BD or EOL not found for Device:", device);
                return;
            }

            // Update vertical lines
            verticalLines[1].x = data.time[bdIndex]; // BD line
            verticalLines[0].x = data.time[eolIndex]; // EOL line

            console.log("BD Index:", bdIndex, "EOL Index:", eolIndex);

            // Update charts
            updateRulChart(data, bdIndex, eolIndex);
        })
        .catch(error => console.error('Error loading data for Device:", device', error));
}
```

---

### Testing Steps
1. Use the debug logs to verify:
   - `data.bd` and `data.eol` arrays.
   - `bdIndex` and `eolIndex` values.
   - `data.time` alignment.
2. Cross-check with the expected values for `bd` and `eol` in the CSV files.
3. Ensure proper resetting of state between devices.

Let me know how this works!
