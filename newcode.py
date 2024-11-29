let resizeTimeout;

window.addEventListener('resize', () => {
    // Throttle resize events to avoid excessive calls
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        if (voltageChart) {
            const voltageData = voltageChart.data; // Preserve data
            const voltageOptions = voltageChart.options; // Preserve options
            voltageChart.destroy();
            const ctx = document.getElementById('voltageChart').getContext('2d');
            voltageChart = new Chart(ctx, {
                type: 'line',
                data: voltageData,
                options: voltageOptions
            });
        }
        if (rulChart) {
            const rulData = rulChart.data;
            const rulOptions = rulChart.options;
            rulChart.destroy();
            const ctx = document.getElementById('rulChart').getContext('2d');
            rulChart = new Chart(ctx, {
                type: 'line',
                data: rulData,
                options: rulOptions
            });
        }
        if (sohChart) {
            const sohData = sohChart.data;
            const sohOptions = sohChart.options;
            sohChart.destroy();
            const ctx = document.getElementById('sohChart').getContext('2d');
            sohChart = new Chart(ctx, {
                type: 'line',
                data: sohData,
                options: sohOptions
            });
        }
        if (fdChart) {
            const fdData = fdChart.data;
            const fdOptions = fdChart.options;
            fdChart.destroy();
            const ctx = document.getElementById('fdChart').getContext('2d');
            fdChart = new Chart(ctx, {
                type: 'line',
                data: fdData,
                options: fdOptions
            });
        }
    }, 300); // Adjust delay as needed for smoother performance
});
