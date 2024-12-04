If the arrays show the correct values (`128` and `255`), but the `findIndex` method is returning the wrong indices (`11` and `61`), the issue could be due to unexpected data formatting or type mismatches. Let’s address the problem systematically:

---

### Root Cause
1. **Data Type Mismatch**:
   - The values in `data.bd` and `data.eol` might not be true numbers but strings.
   - `findIndex` could fail to match a condition like `value !== 0` if the data isn't properly converted to numbers.

2. **Whitespace or Extra Characters**:
   - Hidden characters (e.g., whitespace or newline) might affect the comparison.

---

### Fix: Force Numerical Comparison
Ensure all values in `data.bd` and `data.eol` are treated as numbers during the `findIndex` operation. Update the logic as follows:

```javascript
const bdIndex = data.bd.findIndex(value => Number(value) !== 0); // Force numerical comparison
const eolIndex = data.eol.findIndex(value => Number(value) !== 0);

console.log("BD Array:", data.bd);
console.log("EOL Array:", data.eol);
console.log("Time Array:", data.time);
console.log("BD Index:", bdIndex, "EOL Index:", eolIndex);
```

---

### Debugging Data Values
Add logs to confirm the exact values and their types in `data.bd` and `data.eol`:
```javascript
data.bd.forEach((value, index) => console.log(`BD[${index}]:`, value, "Type:", typeof value));
data.eol.forEach((value, index) => console.log(`EOL[${index}]:`, value, "Type:", typeof value));
```

---

### Fix: Filter Out Non-Numeric Values
If the arrays contain unexpected non-numeric values, filter them before `findIndex`:
```javascript
const cleanBd = data.bd.map(value => Number(value)).filter(value => !isNaN(value));
const cleanEol = data.eol.map(value => Number(value)).filter(value => !isNaN(value));

const bdIndex = cleanBd.findIndex(value => value !== 0);
const eolIndex = cleanEol.findIndex(value => value !== 0);

console.log("Clean BD Array:", cleanBd);
console.log("Clean EOL Array:", cleanEol);
console.log("BD Index:", bdIndex, "EOL Index:", eolIndex);
```

---

### Ensure Proper Device Switching
When switching devices, reset any lingering states or old data:
```javascript
verticalLines[0].x = null;
verticalLines[1].x = null;
```

---

### Full Debugging Code
Replace the relevant section in your `showGraphsForDevice` function with the following:

```javascript
fetch(`/data/${device}/rulData.csv`)
    .then(response => response.json())
    .then(data => {
        console.log("Fetched Data for Device:", device);
        
        // Debugging raw data
        console.log("Raw BD Array:", data.bd);
        console.log("Raw EOL Array:", data.eol);
        console.log("Raw Time Array:", data.time);
        
        // Convert and clean arrays
        const cleanBd = data.bd.map(value => Number(value)).filter(value => !isNaN(value));
        const cleanEol = data.eol.map(value => Number(value)).filter(value => !isNaN(value));
        console.log("Clean BD Array:", cleanBd);
        console.log("Clean EOL Array:", cleanEol);

        // Find indices
        const bdIndex = cleanBd.findIndex(value => value !== 0);
        const eolIndex = cleanEol.findIndex(value => value !== 0);

        console.log("BD Index:", bdIndex, "EOL Index:", eolIndex);

        if (bdIndex === -1 || eolIndex === -1) {
            console.warn("BD or EOL not found in the current dataset.");
            return;
        }

        // Update vertical lines
        verticalLines[1].x = data.time[bdIndex];
        verticalLines[0].x = data.time[eolIndex];

        // Update charts
        updateRulChart(data, bdIndex, eolIndex);
    })
    .catch(error => console.error("Error loading RUL data:", error));
```

---

### Next Steps
1. Test this implementation.
2. Check the logs to confirm:
   - The raw data arrays (`data.bd`, `data.eol`).
   - The cleaned numeric arrays (`cleanBd`, `cleanEol`).
   - Correct indices for BD and EOL.

If the issue persists, share the logs of `data.bd` and `data.eol` along with the incorrectly computed indices for further debugging.
