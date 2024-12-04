To resolve the issue where BD (Beginning of Degradation) and EOL (End of Life) annotations are not appearing on the graphs when switching devices, the problem is likely due to the BD and EOL indices not being recalculated or passed properly for each new dataset. Here's how you can fix it:

### Key Fixes:

1. **Recalculate BD and EOL Indices for Each Graph**:
   Ensure the `bdIndex` and `eolIndex` are recalculated and passed for every new dataset.

2. **Unified Annotation Plugin**:
   Refactor the `circleAnnotationPlugin` logic to dynamically handle BD and EOL annotations for all graphs.

---

### Updated Code

#### Centralized Annotation Plugin
This plugin ensures BD and EOL annotations are dynamically recalculated and displayed for all graphs.

```javascript
const annotationPlugin = {
    id: 'dynamicAnnotationPlugin',
    beforeDraw: (chart) => {
        const ctx = chart.ctx;
        const xScale = chart.scales.x;
        const yScale = chart.scales.y;

        const bdIndex = chart.data.bdIndex;
        const eolIndex = chart.data.eolIndex;

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

#### Update Graph Functions

Each graph function now calculates the `bdIndex` and `eolIndex` and passes them to the chart data.

##### Example: RUL Chart
```javascript
function updateRulChart(data) {
    const ctx = document.getElementById('rulChart').getContext('2d');

    if (rulChart) rulChart.destroy();

    const bdIndex = data.bd.findIndex(value => value !== 0);
    const eolIndex = data.eol.findIndex(value => value !== 0);

    rulChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [
                {
                    label: 'Remaining Useful Life (RUL)',
                    data: data.rul,
                    borderColor: 'rgb(255, 165, 0)',
                    tension: 0.1,
                    fill: false,
                    pointRadius: 0
                },
                {
                    label: 'Prognostic Health (PH)',
                    data: data.ph,
                    borderColor: 'rgb(0, 150, 136)',
                    tension: 0.1,
                    fill: false,
                    pointRadius: 0
                }
            ],
            bdIndex: bdIndex !== -1 ? bdIndex : null,
            eolIndex: eolIndex !== -1 ? eolIndex : null
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
        plugins: [annotationPlugin]
    });
}
```

##### Example: SoH Chart
```javascript
function updateSoHChart(data) {
    const ctx = document.getElementById('sohChart').getContext('2d');

    if (sohChart) sohChart.destroy();

    const bdIndex = data.bd.findIndex(value => value !== 0);
    const eolIndex = data.eol.findIndex(value => value !== 0);

    sohChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [{
                label: 'State-of-Health (SoH)',
                data: data.soh,
                borderColor: 'rgb(153, 102, 255)',
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

#### Adjust Device Switching Logic

Ensure all graphs are updated with the correct dataset and annotations when switching devices.

```javascript
function showGraphsForDevice(device) {
    fetch(`/data/${device}/voltageData.csv`)
        .then(response => response.json())
        .then(data => updateVoltageChart(data));

    fetch(`/data/${device}/rulData.csv`)
        .then(response => {
            if (!response.ok) throw new Error('Data not found');
            return response.json();
        })
        .then(data => {
            updateRulChart(data);
            updateSoHChart(data);
            updateFDChart(data);
        })
        .catch(error => console.error('Error loading data:', error));
}
```

---

### Summary of Changes
1. **Dynamic Annotations**:
   - The `dynamicAnnotationPlugin` dynamically calculates BD and EOL indices for each graph.
   - This ensures annotations are refreshed correctly when switching devices.

2. **Consistent Annotation Handling**:
   - Centralized logic for BD and EOL annotations across all graphs.

3. **Multi-Line RUL Chart**:
   - The RUL chart includes both RUL and PH lines.

4. **Device Switching**:
   - All graphs are updated properly with new data and annotations when switching devices.

This implementation ensures that BD and EOL annotations work correctly for all graphs and devices. Let me know if you need further adjustments!
