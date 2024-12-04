

// Update the RUL chart with JSON data (no need to parse with parseData)
function updateRulChart(data) {
    const ctx = document.getElementById('rulChart').getContext('2d');

    if (rulChart) rulChart.destroy();

    // Find the indices for BD and EOL in the RUL data
    const bdIndex = data.bd.findIndex(value => value !== 0); // First non-zero BD
    const eolIndex = data.eol.findIndex(value => value !== 0); // First non-zero EOL

    rulChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [{
                label: 'Remaining Useful Life (RUL)',
                data: data.rul,
                borderColor: 'rgb(255, 165, 0)',
                tension: 0.1,
                fill: false,
                pointRadius: (context) => {
                    // Highlight specific points with a larger radius
                    if (context.dataIndex === eolIndex) return 0; // Larger for EOL
                    if (context.dataIndex === bdIndex) return 0; // Larger for BD
                    return 0; // Default size
                },
                pointBackgroundColor: (context) => {
                    // Change color for specific points
                    if (context.dataIndex === eolIndex) return 'red';
                    if (context.dataIndex === bdIndex) return 'green';
                    return 'transparent'; // Default no color
                },
                pointBackgroundColor: 'transparent',
                pointBorderWidth: (context) => {
                    // Thicker border for EOL and BD
                    if (context.dataIndex === eolIndex || context.dataIndex === bdIndex) return 1;
                    return 1;
                }
            },
            {
            label: 'Prognostic (PH)',
            data: data.ph,
            borderColor: 'rgb(0, 150, 136)',
            tension: 0.1,
            fill: false,
            pointRadius: (context) => {
                // Highlight specific points with a larger radius
                if (context.dataIndex === eolIndex) return 0; // Larger for EOL
                if (context.dataIndex === bdIndex) return 0; // Larger for BD
                return 0; // Default size
            },
            pointBackgroundColor: (context) => {
                // Change color for specific points
                if (context.dataIndex === eolIndex) return 'red';
                if (context.dataIndex === bdIndex) return 'green';
                return 'transparent'; // Default no color
            },
            pointBackgroundColor: 'transparent',
            pointBorderWidth: (context) => {
                // Thicker border for EOL and BD
                if (context.dataIndex === eolIndex || context.dataIndex === bdIndex) return 1;
                return 1;
            }
        
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'RUL/PH [AU]' } }
            },
            plugins: {
                zoom: zoomOptions,
                title: {
                    display: true,
                    position: 'bottom',
                    //text: (ctx) => `Zoom: ${zoomStatus(ctx.chart)}, Pan: ${panStatus()}`
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
                        ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for BD
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
                        ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for EOL
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = 'red';
                        ctx.stroke();
                        ctx.restore();
                    }
                }
            },
            {
                id: 'circleAnnotationPlugin',
                beforeDraw: (chart) => {
                    const ctx = chart.ctx;
                    const xScale = chart.scales.x;
                    const yScale = chart.scales.y;

                    // Draw circles on the corresponding data points
                    if (bdIndex !== -1) {
                        const xPixel = xScale.getPixelForValue(data.time[bdIndex]);
                        const yPixel = yScale.getPixelForValue(data.ph[bdIndex]);

                        ctx.save();
                        ctx.beginPath();
                        ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for BD
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = 'green';
                        ctx.stroke();
                        ctx.restore();
                    }

                    if (eolIndex !== -1) {
                        const xPixel = xScale.getPixelForValue(data.time[eolIndex]);
                        const yPixel = yScale.getPixelForValue(data.ph[eolIndex]);

                        ctx.save();
                        ctx.beginPath();
                        ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for EOL
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = 'red';
                        ctx.stroke();
                        ctx.restore();
                    }
                }
            }
        ]
    });
    adjustCharts(); // Adjust size dynamically after creation
}


function updateSoHChart(data) {
    console.log("SoH Data:", data.soh);

    const ctx = document.getElementById('sohChart').getContext('2d');

    if (sohChart) sohChart.destroy();

        // Find the indices for BD and EOL in the RUL data
    const bdIndex = data.bd.findIndex(value => value !== 0); // First non-zero BD
    const eolIndex = data.eol.findIndex(value => value !== 0); // First non-zero EOL

    sohChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time, // Replace with appropriate data
            datasets: [{
                label: 'State-of-Health (SoH)',
                data: data.soh, // Replace with appropriate data
                borderColor: 'rgb(153, 102, 255)',
                tension: 0.1,
                fill: false,
                pointRadius: (context) => {
                    // Highlight specific points with a larger radius
                    if (context.dataIndex === eolIndex) return 0; // Larger for EOL
                    if (context.dataIndex === bdIndex) return 0; // Larger for BD
                    return 0; // Default size
                },
                pointBackgroundColor: (context) => {
                    // Change color for specific points
                    if (context.dataIndex === eolIndex) return 'red';
                    if (context.dataIndex === bdIndex) return 'green';
                    return 'transparent'; // Default no color
                },
                pointBackgroundColor: 'transparent',
                pointBorderWidth: (context) => {
                    // Thicker border for EOL and BD
                    if (context.dataIndex === eolIndex || context.dataIndex === bdIndex) return 1;
                    return 1;
                }
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'SoH [%]' } }
            },
            plugins: {
                zoom: zoomOptions,
                title: {
                    display: true,
                    position: 'bottom',
                    //text: (ctx) => `Zoom: ${zoomStatus(ctx.chart)}, Pan: ${panStatus()}`
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
                        const yPixel = yScale.getPixelForValue(data.soh[bdIndex]);

                        ctx.save();
                        ctx.beginPath();
                        ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for BD
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = 'green';
                        ctx.stroke();
                        ctx.restore();
                    }

                    if (eolIndex !== -1) {
                        const xPixel = xScale.getPixelForValue(data.time[eolIndex]);
                        const yPixel = yScale.getPixelForValue(data.soh[eolIndex]);

                        ctx.save();
                        ctx.beginPath();
                        ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for EOL
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = 'red';
                        ctx.stroke();
                        ctx.restore();
                    }
                }
            }
        ]
    });
    adjustCharts(); // Adjust size dynamically after creation
}


function updateFDChart(data) {
    //console.log("FD Data:", data.fd);
    const ctx = document.getElementById('fdChart').getContext('2d');

    if (fdChart) fdChart.destroy();

            // Find the indices for BD and EOL in the RUL data
    const bdIndex = data.bd.findIndex(value => value !== 0); // First non-zero BD
    const eolIndex = data.eol.findIndex(value => value !== 0); // First non-zero EOL

    verticalLines[0].x = data.time[data.eol.findIndex(value => value !== 0)];
    verticalLines[1].x = data.time[data.bd.findIndex(value => value !== 0)]; // Get the corresponding x-axis value

    fdChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time, // Replace with appropriate data
            datasets: [{
                label: 'Feature Data (FD)',
                data: data.fd, // Replace with appropriate data
                borderColor: 'rgb(255, 51, 135)',
                tension: 0.1,
                fill: false,
                pointRadius: (context) => {
                    // Highlight specific points with a larger radius
                    if (context.dataIndex === eolIndex) return 0; // Larger for EOL
                    if (context.dataIndex === bdIndex) return 0; // Larger for BD
                    return 0; // Default size
                },
                pointBackgroundColor: (context) => {
                    // Change color for specific points
                    if (context.dataIndex === eolIndex) return 'red';
                    if (context.dataIndex === bdIndex) return 'green';
                    return 'transparent'; // Default no color
                },
                pointBackgroundColor: 'transparent',
                pointBorderWidth: (context) => {
                    // Thicker border for EOL and BD
                    if (context.dataIndex === eolIndex || context.dataIndex === bdIndex) return 1;
                    return 1;
                }
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'FD [AU]' } }
            },
            plugins: {
                zoom: zoomOptions,
                title: {
                    display: true,
                    position: 'bottom',
                    //text: (ctx) => `Zoom: ${zoomStatus(ctx.chart)}, Pan: ${panStatus()}`
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
                        ctx.setLineDash([5, 5]); //5px dash line
                        ctx.beginPath();
                        ctx.moveTo(xPixel, yScale.top); // Start from the top of the y-axis
                        ctx.lineTo(xPixel, yScale.bottom); // Extend to the bottom of the y-axis
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = line.color; // Line color and opacity
                        ctx.stroke();

                        // Draw the label for the vertical line
                        ctx.setLineDash([]); //reset line dash for text
                        ctx.font = '12px Arial';
                        ctx.fillStyle = line.color;
                        ctx.textAlign = 'center';
                        ctx.fillText(line.label, xPixel, yScale.top - 10); // Label position slightly above the line
                        ctx.restore();
                    });
                }
            }
        ]
    });
    adjustCharts(); // Adjust size dynamically after creation
}
