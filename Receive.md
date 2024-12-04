Let's refine the `updateFDChart` function to incorporate the same level of robustness and consistency as discussed earlier. Here's the updated version:

### Updated `updateFDChart`

```javascript
function updateFDChart(data, bdIndex, eolIndex) {
    const ctx = document.getElementById('fdChart').getContext('2d');

    if (fdChart) fdChart.destroy();

    // Ensure vertical lines are reset before updating
    verticalLines[0].x = null;
    verticalLines[1].x = null;

    // Clean BD and EOL arrays for robustness
    const cleanBd = data.bd.map(value => Number(value)).filter(value => !isNaN(value));
    const cleanEol = data.eol.map(value => Number(value)).filter(value => !isNaN(value));

    console.log("Clean BD Array for FD:", cleanBd);
    console.log("Clean EOL Array for FD:", cleanEol);

    // Dynamically find the BD and EOL indices
    const fdBdIndex = cleanBd.findIndex(value => value !== 0);
    const fdEolIndex = cleanEol.findIndex(value => value !== 0);

    console.log("FD BD Index:", fdBdIndex, "FD EOL Index:", fdEolIndex);

    if (fdBdIndex >= 0) verticalLines[1].x = data.time[fdBdIndex]; // Update BD line
    if (fdEolIndex >= 0) verticalLines[0].x = data.time[fdEolIndex]; // Update EOL line

    console.log("Updated Vertical Lines for FD:", verticalLines);

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
                pointRadius: 0,
                pointBackgroundColor: (context) => {
                    if (context.dataIndex === fdEolIndex) return 'red';
                    if (context.dataIndex === fdBdIndex) return 'green';
                    return 'transparent'; 
                },
                pointBorderWidth: (context) => {
                    if (context.dataIndex === fdEolIndex || context.dataIndex === fdBdIndex) return 1;
                    return 1;
                }
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
        plugins: [
            {
                id: 'verticalLinePlugin',
                beforeDraw: (chart) => {
                    const ctx = chart.ctx;
                    const xScale = chart.scales.x;
                    const yScale = chart.scales.y;

                    verticalLines.forEach(line => {
                        if (!line.visible || line.x === null) return;

                        const xPixel = xScale.getPixelForValue(line.x);

                        // Draw vertical line
                        ctx.save();
                        ctx.setLineDash([5, 5]);
                        ctx.beginPath();
                        ctx.moveTo(xPixel, yScale.top);
                        ctx.lineTo(xPixel, yScale.bottom);
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = line.color;
                        ctx.stroke();

                        // Add label
                        ctx.setLineDash([]);
                        ctx.font = '12px Arial';
                        ctx.fillStyle = line.color;
                        ctx.textAlign = 'center';
                        ctx.fillText(line.label, xPixel, yScale.top - 10);
                        ctx.restore();
                    });
                }
            }
        ]
    });

    adjustCharts(); // Adjust size dynamically after creation
}
```

---

### Key Improvements

1. **Clean Data**:
   - Ensures BD and EOL arrays (`data.bd` and `data.eol`) are sanitized to remove `NaN` values and unexpected types.

2. **Dynamic Indices**:
   - Dynamically calculates `fdBdIndex` and `fdEolIndex` using cleaned data.

3. **Vertical Lines Reset**:
   - Clears `verticalLines` before updating, ensuring no residual states.

4. **Detailed Logs**:
   - Logs cleaned arrays and indices for debugging.

5. **Consistent Plugin Behavior**:
   - Ensures the `verticalLinePlugin` reflects the updated `verticalLines`.

---

### Testing Steps

1. Ensure the `data` fed to `updateFDChart` has the correct structure, including:
   - `data.fd`
   - `data.bd`
   - `data.eol`
   - `data.time`

2. Debugging:
   - Check the logs for `Clean BD Array`, `Clean EOL Array`, and `Updated Vertical Lines for FD`.
   - Verify the `verticalLines` match the expected BD and EOL values for the active device.

Let me know if any further adjustments are needed!
