Let's address both issues:

1. **Too Many Circles**: 
   - The issue of multiple circles is likely caused by the plugin using every `bd` and `eol` value instead of just the **first occurrence**. We will restrict the annotation to only the first non-zero `bd` and `eol` index.

2. **Missing BD/EOL on Switching Devices**:
   - The issue arises because the `bd` and `eol` indices are not being recalculated properly for each dataset when switching devices. This can be resolved by ensuring that the logic to calculate `bd` and `eol` indices runs dynamically for the selected device.

---

### Updated Code

#### Annotation Plugin (Fixing Too Many Circles)

Update the plugin to only display the **first `bd` and `eol` indices**:

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

#### Reusable Chart Creation

Update the chart creation logic to calculate the **first `bd` and `eol` indices** dynamically for each dataset:

```javascript
function createChart(ctx, data, label, borderColor) {
    // Find the first indices for BD and EOL
    const bdIndex = data.bd.findIndex(value => value !== 0);
    const eolIndex = data.eol.findIndex(value => value !== 0);

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time, // X-axis labels
            datasets: [{
                label: label,
                data: data[label.toLowerCase()], // Y-axis data
                borderColor: borderColor,
                tension: 0.1,
                fill: false,
                pointRadius: 0
            }],
            bdIndex: bdIndex !== -1 ? bdIndex : null, // Pass first BD index
            eolIndex: eolIndex !== -1 ? eolIndex : null // Pass first EOL index
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: `${label} [AU]` } }
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

#### Chart Update Functions

Ensure each chart recalculates its `bd` and `eol` indices when switching devices:

```javascript
function updateChart(data, chartRef, ctxId, label, color) {
    const ctx = document.getElementById(ctxId).getContext('2d');

    if (chartRef) chartRef.destroy();

    return createChart(ctx, data, label, color);
}

function updateRulChart(data) {
    rulChart = updateChart(data, rulChart, 'rulChart', 'RUL', 'rgb(255, 165, 0)');
}

function updateSoHChart(data) {
    sohChart = updateChart(data, sohChart, 'sohChart', 'SoH', 'rgb(153, 102, 255)');
}

function updateFDChart(data) {
    fdChart = updateChart(data, fdChart, 'fdChart', 'FD', 'rgb(255, 51, 135)');
}
```

---

#### Switching Devices

When switching devices, make sure to recalculate indices and update all graphs:

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
            updateRulChart(data);  // RUL Chart
            updateSoHChart(data);  // SoH Chart
            updateFDChart(data);   // FD Chart
        })
        .catch(error => console.error('Error loading data:', error));
}
```

---

### How It Solves the Issues:
1. **Only First BD/EOL**:
   - The plugin now limits the annotations to the **first non-zero `bd` and `eol` values**.

2. **Proper BD/EOL on Switch**:
   - Each chart dynamically recalculates and uses the correct indices for the dataset of the selected device.

---

Let me know if there are additional refinements you'd like!
