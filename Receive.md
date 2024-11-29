If you are only using `responsive: true` and avoiding `maintainAspectRatio: false` due to stretching issues, here's a more tailored approach to handle resizing properly without distortion:

---

### Key Adjustments to Avoid Stretching
1. **Ensure Parent Container Resizing:** The chart’s parent container must resize properly. Constrain its width and height dynamically via CSS.
2. **Dynamic Height for Graphs:** Use percentages or `vh` units for height to prevent hardcoded dimensions.
3. **Aspect Ratio Handling via CSS:** Let Chart.js inherit width and height from the parent container.

---

### Step 1: CSS for `.graph` and `.canvas`
Define styles to ensure the container adapts to the screen size while maintaining proper scaling.

```css
.graph {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #cfe2f3;
    border: 1px solid #000;
    padding: 10px;
    height: auto;
    max-height: 50vh; /* Constrain to half the viewport height */
    width: 100%;
}

.graph canvas {
    width: 100%;
    height: calc(100% - 20px); /* Dynamically adjust height */
}
```

---

### Step 2: Chart.js Options
Use only `responsive: true` and let the aspect ratio remain the default (4:3).

```javascript
const commonOptions = {
    responsive: true,
    plugins: {
        legend: {
            display: true,
            position: 'top'
        },
        zoom: {
            pan: {
                enabled: true,
                mode: 'xy'
            },
            zoom: {
                wheel: {
                    enabled: true
                },
                pinch: {
                    enabled: true
                },
                mode: 'xy'
            }
        }
    },
    scales: {
        x: {
            title: {
                display: true,
                text: 'Time'
            }
        },
        y: {
            title: {
                display: true,
                text: 'Value'
            }
        }
    }
};
```

---

### Step 3: Handle Resizing
Use the `resize` event to handle container changes dynamically.

```javascript
function adjustCharts() {
    const charts = [voltageChart, rulChart, sohChart, fdChart];
    charts.forEach(chart => {
        if (chart) {
            chart.resize(); // Dynamically resize chart
        }
    });
}

// Attach resize event listener
window.addEventListener('resize', adjustCharts);
```

---

### Step 4: Ensure Parent Resizing
If the parent container (`.graphs-grid` or `.graph`) isn't resizing correctly, ensure it has dynamic dimensions.

```css
.graphs-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
    gap: 20px;
    padding: 20px;
    height: auto;
    max-height: calc(100vh - 100px); /* Account for header/footer */
}
```

---

### Step 5: Final Implementation Example
Here’s how the `updateVoltageChart` might look:

```javascript
function updateVoltageChart(data) {
    const ctx = document.getElementById('voltageChart').getContext('2d');

    if (voltageChart) voltageChart.destroy();

    voltageChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [{
                label: 'Voltage Decay',
                data: data.voltage,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                fill: false
            }]
        },
        options: commonOptions
    });

    adjustCharts(); // Adjust size dynamically after creation
}
```

---

### Expected Outcome
- The chart adapts to window resizing without distortion.
- The `responsive: true` ensures charts scale proportionally within their parent containers.
- No stretching occurs because `maintainAspectRatio` defaults to `true`.
