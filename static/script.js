function updateSoHChart(data) {
    const ctx = document.getElementById('sohChart').getContext('2d');

    if (sohChart) sohChart.destroy();

    sohChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [{
                label: 'State-of-Health (SoH)',
                data: data.soh,
                borderColor: 'rgb(153, 102, 255)',
                tension: 0.1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'SoH [%]' } }
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
                id: 'circlePlugin',
                beforeDraw: (chart) => {
                    const ctx = chart.ctx;
                    const xScale = chart.scales.x;
                    const yScale = chart.scales.y;

                    // Determine the circle position from the data
                    const highlightIndex = data.soh.findIndex(value => value > SOME_CONDITION); // Replace with your condition
                    if (highlightIndex !== -1) {
                        const xValue = data.time[highlightIndex];
                        const yValue = data.soh[highlightIndex];

                        const xPixel = xScale.getPixelForValue(xValue);
                        const yPixel = yScale.getPixelForValue(yValue);

                        // Draw the circle
                        ctx.save();
                        ctx.beginPath();
                        ctx.arc(xPixel, yPixel, circleConfig.soh.radius, 0, 2 * Math.PI);
                        ctx.fillStyle = circleConfig.soh.color;
                        ctx.fill();

                        // Draw the label
                        ctx.font = '12px Arial';
                        ctx.fillStyle = circleConfig.soh.color;
                        ctx.textAlign = 'center';
                        ctx.fillText(circleConfig.soh.label, xPixel, yPixel - 10);
                        ctx.restore();
                    }
                }
            }
        ]
    });
}

function updateFDChart(data) {
    const ctx = document.getElementById('fdChart').getContext('2d');

    if (fdChart) fdChart.destroy();

    fdChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [{
                label: 'Feature Data (FD)',
                data: data.fd,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'FD [AU]' } }
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
                id: 'circlePlugin',
                beforeDraw: (chart) => {
                    const ctx = chart.ctx;
                    const xScale = chart.scales.x;
                    const yScale = chart.scales.y;

                    // Determine the circle position from the data
                    const highlightIndex = data.fd.findIndex(value => value > SOME_CONDITION); // Replace with your condition
                    if (highlightIndex !== -1) {
                        const xValue = data.time[highlightIndex];
                        const yValue = data.fd[highlightIndex];

                        const xPixel = xScale.getPixelForValue(xValue);
                        const yPixel = yScale.getPixelForValue(yValue);

                        // Draw the circle
                        ctx.save();
                        ctx.beginPath();
                        ctx.arc(xPixel, yPixel, circleConfig.fd.radius, 0, 2 * Math.PI);
                        ctx.fillStyle = circleConfig.fd.color;
                        ctx.fill();

                        // Draw the label
                        ctx.font = '12px Arial';
                        ctx.fillStyle = circleConfig.fd.color;
                        ctx.textAlign = 'center';
                        ctx.fillText(circleConfig.fd.label, xPixel, yPixel - 10);
                        ctx.restore();
                    }
                }
            }
        ]
    });
}


// Circle configurations
const circleConfig = {
    soh: {
        color: 'red',
        radius: 5,
        label: 'SoH Event'
    },
    fd: {
        color: 'green',
        radius: 5,
        label: 'FD Event'
    }
};
