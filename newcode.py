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
                <h2 id="graph3-title">State-of-Health</h2>
                <canvas id="sohChart"></canvas>
            </div>
        
            <!-- Graph 4 -->
            <div class="graph" id="feature-data-graph">
                <h2 id="graph4-title">Feature Data</h2>
                <canvas id="fdChart"></canvas>
            </div>
        </div>

    <div class="footer">
        <p>Legend: Explain data here.</p>
    </div>

    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
