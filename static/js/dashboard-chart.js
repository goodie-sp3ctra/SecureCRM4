// static/js/dashboard-chart.js
// —no need for TS or fancy template tags here—just normal JS—

(function () {
    // fetch the JSON blob from the page
    const raw = document.getElementById('chart-data').textContent;
    const chartData = JSON.parse(raw);

    // now you have chartData.labels and chartData.values
    const ctx = document.getElementById('stageChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Jobs by Status',
                data: chartData.values,
                backgroundColor: 'rgba(0,123,255,0.5)',
                borderColor: 'rgba(0,123,255,1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: { y: { beginAtZero: true } }
        }
    });
})();
