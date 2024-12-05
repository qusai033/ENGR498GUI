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
        .then(data => updateVoltageChart(data))
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

            // Clean BD and EOL arrays
            const cleanBd = data.bd.map(value => Number(value)).filter(value => !isNaN(value));
            const cleanEol = data.eol.map(value => Number(value)).filter(value => !isNaN(value));


            // Find BD and EOL indices
            const bdIndex = cleanBd.findIndex(value => value !== 0);
            const eolIndex = cleanEol.findIndex(value => value !== 0);


            if (bdIndex < 0 || eolIndex < 0) {
                console.warn("BD or EOL not found in the current dataset.");
                return;
            }

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
    const fdBdIndex = cleanBd.findIndex(value => value !== 0);
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



from flask import Flask, jsonify, render_template, request, abort
import pandas as pd
import os
from io import StringIO


app = Flask(__name__)


# Path to the directory containing device folders
DATA_DIRECTORY = '../data'  # Relative path to the data folder
# Upload file route
# Path to the directory containing device folders
# Path to the directory containing device folders
UPLOAD_DATA_DIRECTORY = './data/uploads/voltage_log'  # Update to match your directory structure
COUNTER_FILE_DIRECTORY = './data/uploads'  # File to store the counter

COUNTER_FILE = os.path.join(COUNTER_FILE_DIRECTORY, 'file_voltage_counter.txt')

# Ensure directories and counter file exist
os.makedirs(UPLOAD_DATA_DIRECTORY, exist_ok=True)
os.makedirs(COUNTER_FILE_DIRECTORY, exist_ok=True)

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, 'w') as f:
        f.write('0')  # Initialize the counter to 0


# Function to get the current counter value
def get_file_counter():
    with open(COUNTER_FILE, 'r') as f:
        return int(f.read().strip())


# Function to increment and save the counter
def increment_file_counter():
    counter = get_file_counter() + 1
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(counter))
    return counter



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Read raw CSV data from the request body
        csv_data = request.data.decode('utf-8')
        if not csv_data:
            print("Error: No data received.")  # Debug log
            return jsonify({"error": "No data received"}), 400
        

        # Convert CSV data into a Pandas DataFrame

        csv_stream = StringIO(csv_data)
        df = pd.read_csv(csv_stream)


        df.columns = df.columns.str.strip()

        # Ensure Time and Voltage columns are checked for duplicates
        if 'Voltage' not in df.columns or 'Time' not in df.columns:
            print("Error: Missing 'Time' or 'Voltage' columns.")  # Debug log
            return jsonify({"error": "Missing 'Time' or 'Voltage' columns in CSV"}), 400
        

        original_length = len(df)


        # Drop duplicates based on Time and Voltage
        df = df.drop_duplicates(subset=['Voltage', 'Time'])

        new_lenth = len(df)

        print(f"remove {original_length - new_lenth} duplicate rows.")

        # Increment the file counter and generate a unique filename
        file_counter = increment_file_counter()
        unique_filename = f"voltageDecay_{file_counter}.csv"

        # Save the uniquely named file in the uploads directory
        save_path = os.path.join(UPLOAD_DATA_DIRECTORY, unique_filename)
        df.to_csv(save_path, index=False)

        print(f"File saved to: {save_path}")  # Debug log


        # Traverse `data` directory to find all `voltageData.csv` files
        overridden_files = []
        for root, dirs, files in os.walk(DATA_DIRECTORY):  # Recursively walk through directories
            for file in files:
                if file == 'voltageData.csv':  # Check for `voltageData.csv`
                    file_path = os.path.join(root, file)
                    
                    # Override the file content with normalized data
                    df.to_csv(file_path, index=False)  # Save normalized DataFrame
                    overridden_files.append(file_path)
                    

        if not overridden_files:
            return jsonify({"message": "No voltageData.csv files found to override."}), 404

        print(f"Overridden files: {overridden_files}")  # Debug log
        return jsonify({
            "message": f"Overridden {len(overridden_files)} voltageData.csv files successfully.",
            "overridden_files": overridden_files
        }), 200
    

    except Exception as e:
        print(f"Error processing CSV: {e}")  # Debug log
        return jsonify({"error": f"Error processing CSV: {e}"}), 500



# Endpoint to list all devices (subdirectories in the DATA_DIRECTORY)
@app.route('/list_devices', methods=['GET'])
def list_devices():
    try:
        # List all directories (devices) within the DATA_DIRECTORY
        devices = [d for d in os.listdir(DATA_DIRECTORY) if os.path.isdir(os.path.join(DATA_DIRECTORY, d))]
        return jsonify(devices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    

# Endpoint to get voltage data for a specific device
@app.route('/data/<device>/voltageData.csv', methods=['GET'])
def get_voltage_data(device):
    file_path = os.path.join(DATA_DIRECTORY, device, 'voltageData.csv')
    
    if not os.path.exists(file_path):
        return abort(404, description="Voltage data file not found.")
    
    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Check if the necessary columns exist in the CSV
    if 'Time' not in df.columns or 'Voltage' not in df.columns:
        return abort(400, description="CSV file must contain 'Time' and 'Voltage' columns.")
    
    # Convert the DataFrame to a dictionary suitable for JSON
    data = {
        "time": df['Time'].tolist(),
        "voltage": df['Voltage'].tolist()
    }
    
    return jsonify(data)

@app.route('/data/<device>/rulData.csv', methods=['GET'])
def get_rul_fd_soh_data(device):
    file_path = os.path.join(DATA_DIRECTORY, device, 'rulData.csv')
    
    if not os.path.exists(file_path):
        return abort(404, description="RUL data file not found.")
    
    try:
        df = pd.read_csv(file_path)
        
        # Ensure all required columns exist
        required_columns = ['DT', 'RUL', 'PH', 'FD', 'SOH']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return abort(400, description=f"Missing columns: {', '.join(missing_columns)}")
        
        # Prepare JSON response
        data = {
            "time": df['DT'].tolist(),
            "rul": df['RUL'].tolist(),
            "ph": df['PH'].tolist(),
            "fd": df['FD'].tolist(),
            "eol": df['EOL'].tolist(),
            "bd": df['BD'].tolist(),
            "soh": df['SOH'].tolist()
        }
        return jsonify(data)
    except Exception as e:
        print("Error:", e)  # Debug error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


