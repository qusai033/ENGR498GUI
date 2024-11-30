sohChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: data.time, // Time data from CSV
        datasets: [{
            label: 'State-of-Health (SoH)',
            data: data.soh, // SoH data from CSV
            borderColor: 'rgb(153, 102, 255)',
            tension: 0.1,
            fill: false,
            pointRadius: 0, // Default points not visible
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: { title: { display: true, text: 'Time [AU]' } },
            y: { title: { display: true, text: 'SoH [%]' } }
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

                // Annotate all BD points
                data.bd.forEach((bdValue, index) => {
                    if (bdValue !== 0) {
                        const xPixel = xScale.getPixelForValue(data.time[index]);
                        const yPixel = yScale.getPixelForValue(data.soh[index]);

                        ctx.save();
                        ctx.beginPath();
                        ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for BD
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = 'green';
                        ctx.stroke();
                        ctx.restore();
                    }
                });

                // Annotate all EOL points
                data.eol.forEach((eolValue, index) => {
                    if (eolValue !== 0) {
                        const xPixel = xScale.getPixelForValue(data.time[index]);
                        const yPixel = yScale.getPixelForValue(data.soh[index]);

                        ctx.save();
                        ctx.beginPath();
                        ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for EOL
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = 'red';
                        ctx.stroke();
                        ctx.restore();
                    }
                });
            }
        }
    ]
});
