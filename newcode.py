// Update the voltage chart with the fetched data
function updateVoltageChart(data) {
    const ctx = document.getElementById('voltageChart').getContext('2d');
    const voltageData = parseData(data);  // Parse the data into labels and values

    // Destroy the old chart instance before creating a new one
    if (voltageChart) {
        voltageChart.destroy();
    }

    voltageChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: voltageData.labels,
            datasets: [{
                label: 'Voltage vs Time',
                data: voltageData.values,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: {
                    title: { display: true, text: 'Time (second)'}
                },
                y: {
                    title: { display: true, text: 'Voltage (V)'}
                }
            },
            Plugins: {
                zoom:{
                    zoom: {
                        wheel: {
                            enabled: true //enable zooming with the mouse wheel
                        },
                        pinch: {
                            enabled: true // enable zooming with pinch devices
                        },
                        mode: 'xy' // zoom in both x and y directions
                    },
                    pan: {
                        enabled: true,
                        mode: 'xy' //allowing panning in both x, y directions
                    }
                }
            }
        }
    });
}

