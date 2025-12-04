// Formatting timestamp
function formatTimestamp(ts) {
    const date = new Date(ts * 1000);
    return date.toLocaleTimeString();
}

// DOM Elements
const healthStatus = document.getElementById("health-status");
const healthUptime = document.getElementById("health-uptime");
const healthTimestamp = document.getElementById("health-timestamp");
const tbody = document.getElementById("status");

// Chart.js setup
const ctx = document.getElementById('latencyChart').getContext('2d');
const latencyChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // timestamps
        datasets: [{
            label: 'Latency (s)',
            data: [],
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            borderColor: 'rgba(59, 130, 246, 1)',
            borderWidth: 2,
            tension: 0.3,
            fill: true
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Fetch /health
async function fetchHealth() {
    const res = await fetch("http://localhost:8000/health");
    const data = await res.json();
    healthStatus.textContent = data.status;
    healthUptime.textContent = data.uptime_seconds.toFixed(2);
    healthTimestamp.textContent = new Date(data.timestamp*1000).toLocaleTimeString();

    // color box dynamically
    healthStatus.parentElement.className = `bg-${data.status==="ok"?"green":"red"}-100 shadow rounded p-4 text-center`;
}

// Fetch /status
async function fetchStatus() {
    const res = await fetch("http://localhost:8000/status");
    const logs = await res.json();
    tbody.innerHTML = "";

    // Update table and chart (latest on top)
    const reversed = logs.slice().reverse();
    latencyChart.data.labels = reversed.map(l => formatTimestamp(l.timestamp));
    latencyChart.data.datasets[0].data = reversed.map(l => l.latency);
    latencyChart.update();

    reversed.forEach(log => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td class="px-4 py-2">${log.url}</td>
            <td class="px-4 py-2 font-bold ${log.status === "UP" ? "text-green-600" : "text-red-600"}">${log.status}</td>
            <td class="px-4 py-2">${log.latency}</td>
            <td class="px-4 py-2">${formatTimestamp(log.timestamp)}</td>
        `;
        tbody.appendChild(row);
    });
}

// Fetch every 5s
setInterval(fetchHealth, 5000);
setInterval(fetchStatus, 5000);

// Initial fetch
fetchHealth();
fetchStatus();
