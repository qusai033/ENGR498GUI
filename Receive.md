The issue seems to stem from the BD and EOL indices or vertical lines not being correctly updated for some devices. Let’s fix this step by step:

### Key Areas to Investigate and Resolve:
1. **Cleaned Data Handling**:
   Ensure `data.bd`, `data.eol`, and `data.time` are correctly parsed and processed, as they are crucial for determining BD and EOL indices.

2. **Vertical Line Updates**:
   Ensure `verticalLines` is updated consistently when switching devices.

3. **Chart Redrawing**:
   Ensure charts are fully redrawn with the updated vertical lines and annotations when switching devices.

---

### Fix Implementation

#### Update `showGraphsForDevice`

- Ensure `verticalLines` and indices (`bdIndex`, `eolIndex`) are updated and passed correctly for every dataset.

```javascript
function showGraphsForDevice(device) {
    console.log("Switching to Device:", device);

    // Fetch Voltage Data
    fetch(`/data/${device}/voltageData.csv`)
        .then(response => response.json())
        .then(data => updateVoltageChart(data))
        .catch(error => console.error('Error loading voltage data:', error));

    // Fetch RUL Data
    fetch(`/data/${device}/rulData.csv`)
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Data for Device:", device);

            // Debug raw data
            console.log("Raw BD Array:", data.bd);
            console.log("Raw EOL Array:", data.eol);
            console.log("Raw Time Array:", data.time);

            // Clear old vertical line states
            verticalLines[0].x = null; // Clear EOL
            verticalLines[1].x = null; // Clear BD

            // Clean BD and EOL arrays
            const cleanBd = data.bd.map(value => Number(value)).filter(value => !isNaN(value));
            const cleanEol = data.eol.map(value => Number(value)).filter(value => !isNaN(value));

            console.log("Clean BD Array:", cleanBd);
            console.log("Clean EOL Array:", cleanEol);

            // Find BD and EOL indices
            const bdIndex = cleanBd.findIndex(value => value !== 0);
            const eolIndex = cleanEol.findIndex(value => value !== 0);

            console.log("BD Index:", bdIndex, "EOL Index:", eolIndex);

            if (bdIndex < 0 || eolIndex < 0) {
                console.warn("BD or EOL not found in the current dataset.");
                return;
            }

            // Update vertical lines with corresponding time values
            verticalLines[1].x = data.time[bdIndex]; // BD line
            verticalLines[0].x = data.time[eolIndex]; // EOL line

            console.log("Updated Vertical Lines:", verticalLines);

            // Update charts with the new data and indices
            updateRulChart(data, bdIndex, eolIndex);
            updateSoHChart(data, bdIndex, eolIndex);
            updateFDChart(data, bdIndex, eolIndex);
        })
        .catch(error => console.error('Error loading RUL data:', error));
}
```

---

#### Ensure Vertical Lines Update Consistently in Charts

For each chart (`updateRulChart`, `updateSoHChart`, `updateFDChart`), use `verticalLines` for vertical line plotting. Ensure the `beforeDraw` plugin dynamically reflects these values.

Example for the RUL Chart:

```javascript
function updateRulChart(data, bdIndex, eolIndex) {
    const ctx = document.getElementById('rulChart').getContext('2d');

    if (rulChart) rulChart.destroy();

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
            bdIndex: bdIndex,
            eolIndex: eolIndex
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
        plugins: [{
            id: 'verticalLinePlugin',
            beforeDraw: (chart) => {
                const ctx = chart.ctx;
                const xScale = chart.scales.x;
                const yScale = chart.scales.y;

                // Loop through vertical lines and draw them
                verticalLines.forEach(line => {
                    if (!line.visible || line.x === null) return;

                    const xPixel = xScale.getPixelForValue(line.x);

                    ctx.save();
                    ctx.setLineDash([5, 5]); // Dotted line
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
        }]
    });
}
```

Repeat a similar implementation for `updateSoHChart` and `updateFDChart`.

---

### Debugging Steps
1. **Verify `verticalLines` Values**:
   - Log the `verticalLines` array after updating for each device. Ensure it shows the correct `x` values (from `data.time`).

2. **Check Chart Updates**:
   - Log messages in the `beforeDraw` plugin to confirm the `verticalLines` are being processed.

3. **Validate `data.time` Consistency**:
   - Ensure the `data.time` array for each device matches the expected format and values.

---

### Expected Outcome
Switching devices will correctly update and display BD and EOL vertical lines on all charts. Each dataset will correctly reflect its unique indices.
