        // Fetch health data from the Flask server
        async function fetchHealthData() {
            const response = await fetch('/get_health_data');
            if (!response.ok) {
                console.error('Failed to fetch health data');
                return;
            }
            const data = await response.json();
            plotHealthData(data);
        }

        // Plot the health data using Chart.js
        function plotHealthData(data) {
            const ctx = document.getElementById('healthChart').getContext('2d');
            const healthChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.timestamps,
                    datasets: [
                        {
                            label: 'Health Metric 1',
                            data: data.health_metric_1,
                            borderColor: 'rgb(75, 192, 192)',
                            fill: false,
                            tension: 0.1
                        },
                        {
                            label: 'Health Metric 2',
                            data: data.health_metric_2,
                            borderColor: 'rgb(255, 99, 132)',
                            fill: false,
                            tension: 0.1
                        }
                    ]
                },
                options: {
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Timestamp'
                            },
                            type: 'time',  // Enable time scale if timestamps are in date format
                            time: {
                                unit: 'minute'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Health Metric Value'
                            }
                        }
                    }
                }
            });
        }

        // Load the health data when the page is loaded
        window.onload = fetchHealthData;
