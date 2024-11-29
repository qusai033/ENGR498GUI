const chart = new Chart(ctx, {
    type: 'line',
    data: { /* chart data */ },
    options: {
        responsive: true, // Make the chart responsive
        maintainAspectRatio: false, // Allow the aspect ratio to change with resizing
        scales: {
            x: { title: { display: true, text: 'Time' } },
            y: { title: { display: true, text: 'Value' } },
        },
        plugins: {
            legend: {
                display: true,
            },
        },
    },
});



.graphs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* Automatically adjust columns */
  grid-gap: 20px; /* Space between graphs */
  padding: 20px;
}

.graph {
  width: 100%; /* Allow it to stretch */
  height: 100%; /* Let it adjust dynamically */
  aspect-ratio: 16 / 9; /* Maintain a proper aspect ratio */
  background-color: #cfe2f3;
  border: 1px solid #000;
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.graph canvas {
  width: 100% !important;
  height: auto !important;
}


window.addEventListener('resize', () => {
    if (chart) chart.resize(); // Resize the chart dynamically
});
