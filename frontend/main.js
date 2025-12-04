// -------------------------------
// DOM Elements
// -------------------------------
const healthStatus = document.getElementById("health-status");
const healthUptime = document.getElementById("health-uptime");
const healthTimestamp = document.getElementById("health-timestamp");
const tbody = document.getElementById("status");

// -------------------------------
// Chart.js Setup
// -------------------------------
const ctx = document.getElementById('latencyChart').getContext('2d');
const latencyChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // timestamps
        datasets: []
    },
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                enabled: true,
                callbacks: {
                    label: ctx => `${ctx.dataset.label}: ${ctx.raw.y}s`
                }
            },
            legend: {
                display: true,
                position: 'bottom'
            }
        },
        scales: { y: { beginAtZero: true } }
    }
});

// -------------------------------
// Helper Functions
// -------------------------------
function formatTimestamp(ts) {
    const date = new Date(ts * 1000);
    return date.toLocaleTimeString();
}

let lastStatus = {};

function flashRow(row, color) {
    row.style.transition = "background-color 0.3s";
    row.style.backgroundColor = color;
    setTimeout(() => { row.style.backgroundColor = "" }, 500);
}

// -------------------------------
// Fetch Health
// -------------------------------
async function fetchHealth() {
    try {
        const res = await fetch("http://localhost:8000/health");
        const data = await res.json();

        healthStatus.textContent = data.status;
        healthUptime.textContent = data.uptime_seconds.toFixed(2);
        healthTimestamp.textContent = new Date(data.timestamp*1000).toLocaleTimeString();

        // Change health box color dynamically
        healthStatus.parentElement.className = `bg-${data.status==="ok"?"green":"red"}-100 shadow rounded p-4 text-center`;
    } catch (error) {
        console.error("Error fetching health:", error);
    }
}

// -------------------------------
// Fetch Status Logs (Multi-URL)
// -------------------------------
async function fetchStatus() {
    try {
        const res = await fetch("http://localhost:8000/status");
        const logs = await res.json();

        tbody.innerHTML = "";

        const reversed = logs.slice().reverse();
        let chartDatasets = {};
        const colors = ["rgba(59, 130, 246, 1)", "rgba(16, 185, 129, 1)", "rgba(239, 68, 68, 1)", "rgba(234, 179, 8, 1)"];

        // Build datasets per URL
        reversed.forEach(log => {
            // Table row
            const row = document.createElement("tr");
            const prev = lastStatus[log.url];
            row.innerHTML = `
                <td class="px-4 py-2">${log.url}</td>
                <td class="px-4 py-2 font-bold ${log.status === "UP" ? "text-green-600" : "text-red-600"}">${log.status}</td>
                <td class="px-4 py-2">${log.latency}</td>
                <td class="px-4 py-2">${formatTimestamp(log.timestamp)}</td>
            `;
            if(prev && prev !== log.status) {
                flashRow(row, log.status === "UP" ? "lightgreen" : "tomato");
            }
            lastStatus[log.url] = log.status;
            tbody.appendChild(row);

            // Chart dataset
            if(!chartDatasets[log.url]) {
                const color = colors[Object.keys(chartDatasets).length % colors.length];
                chartDatasets[log.url] = {
                    label: log.url,
                    data: [],
                    borderColor: color,
                    backgroundColor: color.replace("1)", "0.2)"),
                    tension: 0.3
                };
            }
            chartDatasets[log.url].data.push({x: formatTimestamp(log.timestamp), y: log.latency});
        });

        // Update chart
        latencyChart.data.labels = [...new Set(reversed.map(l => formatTimestamp(l.timestamp)))];
        latencyChart.data.datasets = Object.values(chartDatasets);
        latencyChart.update();

    } catch (error) {
        console.error("Error fetching status:", error);
    }
}

// -------------------------------
// Auto-refresh every 5 seconds
// -------------------------------
setInterval(fetchHealth, 5000);
setInterval(fetchStatus, 5000);

// Initial fetch
fetchHealth();
fetchStatus();
