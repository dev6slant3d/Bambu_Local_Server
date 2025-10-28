# Bambu Local Server

A lightweight **local web dashboard** and **API controller** for **Bambu Lab 3D printers**, built with **Flask**, **Socket.IO**, and **bambulabs_api**.
It enables **real-time monitoring**, **camera streaming**, and **direct printer control**,  all without Bambu’s cloud services.

---

## Overview

**Bambu Local Server** runs entirely on your **local network** and communicates directly with your Bambu Lab printer using the **LAN mode API**.

It collects telemetry (temperatures, progress, job info), retrieves live camera images, and exposes this data through a **real-time web interface** built with Flask and Socket.IO.

You can view your printer’s status and camera feed from a browser and even toggle the printer light,  all locally, without any external servers.

---

## Features

| Feature               | Description                                                                         |
| --------------------- | ----------------------------------------------------------------------------------- |
| **Local Connection**  | Connects to your Bambu printer over LAN using its hostname, serial, and access code |
| **Live Printer Data** | Tracks print progress, layer info, bed & nozzle temperatures, remaining time        |
| **Camera Streaming**  | Captures live printer images (1 frame per second)                                   |
| **Light Control**     | Toggle the printer’s light directly from the web UI                                 |
| **WebSocket Updates** | Real-time updates to the browser without page reloads                               |
| **Modular Codebase**  | Clean separation between hardware access, encoding, and web serving                 |

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SteelCantSpeak/Bambu_Local_Server.git
cd Bambu_Local_Server
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```ini
HOSTNAME=192.168.1.42
ACCESS_CODE=your_printer_access_code
SERIAL=your_printer_serial
```

**Tip:** You can find these values in the Bambu Handy app or your printer’s LAN settings.
Make sure **LAN Mode** is enabled on your printer.

---

## Running the Server

Start the Flask app:

```bash
python app.py
```

Then open your browser and go to:

```
http://<your-computer-ip>:5000
```

(Also available [here](http://127.0.0.1:5000/))
You’ll see a simple dashboard showing:

* Live camera image (updated every 2 seconds)
* Real-time print data (progress, temps, etc.)
* A **“Toggle Light”** button to control the printer’s onboard light

---

## Project Structure

```
Bambu_Local_Server/
├── app.py                 # Main Flask + Socket.IO web server
├── utils/
│   ├── monitor.py         # Handles printer connection and data collection
│   └── encoder.py         # Converts images to base64 (JPEG)
├── templates/
│   └── index.html         # Web dashboard UI
├── static/                # JS/CSS for frontend (optional)
├── .env                   # Printer credentials (not committed)
└── requirements.txt
```

## Dependencies

| Library                                                    | Purpose                                  |
| ---------------------------------------------------------- | ---------------------------------------- |
| `Flask`                                                    | Serves web pages and API endpoints       |
| `Flask-SocketIO`                                           | Real-time client updates via WebSocket   |
| [`bambulabs_api`](https://pypi.org/project/bambulabs-api/) | Direct communication with the printer    |
| `python-dotenv`                                            | Securely load `.env` printer credentials |
| `Pillow`                                                   | Image handling and JPEG conversion       |
| `numpy`                                                    | Image array manipulation                 |

Install them all with:

```bash
pip install -r requirements.txt
```

---

## Security Notes

* Keep your `.env` file private,  it contains your printer credentials.
* Use this server **only on trusted local networks**.
* If you expose it beyond LAN, enable HTTPS and user authentication.

---

## Future Enhancements

* RESTful API for extended printer commands (pause, resume, queue)
* Multi-printer dashboard
* Authentication for secure web access
* Historical data logging
* Docker deployment for one-command setup

---

## Disclaimer

This is an **unofficial** open-source project, not affiliated with **Bambu Lab**.
Use responsibly and at your own risk. Ensure your printer supports and has **LAN Mode** enabled.

---

## License

Licensed under the **MIT License**.
See [LICENSE](./LICENSE) for details.

---
