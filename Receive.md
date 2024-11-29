Based on your observations, it seems the issue lies in how the graphs are being redrawn or resized after data is loaded. Here’s how to ensure the charts resize properly both when the window is expanded and when it’s reduced in size:

---

### 1. **Update Chart.js Responsiveness**
Ensure that the `responsive` and `maintainAspectRatio` options are properly set for all charts. You already have `responsive: true`, but you should also force a resize when the window size changes.

For example, in the chart options:

```javascript
const chartOptions = {
    responsive: true,
    maintainAspectRatio: false, // Allow the chart to resize dynamically
    scales: {
        x: { title: { display: true, text: 'Time (MS)' } },
        y: { title: { display: true, text: 'Voltage (V)' } },
    },
    plugins: {
        zoom: zoomOptions,
        legend: { display: true },
    },
};
```

Ensure all your charts (e.g., `updateVoltageChart`, `updateRulChart`, etc.) use this configuration.

---

### 2. **Handle Window Resize Event**
Add a global resize handler to ensure all charts adjust when the window is resized. You can loop through all the charts and call their `resize` method.

Add the following code to your JavaScript:

```javascript
window.addEventListener('resize', () => {
    if (voltageChart) voltageChart.resize();
    if (rulChart) rulChart.resize();
    if (sohChart) sohChart.resize();
    if (fdChart) fdChart.resize();
});
```

This ensures that all charts respond to window resizing.

---

### 3. **Ensure Containers Are Resizable**
In your CSS, ensure the `.graph` and `.graphs-grid` containers are flexible and adjust dynamically. You’ve already defined `grid-template-columns` and `grid-template-rows` with `1fr`, which is good. Add the following:

```css
.graph {
    flex-grow: 1; /* Allow graphs to grow dynamically */
    min-width: 0; /* Prevent graphs from overflowing */
    max-width: 100%; /* Prevent graphs from exceeding the container */
}

.graph canvas {
    width: 100% !important;
    height: auto !important; /* Adjust canvas height dynamically */
}
```

---

### 4. **Force Chart.js to Resize Dynamically**
When you load data into the chart, force a resize immediately after rendering to ensure the chart fits properly within the container.

For example, in your `updateVoltageChart` function, add:

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
                fill: false,
            }]
        },
        options: chartOptions,
    });

    // Force resize after rendering
    voltageChart.resize();
}
```

Repeat this adjustment for all other `update*Chart` functions.

---

### 5. **Debugging Observations**
If the resizing still doesn’t work, check the following:
- Ensure there are no fixed widths/heights in your CSS that override the responsive behavior.
- Open your browser’s developer tools and inspect the canvas elements to ensure their widths/heights are being adjusted dynamically.

---

### 6. **Fallback Option: Manual Redraw**
If resizing still doesn’t behave as expected, you can destroy and recreate the chart dynamically on resize. While not ideal, this ensures the charts always match the container size:

```javascript
window.addEventListener('resize', () => {
    if (voltageChart) {
        const data = voltageChart.data; // Preserve data
        voltageChart.destroy();
        updateVoltageChart(data); // Recreate chart
    }
    // Repeat for other charts
});
```

---

### 7. **Testing**
After implementing the above steps:
1. Load the GUI with empty graphs.
2. Resize the window (make it smaller and larger) to confirm proper behavior.
3. Load the data and repeat the resizing tests to verify adjustments.

Let me know if this resolves your issue!
