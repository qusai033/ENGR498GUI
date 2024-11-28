let voltageChart = null;  // Declare chart globally so it can be destroyed later
let rulChart = null;  // Declare a global variable for the RUL (health) chart
let allDevices = [];  // Store the list of all devices for filtering
let sohChart = null;
let fdChart = null;
let verticalLines = [
    { x: null, label: 'End of Life', visible: true, color: 'red'},
    { x: null, label: 'Beginging of Degradation', visible: true, color: 'green'}
];


function zoomStatus(chart) {
    return chart.scales.x.min + ' - ' + chart.scales.x.max;
}

function panStatus() {
    return 'Enabled';
}
// Define zoom options separately
const zoomOptions = {
    limits: {
      x: { min: -200, max: 200, minRange: 50 },
      y: { min: -200, max: 200, minRange: 50 }
    },
    pan: {
      enabled: true,
      mode: 'xy'
    },
    zoom: {
      wheel: { enabled: true },
      pinch: { enabled: true },
      mode: 'xy',
      onZoomComplete({ chart }) {
        chart.update('none');  // Update chart to reflect zoom level
      }
    }
  };
  
function resetZoom() {
    if (voltageChart) {
        voltageChart.resetZoom();
    }
    if (rulChart) {
        rulChart.resetZoom();
    }
    if (sohChart) {
        sohChart.resetZoom();
    }
    if (fdChart) {
        fdChart.resetZoom();
    }
}
// Function to load all devices from the server
function loadDevices() {
    fetch('/list_devices')
        .then(response => response.json())
        .then(devices => {
            allDevices = devices; // Store the list of all devices for filtering
            displayDevices(devices); // Display the full list of devices initially
        })
        .catch(error => console.error('Error loading devices:', error));
}

function showGraphsForDevice(device) {
    // Fetch and update data for all four graphs
    fetch(`/data/${device}/voltageData.csv`)
        .then(response => response.json())
        .then(data => updateVoltageChart(data));

    fetch(`/data/${device}/rulData.csv`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Data not found');
            }
            return response.json();
        })
        .then(data => {
            console.log("Fetched Data:", data);  // Debug fetched data

            // Update all charts
            updateRulChart(data);  // RUL Chart
            updateSoHChart(data);  // SoH Chart
            updateFDChart(data);   // FD Chart
        })
        .catch(error => console.error('Error loading data:', error));

}

// Update the RUL chart with JSON data (no need to parse with parseData)
function updateRulChart(data) {
    const ctx = document.getElementById('rulChart').getContext('2d');

    if (rulChart) rulChart.destroy();

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
            },
            {
            label: 'Prognostic (PH)',
            data: data.ph,
            borderColor: 'rgb(54, 162, 132)',
            tension: 0.1,
            fill: false
        
            }]
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
        }
    });
}

function updateSoHChart(data) {
    console.log("SoH Data:", data.soh);

    const ctx = document.getElementById('sohChart').getContext('2d');

    if (sohChart) sohChart.destroy();

    sohChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time, // Replace with appropriate data
            datasets: [{
                label: 'State-of-Health (SoH)',
                data: data.soh, // Replace with appropriate data
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
                zoom: zoomOptions,
                title: {
                    display: true,
                    position: 'bottom',
                    text: (ctx) => `Zoom: ${zoomStatus(ctx.chart)}, Pan: ${panStatus()}`
                }
            }
        }
    });
}

function updateFDChart(data) {
    console.log("SoH Data:", data.fd);
    const ctx = document.getElementById('fdChart').getContext('2d');

    if (fdChart) fdChart.destroy();

    verticalLines[0].x = data.time[data.eol.findIndex(value => value !== 0)];
    verticalLines[1].x = data.time[data.bd.findIndex(value => value !== 0)]; // Get the corresponding x-axis value

    fdChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time, // Replace with appropriate data
            datasets: [{
                label: 'Feature Data (FD)',
                data: data.fd, // Replace with appropriate data
                borderColor: 'rgb(153, 102, 255)',
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
}

// Update the voltage chart with the fetched data
function updateVoltageChart(data) {
    const ctx = document.getElementById('voltageChart').getContext('2d');

    if (voltageChart) voltageChart.destroy();

    voltageChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [{
                label: 'Voltage Decay',
                data: data.voltage,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time (seconds)' } },
                y: { title: { display: true, text: 'Voltage (V)' } }
            },
            plugins: {
                zoom: zoomOptions,
                title: {
                    display: true,
                    position: 'bottom',
                    text: (ctx) => `Zoom: ${zoomStatus(ctx.chart)}, Pan: ${panStatus()}`
                }
            }
        }
    });
}


function parseCsvData(data) {
    const lines = data.split('\n');
    const headers = lines[0].split(',');
    const result = {};

    // Initialize result arrays for each column
    headers.forEach(header => result[header] = []);

    // Populate result arrays
    lines.slice(1).forEach(line => {
        const values = line.split(',');
        headers.forEach((header, index) => {
            if (values[index]) {
                result[header].push(parseFloat(values[index]));
            }
        });
    });

    return result;  // Return an object with arrays for each column
}


// Function to display the filtered devices in the dropdown
function displayDevices(devices) {
    const deviceList = document.getElementById('searchResults');
    deviceList.innerHTML = '';  // Clear the existing list

    devices.forEach(device => {
        const div = document.createElement('div');
        div.textContent = device;
        div.classList.add('device-item');
        div.onclick = function() {
            showGraphsForDevice(device); // Load graphs when clicking on a device
        };
        deviceList.appendChild(div);
    });

    document.querySelector('.search-results').style.display = devices.length ? 'block' : 'none'; // Show or hide dropdown
}
// Function to toggle visibility of a specific vertical line
function toggleVerticalLine(index) {
    if (verticalLines[index]) {
        verticalLines[index].visible = !verticalLines[index].visible; // Toggle visibility
        fdChart.update(); // Update the chart to reflect the change
    }
}
// Function to filter devices based on search input
function filterDevices() {
    const query = document.getElementById('deviceSearch').value.toLowerCase();
    const filteredDevices = allDevices.filter(device => device.toLowerCase().includes(query));
    displayDevices(filteredDevices); // Display the filtered devices
}

// Load devices on page load
window.onload = loadDevices;
