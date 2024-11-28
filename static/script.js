let rulChart = null;  // Global variable for the RUL chart
let verticalLines = [
    { x: null, label: 'Jump Point', visible: true }, // First vertical line
    { x: null, label: 'Another Point', visible: true } // Second vertical line
];

function updateRulChart(data) {
    const ctx = document.getElementById('rulChart').getContext('2d');

    if (rulChart) rulChart.destroy();

    // Determine positions for each vertical line
    verticalLines[0].x = data.time[data.jumpColumn.findIndex(value => value !== 0)]; // First line
    verticalLines[1].x = data.time[data.jumpColumn.findIndex(value => value === SOME_CONDITION)]; // Replace with your logic for the second line

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

                    verticalLines.forEach(line => {
                        if (!line.visible || line.x === null) return; // Skip if not visible or x is null

                        // Get the pixel position of the vertical line on the x-axis
                        const xPixel = xScale.getPixelForValue(line.x);

                        // Draw the vertical line
                        ctx.save();
                        ctx.beginPath();
                        ctx.moveTo(xPixel, yScale.top); // Start from the top of the y-axis
                        ctx.lineTo(xPixel, yScale.bottom); // Extend to the bottom of the y-axis
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = 'rgba(0, 0, 255, 0.8)'; // Line color and opacity
                        ctx.stroke();

                        // Draw the label for the vertical line
                        ctx.font = '12px Arial';
                        ctx.fillStyle = 'blue';
                        ctx.textAlign = 'center';
                        ctx.fillText(line.label, xPixel, yScale.top - 10); // Label position slightly above the line
                        ctx.restore();
                    });
                }
            }
        ]
    });
}

// Function to toggle visibility of a specific vertical line
function toggleVerticalLine(index) {
    if (verticalLines[index]) {
        verticalLines[index].visible = !verticalLines[index].visible; // Toggle visibility
        rulChart.update(); // Update the chart to reflect the change
    }
}
