function showGraphsForDevice(device) {
    fetch(`/data/${device}/voltageData.csv`)
        .then(response => response.json())
        .then(data => updateVoltageChart(data));

    fetch(`/data/${device}/rulData.csv`)
        .then(response => response.json())
        .then(data => updateRulChart(data));

    fetch(`/data/${device}/fdData.csv`) // Fetch FD data
        .then(response => response.json())
        .then(data => updateGraph3Chart(data));

    fetch(`/data/${device}/sohData.csv`) // Fetch SoH data
        .then(response => response.json())
        .then(data => updateGraph4Chart(data));
}
