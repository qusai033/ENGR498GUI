The issue likely lies in how `bd` and `eol` data are processed and how the annotations are applied to graphs other than `rulChart`. Here’s how you can resolve the problem:

### Issues to Address:
1. **Global Indices for `bd` and `eol`**:
   - The indices for `bd` and `eol` are being calculated for each graph but might not be shared correctly across all graphs.

2. **Incorrect Annotation Logic**:
   - The logic for identifying `bd` and `eol` points may not consider multiple events properly.

3. **Plugin Duplication**:
   - You are reusing the `circleAnnotationPlugin` across charts without adapting it for each chart's dataset.

---

### Fixes:

#### 1. Extract `bd` and `eol` Indices for Each Dataset
Instead of calculating the indices globally, calculate them per chart based on the dataset.

#### 2. Pass Event Indices as Chart Data
Store the event indices (`bd` and `eol`) as part of the chart data to make them accessible during rendering.

---

### Updated Code:

#### Refactored Annotation Plugin:
Create a reusable annotation plugin that dynamically adapts to the chart’s dataset.

```javascript
const annotationPlugin = {
    id: 'dynamicAnnotationPlugin',
    beforeDraw: (chart) => {
        const ctx = chart.ctx;
        const xScale = chart.scales.x;
        const yScale = chart.scales.y;

        // Retrieve indices for BD and EOL from chart data
        const bdIndices = chart.data.bdIndices || [];
        const eolIndices = chart.data.eolIndices || [];

        // Draw circles for BD points
        bdIndices.forEach(index => {
            const xPixel = xScale.getPixelForValue(chart.data.labels[index]);
            const yPixel = yScale.getPixelForValue(chart.data.datasets[0].data[index]);

            ctx.save();
            ctx.beginPath();
            ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for BD
            ctx.lineWidth = 2;
            ctx.strokeStyle = 'green';
            ctx.stroke();
            ctx.restore();
        });

        // Draw circles for EOL points
        eolIndices.forEach(index => {
            const xPixel = xScale.getPixelForValue(chart.data.labels[index]);
            const yPixel = yScale.getPixelForValue(chart.data.datasets[0].data[index]);

            ctx.save();
            ctx.beginPath();
            ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for EOL
            ctx.lineWidth = 2;
            ctx.strokeStyle = 'red';
            ctx.stroke();
            ctx.restore();
        });
    }
};
```

---

#### Example Chart Setup:

For each chart, calculate the `bd` and `eol` indices and pass them to the `chart.data`.

```javascript
function createChart(ctx, data, label, borderColor, indices) {
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
            bdIndices: indices.bdIndices, // Pass BD indices
            eolIndices: indices.eolIndices // Pass EOL indices
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

#### Function to Create Each Chart:

```javascript
function updateChart(data, chartRef, ctxId, label, color) {
    const ctx = document.getElementById(ctxId).getContext('2d');

    if (chartRef) chartRef.destroy();

    // Calculate BD and EOL indices
    const bdIndices = data.bd
        .map((value, index) => (value !== 0 ? index : null))
        .filter(index => index !== null);

    const eolIndices = data.eol
        .map((value, index) => (value !== 0 ? index : null))
        .filter(index => index !== null);

    return createChart(ctx, data, label, color, { bdIndices, eolIndices });
}

// Update specific charts
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

### How It Works:
1. **Annotation Plugin**:
   - Dynamically draws `bd` and `eol` points based on indices passed in the chart’s data.

2. **Reusable Chart Creation**:
   - Simplifies chart setup with a function that handles annotations for any dataset.

3. **Dynamic Indices**:
   - Calculates indices for each dataset (`bd` and `eol`) and attaches them to the chart.

---

Let me know if additional refinements are needed!
