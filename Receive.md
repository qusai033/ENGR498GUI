If the vertical lines still don’t appear despite the correct `x` values being assigned to `verticalLines`, it’s likely that there’s an issue in how the plugin processes the `x` values or how the chart handles the plugin lifecycle.

Let’s systematically refine the logic:

---

### Updated Debugging and Fix

#### 1. **Ensure `verticalLines` Is Correctly Updated**
- Before rendering, log the `verticalLines` to verify it has the right `x` values for each device.
  
  ```javascript
  console.log("Final Vertical Lines Before Rendering:", verticalLines);
  ```

#### 2. **Validate `xScale.getPixelForValue()`**
- If the `x` values from `verticalLines` are correct, the issue might be with how `getPixelForValue()` calculates the pixel position. Log its output:

  ```javascript
  const xPixel = xScale.getPixelForValue(line.x);
  console.log("Pixel Position for Line:", xPixel, "for x:", line.x);
  ```

---

### Final Plugin Update
This version includes enhanced validation and fallback handling to ensure that even if one part fails, it logs useful information:

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

            if (isNaN(xPixel) || xPixel === undefined) {
                console.warn("Invalid xPixel for line:", line, "xScale domain:", xScale.min, "-", xScale.max);
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

### Revised `updateFDChart` with Vertical Line Debugging

This ensures `verticalLines` is updated correctly and logs any potential issues:

```javascript
function updateFDChart(data, bdIndex, eolIndex) {
    const ctx = document.getElementById('fdChart').getContext('2d');

    if (fdChart) fdChart.destroy();

    // Ensure vertical lines are updated with correct `x` values
    verticalLines[0].x = eolIndex >= 0 ? data.time[eolIndex] : null;
    verticalLines[1].x = bdIndex >= 0 ? data.time[bdIndex] : null;

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

### Additional Debugging Steps
1. **Inspect `eolIndex` and `bdIndex`:**
   Log the indices directly before assigning `verticalLines`:
   ```javascript
   console.log("EOL Index:", eolIndex, "BD Index:", bdIndex);
   ```

2. **Check `xScale` Min and Max:**
   If the `x` values fall outside the `xScale` range, they won’t render.
   ```javascript
   console.log("xScale Min:", xScale.min, "xScale Max:", xScale.max);
   ```

3. **Device Switching:**
   Ensure `verticalLines` resets properly when switching devices.

   ```javascript
   console.log("Device Switched. Resetting Vertical Lines:", verticalLines);
   ```

---

### Key Expectations:
- The plugin will now validate all critical operations (`x` values, pixel calculations, scale domains).
- Proper logging will highlight whether the issue is with data, scaling, or rendering.
- Vertical lines should appear consistently for all devices with valid data.

If issues persist, please share the logged outputs for `verticalLines`, `eolIndex`, `bdIndex`, and `xScale`. This will help refine the logic further.
