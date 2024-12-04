To handle the **BD** and **EOL** logic correctly when switching devices, the issue seems to lie in correctly identifying the indices of **BD** (Beginning of Degradation) and **EOL** (End of Life) from the data. Specifically:

1. **BD and EOL**: These values should correspond to the first non-zero values in their respective columns in the CSV file.
2. **Switching Devices**: When switching devices, the logic must dynamically detect these indices from the new dataset.

---

### Updated Solution for BD and EOL Logic

#### Key Updates
- **Identify BD and EOL**: Use the `findIndex()` method to locate the first non-zero value for BD and EOL.
- **Dynamic Updates on Device Switch**: Ensure the logic dynamically adapts to the new dataset every time a device is switched.

---

### Updated Code

#### Adjust the `showGraphsForDevice` Function
This function ensures that when switching devices, the correct logic for BD and EOL is applied for all charts.

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
            console.log("Fetched Data:", data);  // Debug fetched data

            // Find BD and EOL indices dynamically
            const bdIndex = data.bd.findIndex(value => value !== 0);
            const eolIndex = data.eol.findIndex(value => value !== 0);

            // Pass indices to all charts
            updateRulChart(data, bdIndex, eolIndex);  // RUL Chart
            updateSoHChart(data, bdIndex, eolIndex); // SoH Chart
            updateFDChart(data, bdIndex, eolIndex);  // FD Chart
        })
        .catch(error => console.error('Error loading data:', error));
}
```

---

#### Pass BD and EOL Indices to Chart Update Functions

For each chart, update the function to accept and utilize the `bdIndex` and `eolIndex` values.

##### RUL Chart Example

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

---

##### Apply the Same Logic for Other Charts

For **SoH** and **FD** charts, similarly pass the `bdIndex` and `eolIndex` values to their respective `updateSoHChart` and `updateFDChart` functions. Update the `data.bdIndex` and `data.eolIndex` in their configurations as demonstrated above.

---

### Debugging Tips

1. **CSV Data Validation**:
   - Ensure the CSV files for all devices contain the correct non-zero values for BD and EOL.
   - Use `console.log` to print `bdIndex` and `eolIndex` after detecting them.

2. **Annotation Logic**:
   - Ensure the `dynamicAnnotationPlugin` uses `chart.data.bdIndex` and `chart.data.eolIndex` values to draw circles consistently.

3. **Switching Devices**:
   - Verify that the `showGraphsForDevice` function is correctly reloading and redrawing all graphs with the updated dataset.

---

Let me know if the above solution resolves the issue or if further refinements are needed!
