let voltageChart, currentChart, capacitorHealthChart;

// Initialize empty graphs when the page loads
function initializeEmptyGraphs() {
    // Voltage Chart
    const voltageCtx = document.getElementById('voltageChart').getContext('2d');
    voltageChart = new Chart(voltageCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Voltage vs Time',
                data: [],
                borderColor: 'blue',
                fill: false
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time (s)' } },
                y: { title: { display: true, text: 'Voltage (V)' } }
            }
        }
    });

    // Current Chart
    const currentCtx = document.getElementById('currentChart').getContext('2d');
    currentChart = new Chart(currentCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Current vs Time',
                data: [],
                borderColor: 'green',
                fill: false
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time (s)' } },
                y: { title: { display: true, text: 'Current (A)' } }
            }
        }
    });

    // Capacitor Health Chart
    const capacitorCtx = document.getElementById('capacitorHealthChart').getContext('2d');
    capacitorHealthChart = new Chart(capacitorCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Capacitor Health vs Time',
                data: [],
                borderColor: 'red',
                fill: false
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time (s)' } },
                y: { title: { display: true, text: 'Health (%)' } }
            }
        }
    });
}

// Update the graphs when a device is selected
async function updateGraphsForDevice(device) {
    // Update Voltage Chart
    await updateGraph(voltageChart, device, 'voltageData.txt', 'Voltage vs Time');

    // Update Current Chart
    await updateGraph(currentChart, device, 'currentData.txt', 'Current vs Time');

    // Update Capacitor Health Chart
    await updateGraph(capacitorHealthChart, device, 'capacitorHealthData.txt', 'Capacitor Health vs Time');
}

// Function to update a specific graph with data
async function updateGraph(chart, device, fileName, label) {
    const { xValues, yValues } = await fetchDataWithDetails(device, fileName);

    // Update the chart data
    chart.data.labels = xValues;
    chart.data.datasets[0].data = yValues;
    chart.data.datasets[0].label = label;
    chart.update(); // Redraw the chart with the new data
}

// Function to fetch data from the text files
async function fetchDataWithDetails(device, fileName) {
    const response = await fetch(`/data/${device}/${fileName}`);
    const data = await response.text();
    const lines = data.trim().split('\n').map(line => line.split(',').map(Number));
    const xValues = lines.map(line => line[0]); // First column is X values
    const yValues = lines.map(line => line[1]); // Second column is Y values
    return { xValues, yValues };
}

// Load empty graphs on page load
window.onload = function() {
    initializeEmptyGraphs(); // Initialize the graphs with no data
};
