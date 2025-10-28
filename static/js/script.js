const socket = io();
socket.on('update', (data) => {
    document.getElementById('data').innerHTML = `${Date()}`
    document.getElementById('mainer').innerHTML = `</p>
    <p>FILE: ${data.values["file"]}</p>
    <p>STATUS: ${data.values["status"]}</p>
    <p>% COMPLETE: ${data.values["percentage"]}%</p>
    <p>LAYER: ${data.values["layer_num"]}/${data.values["total_layer_num"]}</p>
    <p>BED TEMP: ${data.values["bed_temperature"]}</p>
    <p>NOZZLE TEMP: ${data.values["nozzle_temperature"]}</p>
    <p>REMAINING TIME: ${formatTime(data.values["remaining_time"])}</p>
    `
    document.getElementById("latest").src = 'data:image/jpeg;base64,' + data.image;
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

function light() {
    fetch('/set_light', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: "empty"
    }).then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // Parse the response as JSON
    })
        .then(data => {
            console.log("Fetched data:", data); // Print the parsed data
            const button = document.getElementById("light_switch")
            if (data.value) {
                button.classList.add('lighton')
                if (button.classList.contains('lightoff')) {
                    button.classList.remove('lightoff');
                }
            } else {
                button.classList.add('lightoff')
                if (button.classList.contains('lighton')) {
                    button.classList.remove('lighton');
                }
            }
        })
        .catch(error => {
            console.error("Error during fetch operation:", error); // Handle any errors
        });
}



// Send a new value to the server
function updateValue() {
    var val = document.getElementById("valueInput").value;
    fetch('/set_value', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'value=' + val
    });
}