import time
import threading
import bambulabs_api as bl
import atexit
from jsonc_parser.parser import JsoncParser
from io import BytesIO
import zipfile
import os

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

        IP, access_code, has_camera = details
        object = bl.Printer(IP, access_code, serial)
        atexit.register(object.disconnect)
        object.connect()
        print("Connecting to printer: ", serial)
        time.sleep(5)
        print("PRINTER READY: ", serial)

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
                dump["print_status"] = str(printer["object"].get_current_state())
                dump["percentage"] = printer["object"].get_percentage()
                dump["layer_num"] = printer["object"].current_layer_num()
                dump["total_layer_num"] = printer["object"].total_layer_num()
                dump["bed_temperature"] = printer["object"].get_bed_temperature()
                dump["nozzle_temperature"] = printer["object"].get_nozzle_temperature()
                dump["print_speed"] = printer["object"].get_print_speed()
                dump["remaining_time"] = printer["object"].get_time()
                dump["error_code"] = printer["object"].print_error_code()
                
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
                    latest_frame = printer["object"].get_camera_image()
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


def create_zip_archive_in_memory(text_content: str, text_file_name: str = 'file.txt') -> BytesIO:
    """
    Create a zip archive in memory

    Args:
        text_content (str): content of the text file
        text_file_name (str, optional): location of the text file.
            Defaults to 'file.txt'.

    Returns:
        io.BytesIO: zip archive in memory
    """

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(text_file_name, text_content)
    zip_buffer.seek(0)
    return zip_buffer


def handle_command(data):
    """Handle a printer command."""
    global printers

    print('Received command:', data)

    type = data["type"]
    serial = data["serial"]
    filepath = data["filepath"]

    index = getPrinterIndex(serial)
    if index == -1:
        return
    
    printer = printers[index]["object"]

    if type == 'startPrint':
        start_print(printer, filepath)
    elif type == 'pausePrint':
        pause_print(printer)
    elif type == 'resumePrint':
        resume_print(printer)
    elif type == 'stopPrint':
        stop_print(printer)


def start_print(printer, filepath):
    """Start print on printer."""

    filename = os.path.basename(filepath)
    path = filepath
    while True:
        try:
            with open(path, "r") as file:
                gcode = file.read()
            break
        except FileNotFoundError:
            if path.startswith('..\\'):
                path = path[3:]
            else:
                raise FileNotFoundError(f"Could not find file: {filepath}")

    gcode_location = 'Metadata/plate_1.gcode'
    io_file = create_zip_archive_in_memory(gcode, gcode_location)
    if gcode:
        try:
            printer.upload_file(io_file, filename)
        except Exception as e:
            print(f"Exception during upload: {e}")
            return
        
        print("Upload done, starting print...")
        printer.start_print(filename, 1)
        print("Start Print Command Sent")


def pause_print(printer):
    """Pause a printer from printing."""

    printer.pause_print()
    
def resume_print(printer):
    """Resume a printer printing."""

    printer.resume_print()


def stop_print(printer):
    """Stop a printer from printing."""

    printer.stop_print()


def toggle_light(serial):
    """Toggle the printer light."""
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


def main():
    load_printers()


if __name__ == "__main__":
    main()