function updateRulChart(data) {
    const ctx = document.getElementById('rulChart').getContext('2d');

    if (rulChart) rulChart.destroy();

    // Find the indices for BD and EOL in the RUL data
    const bdIndex = data.bd.findIndex(value => value !== 0); // First non-zero BD
    const eolIndex = data.eol.findIndex(value => value !== 0); // First non-zero EOL

    // Update the RUL chart
    rulChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time, // X-axis values
            datasets: [
                {
                    label: 'Remaining Useful Life (RUL)',
                    data: data.rul, // RUL data series
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1,
                    fill: false,
                    pointRadius: (context) => {
                        // Highlight specific points with a larger radius
                        if (context.dataIndex === eolIndex) return 6; // Larger for EOL
                        if (context.dataIndex === bdIndex) return 6; // Larger for BD
                        return 3; // Default size
                    },
                    pointBackgroundColor: (context) => {
                        // Change color for specific points
                        if (context.dataIndex === eolIndex) return 'red';
                        if (context.dataIndex === bdIndex) return 'green';
                        return 'transparent'; // Default no color
                    }
                },
                {
                    label: 'Prognostic Health (PH)',
                    data: data.ph, // PH data series
                    borderColor: 'rgb(54, 162, 132)',
                    tension: 0.1,
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'RUL/PH [AU]' } }
            },
            plugins: {
                zoom: zoomOptions,
                title: {
                    display: true,
                    position: 'bottom',
                    text: (ctx) => `Zoom: ${zoomStatus(ctx.chart)}, Pan: ${panStatus()}`
                }
            }
        },
        plugins: [
            {
                id: 'circleAnnotationPlugin',
                beforeDraw: (chart) => {
                    const ctx = chart.ctx;
                    const xScale = chart.scales.x;
                    const yScale = chart.scales.y;

                    // Draw circles on the corresponding data points
                    if (bdIndex !== -1) {
                        const xPixel = xScale.getPixelForValue(data.time[bdIndex]);
                        const yPixel = yScale.getPixelForValue(data.rul[bdIndex]);

                        ctx.save();
                        ctx.beginPath();
                        ctx.arc(xPixel, yPixel, 6, 0, 2 * Math.PI); // Circle for BD
                        ctx.fillStyle = 'green';
                        ctx.fill();
                        ctx.restore();
                    }

                    if (eolIndex !== -1) {
                        const xPixel = xScale.getPixelForValue(data.time[eolIndex]);
                        const yPixel = yScale.getPixelForValue(data.rul[eolIndex]);

                        ctx.save();
                        ctx.beginPath();
                        ctx.arc(xPixel, yPixel, 6, 0, 2 * Math.PI); // Circle for EOL
                        ctx.fillStyle = 'red';
                        ctx.fill();
                        ctx.restore();
                    }
                }
            }
        ]
    });
}
