function updateRulChart(data) {
    const ctx = document.getElementById('rulChart').getContext('2d');

    if (rulChart) rulChart.destroy();

    // Find the index of the non-zero value in the JumpColumn
    const verticalLineIndex = data.jumpColumn.findIndex(value => value !== 0);
    const verticalLineX = data.time[verticalLineIndex]; // Get the corresponding x-axis value

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
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'RUL [AU]' } }
            },
            plugins: {
                zoom: {
                    pan: { enabled: true, mode: 'xy' },
                    zoom: { wheel: { enabled: true }, pinch: { enabled: true }, mode: 'xy' }
                }
            }
        },
        plugins: [
            {
                id: 'verticalLinePlugin',
                beforeDraw: (chart) => {
                    const ctx = chart.ctx;
                    const xScale = chart.scales.x;
                    const yScale = chart.scales.y;

                    // Get the pixel position of the vertical line on the x-axis
                    const xPixel = xScale.getPixelForValue(verticalLineX);

                    // Draw the vertical line
                    ctx.save();
                    ctx.beginPath();
                    ctx.moveTo(xPixel, yScale.top); // Start from the top of the y-axis
                    ctx.lineTo(xPixel, yScale.bottom); // Extend to the bottom of the y-axis
                    ctx.lineWidth = 2;
                    ctx.strokeStyle = 'rgba(0, 0, 255, 0.8)'; // Line color and opacity
                    ctx.stroke();
                    ctx.restore();
                }
            }
        ]
    });
}
