function updateStatsAndTable(data) {
    const devices = data.devices || [];
    const total = devices.length;
    const online = devices.filter(d => d.status === "online").length;
    const offline = total - online;
    const unknown = devices.filter(d => d.type === "Unknown").length;

    const setText = (id, value) => {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    };

    setText("stat-total", total);
    setText("stat-online", online);
    setText("stat-offline", offline);
    setText("stat-unknown", unknown);

    const tbody = document.getElementById("devices-body");
    if (!tbody) return;

    tbody.innerHTML = "";
    devices.forEach(d => {
        const tr = document.createElement("tr");
        tr.className = "row-status-" + d.status;

        const cells = [
            d.ip,
            d.type,
            d.status,
            d.title || "",
            d.last_seen || "-",
        ];

        cells.forEach(text => {
            const td = document.createElement("td");
            td.textContent = text;
            tbody.appendChild(tr);
            tr.appendChild(td);
        });

        const tdActions = document.createElement("td");

        const aWeb = document.createElement("a");
        aWeb.href = "http://" + d.ip;
        aWeb.target = "_blank";
        aWeb.className = "btn btn-small";
        aWeb.textContent = "Web UI";

        const btnApi = document.createElement("button");
        btnApi.className = "btn btn-small btn-secondary";
        btnApi.textContent = "API";
        btnApi.dataset.ip = d.ip;
        btnApi.dataset.action = "api";

        const aDetails = document.createElement("a");
        aDetails.href = "/device/" + encodeURIComponent(d.ip);
        aDetails.className = "btn btn-small btn-outline";
        aDetails.textContent = "Details";

        tdActions.appendChild(aWeb);
        tdActions.appendChild(btnApi);
        tdActions.appendChild(aDetails);

        tr.appendChild(tdActions);
    });
}

function fetchDevices() {
    fetch("/devices")
        .then(r => r.json())
        .then(data => {
            updateStatsAndTable(data);
        })
        .catch(err => {
            console.error("Failed to fetch devices", err);
        });
}

function setupAutoRefresh() {
    fetchDevices();
    setInterval(fetchDevices, 5000);
}

function setupManualScan() {
    const btn = document.getElementById("btn-manual-scan");
    if (!btn) return;
    btn.addEventListener("click", () => {
        btn.disabled = true;
        btn.textContent = "Scanning...";
        fetch("/scan")
            .then(r => r.json())
            .then(() => {
                fetchDevices();
            })
            .finally(() => {
                btn.disabled = false;
                btn.textContent = "Manual Scan";
            });
    });
}

function setupApiModal() {
    const backdrop = document.getElementById("modal-backdrop");
    const closeBtn = document.getElementById("modal-close");
    const content = document.getElementById("modal-content");

    if (!backdrop || !closeBtn || !content) return;

    const close = () => {
        backdrop.hidden = true;
    };

    closeBtn.addEventListener("click", close);
    backdrop.addEventListener("click", (e) => {
        if (e.target === backdrop) close();
    });

    document.addEventListener("click", (e) => {
        const target = e.target;
        if (!(target instanceof HTMLElement)) return;
        if (target.dataset && target.dataset.action === "api") {
            const ip = target.dataset.ip;
            backdrop.hidden = false;
            content.textContent = "Loading...";
            fetch(`/api/miner?ip=${encodeURIComponent(ip)}`)
                .then(r => r.json())
                .then(data => {
                    content.textContent = JSON.stringify(data, null, 2);
                })
                .catch(err => {
                    content.textContent = "Error: " + err;
                });
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    setupAutoRefresh();
    setupManualScan();
    setupApiModal();
});
