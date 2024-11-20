function updateGraph3Chart(data) {
    const ctx = document.getElementById('graph3Chart').getContext('2d');

    const graph3Chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels, // Replace with appropriate data
            datasets: [{
                label: 'Graph 3 Data',
                data: data.values, // Replace with appropriate data
                borderColor: 'rgb(153, 102, 255)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'X-Axis Label' } },
                y: { title: { display: true, text: 'Y-Axis Label' } }
            },
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'xy'
                    },
                    zoom: {
                        wheel: { enabled: true },
                        pinch: { enabled: true },
                        mode: 'xy'
                    }
                }
            }
        }
    });
}
