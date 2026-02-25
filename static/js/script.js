const socket = io();
socket.on('update', (data) => {
    document.getElementById('data').innerHTML = `${Date()}`
    document.getElementById('mainer').innerHTML = data.map(printer => `
        <div class="card">
        <h3>Printer: ${printer.serial}</h3>
        <p>FILE: ${printer.file}</p>
        <p>STATUS: ${printer.status}</p>
        <p>PRINT STATUS: ${printer.print_status}</p>
        <p>% COMPLETE: ${printer.percentage}%</p>
        <p>LAYER: ${printer.layer_num}/${printer.total_layer_num}</p>
        <p>BED TEMP: ${printer.bed_temperature}°C</p>
        <p>NOZZLE TEMP: ${printer.nozzle_temperature}°C</p>
        <p>REMAINING TIME: ${formatTime(printer.remaining_time)}</p>
        <div class="card-buttons">
            <button onclick="light('${printer.serial}')">Light</button>
        </div>
    </div>
    `).join('');
});

function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    return [
        hours.toString().padStart(2, '0'),
        minutes.toString().padStart(2, '0'),
        secs.toString().padStart(2, '0')
    ].join(':');
}

function light(serial) {
    fetch(`/set_light/${serial}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: "empty"
    }).then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // Parse the response as JSON
    })
        .catch(error => {
            console.error("Error during fetch operation:", error); // Handle any errors
        });
}