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
    console.log("Switching to Device:", device);

    // Fetch Voltage Data
    fetch(`/data/${device}/voltageData.csv`)
        .then(response => response.json())
        .then(data => {
            // Ensure data arrays are non-empty
            if (!data.time || data.time.length === 0) {
                data.time = [0]; // Default to a single zero entry
                data.voltage = [0]; // Default voltage value
            }
            updateVoltageChart(data);
        })
        .catch(error => console.error('Error loading voltage data:', error));


    // Fetch RUL Data
    fetch(`/data/${device}/rulData.csv`)
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Data for Device:", device);

            console.log("Fetched Data:", data);

            // Clear old vertical line states
            verticalLines[0].x = null; // Clear EOL
            verticalLines[1].x = null; // Clear BD

            // Ensure non-empty arrays and replace `-NaN` or `NaN` with `0`
            Object.keys(data).forEach(key => {
                if (Array.isArray(data[key])) {
                    data[key] = data[key].map(value => isNaN(value) ? 0 : value);
                }
            });

            // Default to zero if BD/EOL indices are missing
            const bdIndex = data.bd.findIndex(value => value !== -1) || 0;
            const eolIndex = data.eol.findIndex(value => value !== 0) || 0;


            // Update vertical lines with corresponding time values
            verticalLines[1].x = data.time[bdIndex]; // BD line
            verticalLines[0].x = data.time[eolIndex]; // EOL line

            console.log("Updated Vertical Lines:", verticalLines);

            // Update charts with the new data and indices
            updateRulChart(data, bdIndex, eolIndex);
            updateSoHChart(data, bdIndex, eolIndex);
            updateFDChart(data, bdIndex, eolIndex);
        })
        .catch(error => console.error('Error loading RUL data:', error));
}


const annotationPlugin = {
    id: 'dynamicAnnotationPlugin',
    beforeDraw: (chart) => {
        const ctx = chart.ctx;
        const xScale = chart.scales.x;
        const yScale = chart.scales.y;

        const bdIndex = chart.data.bdIndex;
        const eolIndex = chart.data.eolIndex;

        if (bdIndex !== null && bdIndex >= 0) {
            const xPixel = xScale.getPixelForValue(chart.data.labels[bdIndex]);
            const yPixel = yScale.getPixelForValue(chart.data.datasets[0].data[bdIndex]);
            ctx.save();
            ctx.beginPath();
            ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for BD
            ctx.lineWidth = 2;
            ctx.strokeStyle = 'green';
            ctx.stroke();
            ctx.restore();
        }

        if (eolIndex !== null && eolIndex >= 0) {
            const xPixel = xScale.getPixelForValue(chart.data.labels[eolIndex]);
            const yPixel = yScale.getPixelForValue(chart.data.datasets[0].data[eolIndex]);
            ctx.save();
            ctx.beginPath();
            ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for EOL
            ctx.lineWidth = 2;
            ctx.strokeStyle = 'red';
            ctx.stroke();
            ctx.restore();
        }
    }
};


const verticalLinePlugin = {
    id: 'verticalLinePlugin',
    beforeDraw: (chart) => {
        const ctx = chart.ctx;
        const xScale = chart.scales.x;
        const yScale = chart.scales.y;

        if (!xScale || !yScale) {
            console.warn("Scales not initialized. Cannot draw vertical lines.");
            return;
        }

        verticalLines.forEach(line => {
            if (!line.visible || line.x === null) {
                console.log("Skipping line:", line);
                return; // Skip if not visible or `x` is null
            }

            const xPixel = xScale.getPixelForValue(line.x);

            if (isNaN(xPixel) || xPixel === undefined) {
                console.warn("Invalid xPixel for line:", line, "xScale domain:", xScale.min, "-", xScale.max);
                return; // Skip invalid pixel calculations
            }

            // Draw vertical line
            ctx.save();
            ctx.setLineDash([5, 5]); // Dashed line
            ctx.beginPath();
            ctx.moveTo(xPixel, yScale.top); // Top of the chart
            ctx.lineTo(xPixel, yScale.bottom); // Bottom of the chart
            ctx.lineWidth = 2;
            ctx.strokeStyle = line.color;
            ctx.stroke();
            ctx.restore();

            // Add label
            ctx.setLineDash([]); // Reset dash for label
            ctx.font = '12px Arial';
            ctx.fillStyle = line.color;
            ctx.textAlign = 'center';
            ctx.fillText(line.label, xPixel, yScale.top - 10); // Label above line
        });
    }
};

// Update the RUL chart with JSON data (no need to parse with parseData)
function updateRulChart(data, bdIndex, eolIndex) {
    const ctx = document.getElementById('rulChart').getContext('2d');

    if (rulChart) rulChart.destroy();

    //const bdIndex = data.bd.findIndex(value => value !== 0);
    //const eolIndex = data.eol.findIndex(value => value !== 0);

    rulChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [
                {
                    label: 'Remaining Useful Life (RUL)',
                    data: data.rul,
                    borderColor: 'rgb(255, 165, 0)',
                    tension: 0.1,
                    fill: false,
                    pointRadius: 0
                },
                {
                    label: 'Prognostic Health (PH)',
                    data: data.ph,
                    borderColor: 'rgb(0, 150, 136)',
                    tension: 0.1,
                    fill: false,
                    pointRadius: 0
                }
            ],
            bdIndex: bdIndex,
            eolIndex: eolIndex
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'RUL/PH [AU]' } }
            },
            plugins: {
                zoom: zoomOptions
            }
        },
        plugins: [{
            id: 'dynamicAnnotationPlugin',
            beforeDraw: (chart) => {
                const ctx = chart.ctx;
                const xScale = chart.scales.x;
                const yScale = chart.scales.y;
        
                const bdIndex = chart.data.bdIndex;
                const eolIndex = chart.data.eolIndex;
        
                if (bdIndex !== null && bdIndex >= 0) {
                    const xPixel = xScale.getPixelForValue(chart.data.labels[bdIndex]);
                    const yPixel = yScale.getPixelForValue(chart.data.datasets[0].data[bdIndex]);
                    ctx.save();
                    ctx.beginPath();
                    ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for BD
                    ctx.lineWidth = 2;
                    ctx.strokeStyle = 'green';
                    ctx.stroke();
                    ctx.restore();
                }
        
                if (eolIndex !== null && eolIndex >= 0) {
                    const xPixel = xScale.getPixelForValue(chart.data.labels[eolIndex]);
                    const yPixel = yScale.getPixelForValue(chart.data.datasets[0].data[eolIndex]);
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
            id: 'dynamicAnnotationPlugin',
            beforeDraw: (chart) => {
                const ctx = chart.ctx;
                const xScale = chart.scales.x;
                const yScale = chart.scales.y;
        
                const bdIndex = chart.data.bdIndex;
                const eolIndex = chart.data.eolIndex;
        
                if (bdIndex !== null && bdIndex >= 0) {
                    const xPixel = xScale.getPixelForValue(chart.data.labels[bdIndex]);
                    const yPixel = yScale.getPixelForValue(chart.data.datasets[1].data[bdIndex]);
                    ctx.save();
                    ctx.beginPath();
                    ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for BD
                    ctx.lineWidth = 2;
                    ctx.strokeStyle = 'green';
                    ctx.stroke();
                    ctx.restore();
                }
        
                if (eolIndex !== null && eolIndex >= 0) {
                    const xPixel = xScale.getPixelForValue(chart.data.labels[eolIndex]);
                    const yPixel = yScale.getPixelForValue(chart.data.datasets[1].data[eolIndex]);
                    ctx.save();
                    ctx.beginPath();
                    ctx.arc(xPixel, yPixel, 8, 0, 2 * Math.PI); // Circle for EOL
                    ctx.lineWidth = 2;
                    ctx.strokeStyle = 'red';
                    ctx.stroke();
                    ctx.restore();
                }
            }
        }]
    });
}


function updateSoHChart(data, bdIndex, eolIndex) {
    const ctx = document.getElementById('sohChart').getContext('2d');

    if (sohChart) sohChart.destroy();

    //const bdIndex = data.bd.findIndex(value => value !== 0);
    //const eolIndex = data.eol.findIndex(value => value !== 0);

    sohChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [{
                label: 'State-of-Health (SoH)',
                data: data.soh,
                borderColor: 'rgb(153, 102, 255)',
                tension: 0.1,
                fill: false,
                pointRadius: 0
            }],
            bdIndex: bdIndex,
            eolIndex: eolIndex
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'SoH [%]' } }
            },
            plugins: {
                zoom: zoomOptions
            }
        },
        plugins: [annotationPlugin]
    });
}


function updateFDChart(data, bdIndex, eolIndex) {
    const ctx = document.getElementById('fdChart').getContext('2d');

    if (fdChart) fdChart.destroy();

    // Ensure vertical lines are updated with correct `x` values
    verticalLines[0].x = eolIndex >= 0 ? data.time[eolIndex] : null;
    verticalLines[1].x = bdIndex >= 0 ? data.time[bdIndex] : null;

    // Clean BD and EOL arrays for robustness
    const cleanBd = data.bd.map(value => Number(value)).filter(value => !isNaN(value));
    const cleanEol = data.eol.map(value => Number(value)).filter(value => !isNaN(value));

    // Dynamically find the BD and EOL indices
    const fdBdIndex = cleanBd.findIndex(value => value !== -1);
    const fdEolIndex = cleanEol.findIndex(value => value !== 0);


    if (fdBdIndex >= 0) verticalLines[1].x = data.time[fdBdIndex]; // Update BD line
    if (fdEolIndex >= 0) verticalLines[0].x = data.time[fdEolIndex]; // Update EOL line

    console.log("Updated Vertical Lines for FD:", verticalLines);

    fdChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.time,
            datasets: [{
                label: 'Feature Data (FD)',
                data: data.fd,
                borderColor: 'rgb(255, 51, 135)',
                tension: 0.1,
                fill: false,
                pointRadius: 0,
                pointBackgroundColor: (context) => {
                    if (context.dataIndex === fdEolIndex) return 'red';
                    if (context.dataIndex === fdBdIndex) return 'green';
                    return 'transparent'; 
                },
                pointBorderWidth: (context) => {
                    if (context.dataIndex === fdEolIndex || context.dataIndex === fdBdIndex) return 1;
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
                zoom: zoomOptions
            }
        },
        plugins: [verticalLinePlugin]
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
                borderColor: 'rgb(0, 204, 204)',
                tension: 0.1,
                fill: false,
                pointRadius: 0,
                pointBackgroundColor: 'transparent',
                pointBorderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: { title: { display: true, text: 'Time (MS)' } },
                y: { title: { display: true, text: 'Voltage (V)' } }
            },
            plugins: {
                zoom: zoomOptions
            }
        },
        plugins: [annotationPlugin]
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
            chart.resize(); // Force resize
        }
    });
}

// Attach resize event listener
window.addEventListener('resize', () => {
    adjustCharts();
});

// Load devices on page load
window.onload = loadDevices;
