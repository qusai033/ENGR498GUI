from flask import Flask, jsonify, render_template, request, abort
import pandas as pd
import os

app = Flask(__name__)

# Path to the directory containing device folders
DATA_DIRECTORY = '../data'  # Relative path to the data folder

@app.route('/')
def index():
    return render_template('index.html')



# Upload file route
@app.route('/upload', methods=['POST'])
def upload():
        # Get the uploaded file content from the request
        file = request.data  # This will capture the raw data sent by the Arduino

        # Save the file to the specified path
        file_path = os.path.join(DATA_DIRECTORY, "uploaded_file.csv")
        with open('data_received.csv', "wb") as f:  # Write the file content in binary mode
            f.write(file)
        
        return "File uploaded successfully", 200

    

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
        required_columns = ['DT', 'RUL', 'FD', 'SOH']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return abort(400, description=f"Missing columns: {', '.join(missing_columns)}")
        
        # Prepare JSON response
        data = {
            "time": df['DT'].tolist(),
            "rul": df['RUL'].tolist(),
            "fd": df['FD'].tolist(),
            "soh": df['SOH'].tolist()
        }
        return jsonify(data)
    except Exception as e:
        print("Error:", e)  # Debug error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)






let voltageChart = null;  // Declare chart globally so it can be destroyed later
let rulChart = null;  // Declare a global variable for the RUL (health) chart
let allDevices = [];  // Store the list of all devices for filtering


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
            updateSohChart(data);  // SoH Chart
            updateFdChart(data);   // FD Chart
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
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: 'RUL [AU]' } }
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
    const ctx = document.getElementById('fdChart').getContext('2d');

    if (fdChart) fdChart.destroy();

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
        }
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

// Function to filter devices based on search input
function filterDevices() {
    const query = document.getElementById('deviceSearch').value.toLowerCase();
    const filteredDevices = allDevices.filter(device => device.toLowerCase().includes(query));
    displayDevices(filteredDevices); // Display the filtered devices
}

// Load devices on page load
window.onload = loadDevices;









<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Graph Layout</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@1.0.0-beta.10"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@1.2.1"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom.min.js"></script>

</head>
<body>

    <!-- Header with Logos -->
    <div class="header">
        <img src="{{ url_for('static', filename='logo1.png') }}" alt="Logo 1">
        <img src="{{ url_for('static', filename='logo2.png') }}" alt="Logo 2">
        <img src="{{ url_for('static', filename='logo3.png') }}" alt="Logo 3">
    </div>

    <!-- Nav Buttons -->
    <div class="content">
        <div class="sidebar">
            <button class="nav-button" onclick="showGraphsForDevice('Device1')">Home</button>
            

            <!-- Devices Dropdown -->
            <div class="dropdown">
                <button class="nav-button">Devices</button>
                <div class="dropdown-content">
                    <!-- Search box -->
                    <input type="text" id="deviceSearch" class="search-input" placeholder="Search devices..." onkeyup="filterDevices()">
                    <!-- List of devices -->
                    <div class="device-list" id="searchResults"></div>
                </div>
            </div>
            <button class="nav-button" onclick="resetZoom()">Reset Zoom</button>
        </div>

        <!-- Graphs -->
        <div class="graphs-grid">
            <!-- Graph 1 -->
            <div class="graph" id="voltage-graph">
                <h2 id="voltage-title">Voltage Decay</h2>
                <canvas id="voltageChart"></canvas>
            </div>
        
            <!-- Graph 2 -->
            <div class="graph" id="capacitor-health-graph">
                <h2 id="capacitor-title">Remaining Useful Life (RUL)</h2>
                <canvas id="rulChart"></canvas>
            </div>
        
            <!-- Graph 3 -->
            <div class="graph" id="state-of-Heath-graph">
                <h2 id="soh-title">State-of-Health</h2>
                <canvas id="sohChart"></canvas>
            </div>
        
            <!-- Graph 4 -->
            <div class="graph" id="feature-data-graph">
                <h2 id="fd-title">Feature Data</h2>
                <canvas id="fdChart"></canvas>
            </div>
        </div>

    <div class="footer">
        <p>Legend: Explain data here.</p>
    </div>

    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>




















