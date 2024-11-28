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
                        if (context.dataIndex === eolIndex || context.dataIndex === bdIndex) return 8; // Larger for EOL/BD
                        return 3; // Default size
                    },
                    pointBorderColor: (context) => {
                        // Color only the border for specific points
                        if (context.dataIndex === eolIndex) return 'red';
                        if (context.dataIndex === bdIndex) return 'green';
                        return 'transparent'; // Default no color
                    },
                    pointBackgroundColor: 'transparent', // Keep points hollow
                    pointBorderWidth: (context) => {
                        // Thicker border for EOL and BD
                        if (context.dataIndex === eolIndex || context.dataIndex === bdIndex) return 2;
                        return 1;
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

                    // Draw hollow circles on the corresponding data points
                    if (bdIndex !== -1) {
                        const xPixel = xScale.getPixelForValue(data.time[bdIndex]);
                        const yPixel = yScale.getPixelForValue(data.rul[bdIndex]);

                        ctx.save();
                        ctx.beginPath();
                        ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Outer circle
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = 'green';
                        ctx.stroke();
                        ctx.restore();
                    }

                    if (eolIndex !== -1) {
                        const xPixel = xScale.getPixelForValue(data.time[eolIndex]);
                        const yPixel = yScale.getPixelForValue(data.rul[eolIndex]);

                        ctx.save();
                        ctx.beginPath();
                        ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Outer circle
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = 'red';
                        ctx.stroke();
                        ctx.restore();
                    }
                }
            }
        ]
    });
}
