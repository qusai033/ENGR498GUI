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


function fetchAndPlotData(device) {


    fetch(`/data/${device}/voltageData.csv`)
        .then(response => {
            if(!response.ok){
                throw new Error('Voltage not found');
            }
            return response.json();
        })
        .then(data => {
            updateVoltageChart(data);
        })
        .catch(error => console.error('Error loading voltage data:', error));

    // Fetch data from the Flask endpoint
    fetch(`/data/${device}/rulData.csv`)
      .then(response => response.json())
      .then(data => {
        // Log data for debugging
        console.log("Fetched data:", data);

        // Ensure data is not empty
        if (!data.time || data.time.length === 0) {
          console.error("No time data available!");
          return;
        }

        // Plot each chart
        plotChart('rulChart', 'Remaining Useful Life (RUL)', data.time, data.rul, 'rgb(255, 99, 132)');
        plotChart('fdChart', 'Feature Data (FD)', data.time, data.fd, 'rgb(54, 162, 235)');
        plotChart('sohChart', 'State of Health (SoH)', data.time, data.soh, 'rgb(75, 192, 192)');
      })
      .catch(error => console.error('Error fetching or plotting data:', error));
}

function plotChart(chartId, label, time, dataset, color) {
    const ctx = document.getElementById(chartId).getContext('2d');
    
    // Check if the chart element exists
    if (!ctx) {
      console.error(`Chart element with ID ${chartId} not found!`);
      return;
    }

    // Create the chart
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: time, // Time as the x-axis
            datasets: [
              {
                label: label, // Chart label (e.g., RUL, FD, SoH)
                data: dataset, // Corresponding data array
                borderColor: color,
                fill: false,
                tension: 0.1
              }
            ]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time [AU]' } },
                y: { title: { display: true, text: label } }
            },
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'xy'
                    },
                    zoom: {
                        wheel: { enabled: true },
                        pinch: { enabled: true },
                        mode: 'xy'
                    }
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


// Utility function to parse text data into a format usable by the chart
function parseData(data) {
    const lines = data.split('\n');
    const labels = [];
    const values = [];

    lines.forEach(line => {
        const [label, value] = line.includes(';') ? line.split(';') : line.split(',');
        if (label && value) {  // Ensure both label and value exist
            labels.push(label.trim());
            values.push(parseFloat(value.trim()));
        }
    });

    return { labels, values };
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
            fetchAndPlotData(device); // Load graphs when clicking on a device
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
        required_columns = ['DT', 'RUL', 'FD', 'SoH']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return abort(400, description=f"Missing columns: {', '.join(missing_columns)}")
        
        # Prepare JSON response
        data = {
            "time": df['DT'].tolist(),
            "rul": df['RUL'].tolist(),
            "fd": df['FD'].tolist(),
            "soh": df['SoH'].tolist()
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
