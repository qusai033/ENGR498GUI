If the indices for the vertical lines (`bdIndex` and `eolIndex`) are being calculated incorrectly but the correct `x` values are set in the `verticalLines`, it suggests that the issue is with how the `verticalLinePlugin` is interpreting and rendering the lines. Let's debug and fix this.

### Problem Analysis
1. **Indices Misalignment**: The indices (`bdIndex` and `eolIndex`) are being calculated incorrectly as 11 and 61.
2. **Correct `x` Values**: The `verticalLines` are being updated with the correct `x` values (128 and 255).
3. **Lines Not Rendering**: Despite the correct `x` values, the lines are not showing.

---

### Solution: Debugging and Fixing the Vertical Lines
1. **Ensure `x` Values Are Correct**:
   - Log the `verticalLines` right before the plugin executes.
   - Confirm that the `x` values for BD and EOL are properly assigned.

2. **Refactor `verticalLinePlugin`**:
   - Ensure the plugin correctly translates `x` values to pixel positions.
   - Add fallback mechanisms in case of missing `x` values.

3. **Check Chart Context (`chart.scales`)**:
   - Verify that `xScale` and `yScale` are properly initialized when the plugin runs.

Here’s the updated `verticalLinePlugin`:

---

### Updated `verticalLinePlugin`

```javascript
const verticalLinePlugin = {
    id: 'verticalLinePlugin',
    beforeDraw: (chart) => {
        const ctx = chart.ctx;
        const xScale = chart.scales.x;
        const yScale = chart.scales.y;

        if (!xScale || !yScale) {
            console.warn("Scales not initialized. Cannot draw vertical lines.");
            return;
        }

        verticalLines.forEach(line => {
            if (!line.visible || line.x === null) {
                console.log("Skipping line:", line);
                return; // Skip if not visible or `x` is null
            }

            const xPixel = xScale.getPixelForValue(line.x);

            if (!xPixel) {
                console.warn("Invalid xPixel for line:", line);
                return; // Skip invalid pixel calculations
            }

            // Draw vertical line
            ctx.save();
            ctx.setLineDash([5, 5]); // Dashed line
            ctx.beginPath();
            ctx.moveTo(xPixel, yScale.top); // Top of the chart
            ctx.lineTo(xPixel, yScale.bottom); // Bottom of the chart
            ctx.lineWidth = 2;
            ctx.strokeStyle = line.color;
            ctx.stroke();
            ctx.restore();

            // Add label
            ctx.setLineDash([]); // Reset dash for label
            ctx.font = '12px Arial';
            ctx.fillStyle = line.color;
            ctx.textAlign = 'center';
            ctx.fillText(line.label, xPixel, yScale.top - 10); // Label above line
        });
    }
};
```

---

### Fix for FD Indices (`updateFDChart`)

Here’s the corrected `updateFDChart` function to ensure `verticalLines` updates and the plugin draws the lines correctly:

```javascript
function updateFDChart(data, bdIndex, eolIndex) {
    const ctx = document.getElementById('fdChart').getContext('2d');

    if (fdChart) fdChart.destroy();

    // Ensure vertical lines are updated with correct `x` values
    if (eolIndex >= 0) verticalLines[0].x = data.time[eolIndex];
    if (bdIndex >= 0) verticalLines[1].x = data.time[bdIndex];

    console.log("Updated Vertical Lines for FD Chart:", verticalLines);

    fdChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [{
                label: 'Feature Data (FD)',
                data: data.fd,
                borderColor: 'rgb(255, 51, 135)',
                tension: 0.1,
                fill: false,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'FD [AU]' } }
            },
            plugins: {
                zoom: zoomOptions
            }
        },
        plugins: [verticalLinePlugin]
    });

    adjustCharts(); // Adjust size dynamically after creation
}
```

---

### Debugging Steps
1. **Log `verticalLines`**:
   - Ensure they have the correct `x` values before drawing.

   ```javascript
   console.log("Vertical Lines:", verticalLines);
   ```

2. **Verify Plugin Execution**:
   - Confirm the plugin runs for the correct chart and `xScale`/`yScale` are valid.

   ```javascript
   console.log("xScale Min:", xScale.min, "xScale Max:", xScale.max);
   ```

3. **Check BD/EOL Indices**:
   - Confirm the `bdIndex` and `eolIndex` are calculated correctly from the data.

   ```javascript
   console.log("FD BD Index:", bdIndex, "FD EOL Index:", eolIndex);
   ```

---

### Expected Behavior
1. Correct vertical lines appear for each device's data.
2. Lines update correctly when switching devices.
3. The chart plugin properly scales and aligns lines with the data.

If issues persist, let me know what values are logged, and I’ll help further refine the implementation!
