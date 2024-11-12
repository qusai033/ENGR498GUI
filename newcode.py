<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@1.2.1"></script>
<button onclick="resetZoom()">Reset Zoom</button>
function resetZoom() {
    if (voltageChart) {
        voltageChart.resetZoom();
    }
    if (rulChart) {
        rulChart.resetZoom();
    }
}


function updateVoltageChart(data) {
    const ctx = document.getElementById('voltageChart').getContext('2d');

    if (voltageChart) {
        voltageChart.destroy();
    }

    voltageChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [{
                label: 'Voltage vs Time',
                data: data.voltage,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: {
                    title: { display: true, text: 'Time (seconds)' }
                },
                y: {
                    title: { display: true, text: 'Voltage (V)' }
                }
            },
            plugins: {
                zoom: {
                    zoom: {
                        wheel: {
                            enabled: true  // Enable zooming with the mouse wheel
                        },
                        pinch: {
                            enabled: true  // Enable zooming with pinch gestures on touch devices
                        },
                        mode: 'xy'  // Zoom in both x and y directions
                    },
                    pan: {
                        enabled: true,
                        mode: 'xy'  // Allow panning in both x and y directions
                    }
                }
            }
        }
    });
}


function updateRulChart(data) {
    const ctx = document.getElementById('rulChart').getContext('2d');

    if (rulChart) {
        rulChart.destroy();
    }

    rulChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [{
                label: 'Remaining Useful Life (RUL)',
                data: data.rul,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    title: { display: true, text: 'Time (seconds)' }
                },
                y: {
                    title: { display: true, text: 'RUL' }
                }
            },
            plugins: {
                zoom: {
                    zoom: {
                        wheel: {
                            enabled: true
                        },
                        pinch: {
                            enabled: true
                        },
                        mode: 'xy'
                    },
                    pan: {
                        enabled: true,
                        mode: 'xy'
                    }
                }
            }
        }
    });
}
