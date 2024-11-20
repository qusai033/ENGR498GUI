function showGraphsForDevice(device) {
    // Fetch and update data for all four graphs
    fetch(`/data/${device}/voltageData.csv`)
        .then(response => response.json())
        .then(data => updateVoltageChart(data));

    fetch(`/data/${device}/rulData.csv`)
        .then(response => response.json())
        .then(data => updateRulChart(data));

    fetch(`/data/${device}/graph3Data.csv`) // Replace with actual endpoint
        .then(response => response.json())
        .then(data => updateGraph3Chart(data));

    fetch(`/data/${device}/graph4Data.csv`) // Replace with actual endpoint
        .then(response => response.json())
        .then(data => updateGraph4Chart(data));
}
