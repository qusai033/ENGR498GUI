function fetchAndPlotData(device) {
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
