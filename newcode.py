// Define zoom options separately
const zoomOptions = {
  limits: {
    x: { min: -200, max: 200, minRange: 50 },
    y: { min: -200, max: 200, minRange: 50 }
  },
  pan: {
    enabled: true,
    mode: 'xy'
  },
  zoom: {
    wheel: { enabled: true },
    pinch: { enabled: true },
    mode: 'xy',
    onZoomComplete({ chart }) {
      chart.update('none');  // Update chart to reflect zoom level
    }
  }
};

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
                label: 'Voltage Decay',
                data: data.voltage,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time (seconds)' } },
                y: { title: { display: true, text: 'Voltage (V)' } }
            },
            plugins: {
                zoom: zoomOptions,
                title: {
                    display: true,
                    position: 'bottom',
                    text: (ctx) => `Zoom: ${zoomStatus(ctx.chart)}, Pan: ${panStatus()}`
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
                x: { title: { display: true, text: 'Time (seconds)' } },
                y: { title: { display: true, text: 'RUL' } }
            },
            plugins: {
                zoom: zoomOptions,
                title: {
                    display: true,
                    position: 'bottom',
                    text: (ctx) => `Zoom: ${zoomStatus(ctx.chart)}, Pan: ${panStatus()}`
                }
            }
        }
    });
}
function zoomStatus(chart) {
    return chart.scales.x.min + ' - ' + chart.scales.x.max;
}

function panStatus() {
    return 'Enabled';
}
