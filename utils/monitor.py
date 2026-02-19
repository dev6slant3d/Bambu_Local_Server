import time
import threading
import bambulabs_api as bl
import atexit
from jsonc_parser.parser import JsoncParser

data_dump = []
printers = []

heartbeat_active = False

def load_printers():
    """Load printer information from printerData.jsonc."""
    global printers

    file_path = "./printerData.jsonc"
    printerData = JsoncParser.parse_file(file_path)
    for serial, details in printerData.items():
        printer = {}

        hostname, access_code, has_camera = details
        object = bl.Printer(hostname, access_code, serial)
        atexit.register(object.disconnect)
        object.connect()
        print("Connecting to printer %s...", serial)
        time.sleep(2)

        printer["serial"] = serial
        printer["has_camera"] = has_camera
        printer["object"] = object
        printers.append(printer)
    
    start_heartbeat()


def start_heartbeat():
    """Initiate printer heartbeats."""
    global heartbeat_active
    
    heartbeat_active = True
    threading.Thread(target=data_heartbeat, daemon=True).start()
    threading.Thread(target=camera_heartbeat, daemon=True).start()


def stop_heartbeat():
    """Stop heartbeats."""
    global heartbeat_active
    
    heartbeat_active = False


def data_heartbeat():
    """Continuously fetch printer information using bambu API."""
    global data_dump
    global printers
    global heartbeat_active

    while heartbeat_active:
        for printer in printers:
            dump = {}
            try:
                dump["serial"] = printer["serial"]
                dump["file"] = printer["object"].gcode_file()
                dump["status"] = printer["object"].get_state()
                dump["percentage"] = printer["object"].get_percentage()
                dump["layer_num"] = printer["object"].current_layer_num()
                dump["total_layer_num"] = printer["object"].total_layer_num()
                dump["bed_temperature"] = printer["object"].get_bed_temperature()
                dump["nozzle_temperature"] = printer["object"].get_nozzle_temperature()
                dump["remaining_time"] = printer["object"].get_time()
                
                index = getPrinterDataDumpIndex(printer["serial"])
                if index == -1:
                    data_dump.append(dump)
                else:
                    data_dump[index] = dump
            except Exception as e:
                print("Error fetching printer data: ", e)
            time.sleep(1)


def camera_heartbeat():
    """Continuously fetch camera images at 1 FPS."""
    global printers
    global data_dump
    global heartbeat_active

    while heartbeat_active:
        for printer in printers:
            if printer["has_camera"] == True:
                try:              
                    latest_frame = printer.get_camera_image()
                    index = getPrinterDataDumpIndex(printer["serial"])
                    if index != -1:
                        updatedDump = data_dump[index]
                        updatedDump["latest_frame"] = latest_frame
                        data_dump[index] = updatedDump
                except Exception as e:
                    print("Error fetching camera image: ", e)
            time.sleep(1)  # 1 FPS


def getPrinterDataDumpIndex(serial):
    """Reusable helper function to get latest data dump of printer."""
    global data_dump

    for i in range(len(data_dump)):
        if data_dump[i]["serial"] == serial:
            return i
    
    return -1

def getPrinterIndex(serial):
    """Reusable helper function to get printer index."""
    global printers

    for i in range(len(printers)):
        if printers[i]["serial"] == serial:
            return i
    
    return -1


def toggle_light(serial):
    """Toggle the printer light and return its new state."""
    global printers
    
    index = getPrinterIndex(serial)
    if index == -1:
        return

    printer = printers[index]["object"]
    light_state = printer.get_light_state()

    if light_state == 'on':
        print('[TOGGLING PRINTER LIGHT OFF]')
        printer.turn_light_off()
    else:
        print('[TOGGLING PRINTER LIGHT ON]')
        printer.turn_light_on()
    
    return light_state


def main():
    load_printers()


if __name__ == "__main__":
    main()