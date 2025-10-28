import time
import threading
import bambulabs_api as bl
from dotenv import load_dotenv
import os
import datetime
import atexit

# Load environment variables
load_dotenv()

hostname = os.getenv('HOSTNAME')
access_code = os.getenv('ACCESS_CODE')
serial = os.getenv('SERIAL')

latest_frame = None
data_dump = {}

printer = None
printer_ready = threading.Event()  # Signal when printer is ready
light_state = False  # Track current light state locally


def toggle_light():
    """Toggle the printer light and return its new state."""
    global printer, light_state
    if printer is None:
        raise RuntimeError("Printer not initialized yet")

    if light_state:
        printer.turn_light_off()
        light_state = False
    else:
        printer.turn_light_on()
        light_state = True
    return light_state


def camera_loop():
    """Continuously fetch camera images at 1 FPS."""
    global latest_frame
    global data_dump
    while True:
        if printer_ready.is_set():
            try:
                data_dump["file"] = printer.gcode_file()
                data_dump["status"] = printer.get_state()
                data_dump["percentage"] = printer.get_percentage()
                data_dump["layer_num"] = printer.current_layer_num()
                data_dump["total_layer_num"] = printer.total_layer_num()
                data_dump["bed_temperature"] = printer.get_bed_temperature()
                data_dump["nozzle_temperature"] = printer.get_nozzle_temperature()
                data_dump["remaining_time"] = printer.get_time()
                          
                latest_frame = printer.get_camera_image()
            except Exception as e:
                print("Error fetching camera image:", e)
        time.sleep(1)  # 1 FPS


def main():

    global printer
    printer = bl.Printer(hostname, access_code, serial)

    atexit.register(printer.disconnect)

    printer.connect()
    print("Connecting to printer...")
    time.sleep(5)  # Give time for the connection to establish

    printer_ready.set()  # Signal that printer is ready
    print("Printer ready. Camera streaming started.")

    # Start the camera loop in a separate thread
    threading.Thread(target=camera_loop, daemon=True).start()




if __name__ == "__main__":
    main()

    # Example usage: toggle the light every 0.5 seconds
    while True:
        time.sleep(0.5)
        new_state = toggle_light()
        print("Light is now", "ON" if new_state else "OFF")
