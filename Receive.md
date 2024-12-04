Let's refine the code to:

1. **Fix the Device Switching Issue**:
   - Ensure the correct `bd` and `eol` indices are recalculated and displayed for each device dynamically.
   - Properly refresh all charts and annotations when switching devices.

2. **Add the PH Line to the RUL Chart**:
   - Include the PH data as a second dataset in the RUL chart.

---

### Updated Code

#### Updated RUL Chart with PH Line
Include both RUL and PH lines in the same chart:

```javascript
function updateRulChart(data) {
    const ctx = document.getElementById('rulChart').getContext('2d');

    if (rulChart) rulChart.destroy();

    // Find the first indices for BD and EOL
    const bdIndex = data.bd.findIndex(value => value !== 0);
    const eolIndex = data.eol.findIndex(value => value !== 0);

    rulChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time, // X-axis labels
            datasets: [
                {
                    label: 'Remaining Useful Life (RUL)',
                    data: data.rul,
                    borderColor: 'rgb(255, 165, 0)', // Orange for RUL
                    tension: 0.1,
                    fill: false,
                    pointRadius: 0
                },
                {
                    label: 'Prognostic Health (PH)',
                    data: data.ph,
                    borderColor: 'rgb(0, 150, 136)', // Teal for PH
                    tension: 0.1,
                    fill: false,
                    pointRadius: 0
                }
            ],
            bdIndex: bdIndex !== -1 ? bdIndex : null, // Pass first BD index
            eolIndex: eolIndex !== -1 ? eolIndex : null // Pass first EOL index
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'RUL/PH [AU]' } }
            },
            plugins: {
                zoom: zoomOptions
            }
        },
        plugins: [annotationPlugin] // Add the updated annotation plugin
    });
}
```

---

#### Fixing Device Switching

Ensure all charts properly refresh and display BD/EOL annotations for the selected device:

```javascript
function showGraphsForDevice(device) {
    // Fetch and update data for all four graphs
    fetch(`/data/${device}/voltageData.csv`)
        .then(response => response.json())
        .then(data => updateVoltageChart(data));

    fetch(`/data/${device}/rulData.csv`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Data not found');
            }
            return response.json();
        })
        .then(data => {
            updateRulChart(data);  // RUL Chart with RUL & PH lines
            updateSoHChart(data);  // SoH Chart
            updateFDChart(data);   // FD Chart
        })
        .catch(error => console.error('Error loading data:', error));
}
```

---

#### Enhanced Annotation Plugin for All Charts

Ensure annotations (BD and EOL) are correctly recalculated and displayed for all charts:

```javascript
const annotationPlugin = {
    id: 'dynamicAnnotationPlugin',
    beforeDraw: (chart) => {
        const ctx = chart.ctx;
        const xScale = chart.scales.x;
        const yScale = chart.scales.y;

        // Retrieve first indices for BD and EOL from chart data
        const bdIndex = chart.data.bdIndex || null;
        const eolIndex = chart.data.eolIndex || null;

        // Draw the circle for BD (if it exists)
        if (bdIndex !== null) {
            const xPixel = xScale.getPixelForValue(chart.data.labels[bdIndex]);
            const yPixel = yScale.getPixelForValue(chart.data.datasets[0].data[bdIndex]);

            ctx.save();
            ctx.beginPath();
            ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for BD
            ctx.lineWidth = 2;
            ctx.strokeStyle = 'green';
            ctx.stroke();
            ctx.restore();
        }

        // Draw the circle for EOL (if it exists)
        if (eolIndex !== null) {
            const xPixel = xScale.getPixelForValue(chart.data.labels[eolIndex]);
            const yPixel = yScale.getPixelForValue(chart.data.datasets[0].data[eolIndex]);

            ctx.save();
            ctx.beginPath();
            ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for EOL
            ctx.lineWidth = 2;
            ctx.strokeStyle = 'red';
            ctx.stroke();
            ctx.restore();
        }
    }
};
```

---

#### Example Usage for Other Charts

The logic for adding `bdIndex` and `eolIndex` works the same for other charts (e.g., SoH and FD charts):

```javascript
function updateSoHChart(data) {
    const ctx = document.getElementById('sohChart').getContext('2d');

    if (sohChart) sohChart.destroy();

    // Find the first indices for BD and EOL
    const bdIndex = data.bd.findIndex(value => value !== 0);
    const eolIndex = data.eol.findIndex(value => value !== 0);

    sohChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [{
                label: 'State-of-Health (SoH)',
                data: data.soh,
                borderColor: 'rgb(153, 102, 255)', // Purple for SoH
                tension: 0.1,
                fill: false,
                pointRadius: 0
            }],
            bdIndex: bdIndex !== -1 ? bdIndex : null,
            eolIndex: eolIndex !== -1 ? eolIndex : null
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'SoH [%]' } }
            },
            plugins: {
                zoom: zoomOptions
            }
        },
        plugins: [annotationPlugin]
    });
}
```

---

### Summary of Changes:
1. **Dynamic Annotations**:
   - Updated plugin now only draws the **first BD and EOL points**.
2. **Multi-Line Chart for RUL**:
   - The RUL chart now includes both RUL and PH lines.
3. **Device Switching**:
   - All charts are updated correctly when switching devices, recalculating the BD and EOL points.

---

Let me know if anything else needs tweaking!
