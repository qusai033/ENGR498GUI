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
                borderColor: 'rgb(255, 99, 132)',
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
            borderColor: 'rgb(54, 162, 132)',
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
            //maintainAspectRatio: true,
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
            //maintainAspectRatio: true,
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
    console.log("SoH Data:", data.fd);
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
            //maintainAspectRatio: true,
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
                tension: 0.1,
                fill: false,
                pointRadius: 0,
                pointBackgroundColor: 'transparent',
                pointBorderWidth: 1
            }]
        },
        options: {
            responsive: true,
            //maintainAspectRatio: true,
            scales: {
                x: { title: { display: true, text: 'Time (MS)' } },
                y: { title: { display: true, text: 'Voltage (V)' } }
            },
            plugins: {
                zoom: zoomOptions,
                title: {
                    display: true,
                    position: 'bottom',
                    //text: (ctx) => `Zoom: ${zoomStatus(ctx.chart)}, Pan: ${panStatus()}`
                }
            }
        }
    });
    adjustCharts(); // Adjust size dynamically after creation
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




function sendRequest(action) {
    fetch(`http://192.168.0.158${action}`, { method: 'GET' })
        .then(response => response.text())
        .then(data => console.log('Response from Arduino:', data))
        .catch(error => console.error('Error:', error));
}

function adjustCharts() {
    const charts = [voltageChart, rulChart, sohChart, fdChart];
    charts.forEach(chart => {
        if (chart) {
            chart.resize(); // Dynamically resize chart
        }
    });
}

// Attach resize event listener
window.addEventListener('resize', adjustCharts);

// Load devices on page load
window.onload = loadDevices;


* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f5f5f5;
  padding: 10px 20px;
}

.header img {
  height: 80px;
}

.content {
  display: flex;
  flex-grow: 1;
  width: 100%;
}

.sidebar {
  width: 7%;
  min-width: 100px; /* Ensures the sidebar stays visible on smaller screens */
  background-color: #e0e0e0;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
}

.nav-button {
  margin: 10px;
  padding: 0px;
  background-color: #9ec5fe;
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  text-align: center;
  font-size: 14px;
  cursor: pointer;
}

.nav-button:hover {
  background-color: #6495ed;
}

.graphs-grid {
  flex-grow: 1;
  display: grid;
  grid-template-columns: 1fr 1fr; /* Two columns */
  grid-template-rows: auto auto; /* Two rows */
  grid-auto-rows: 1fr; /* Automatically adjust row height */
  grid-column: 1fr;
  grid-gap: 20px;      /* Space between graphs */
  padding: 20px;
  background-color: #f0f8ff;
  transition: all 0.1s ease-in-out; /* Smooth transition during resizing */
  position: relative;
  height: auto;
  max-height: calc(100vh - 100px); /* Account for header/footer */
}


.graph {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #cfe2f3;
  border: 1px solid #000;
  padding: 10px;
  height: auto;
  max-height: 50vh; /* Constrain to half the viewport height */
  width: 100%;
}

.graph canvas {
  width: 100%;
  height: calc(100% - 20px); /* Dynamically adjust height */
}


/* Styling for the search input inside the dropdown */
.search-input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

/* Search results dropdown container */
.search-results {
  max-height: 150px;
  overflow-y: auto;
  background-color: #ffffff;  /* Set background to white */
  border: 1px solid #ccc;  /* Optional: Light border around the search results */
  position: absolute;
  top: 100%;  /* Positioned just below the search input */
  width: 100%;
  z-index: 1;
  box-shadow: none; /* Removed shadow to avoid gray box appearance */
  padding: 0;  /* Ensure no padding creates extra space */
  border-radius: 4px; /* Add border-radius to smooth the corners */
}

/* Individual device item styling */
.device-item {
  padding: 8px 12px;  /* Adjust padding for device item */
  cursor: pointer;
  border-bottom: 1px solid #ddd;  /* Adds a thin separation between items */
  background-color: #fff;  /* Keep background of each device white */
}


/* Hover effect for each device item */
.device-item:hover {
  background-color: #f0f0f0;  /* Light gray background on hover */
}

/* Ensure the last device item does not have a border at the bottom */
.device-item:last-child {
  border-bottom: none;
}


  /* Styling for the device dropdown and search input */
  .dropdown {
    position: relative;
    display: inline-block;
  }
  
  .dropdown-content {
    display: none;
    position: absolute;
    background-color: #f1f1f1;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
  }
  
  .dropdown-content div {
    color: black;
    padding: 7px 3px;
    text-decoration: none;
    display: block;
    cursor: pointer;
  }
  
  .dropdown-content div:hover {
    background-color: #ddd;
  }
  
  .dropdown:hover .dropdown-content {
    display: block;
  }
  
  
  .device-list {
    max-height: 200px;
    overflow-y: auto;
  }


/* Responsive Design */
@media screen and (max-width: 1024px) {
  .graphs-grid {
    grid-template-columns: 1fr; /* Switch to one column */
    grid-gap: 10px;             /* Keep space between rows */
  }

  .sidebar {
    width: 7%; /* Adjust sidebar width */
  }

  .graph canvas {
    height: 80%; /* Adjust graph size proportionally */
  }

}

@media screen and (max-width: 768px) {
  .graphs-grid {
    grid-template-columns: 1fr; /* Stack graphs in one column */
    grid-gap: 10px;             /* Reduce gap between graphs */
  }

  .sidebar {
    width: 7%; /* Wider sidebar for very small screens */
  }

  .graph canvas {
    height: auto; /* Further reduce graph height */
  }

}
