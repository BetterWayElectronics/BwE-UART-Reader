import sys
import serial
import serial.tools.list_ports
import time
import datetime
import re
import os
import keyboard
import pygetwindow as gw
from colorama import init, Fore, Style
import ctypes

def set_window_title(title):
    ctypes.windll.kernel32.SetConsoleTitleA(title)

set_window_title('BwE UART Reader')

# UART Reader Banner
bwe = """
  __________         ___________
  \______   \__  _  _\_   _____/
   |    |  _/\ \/ \/ /|    __)_ 
   |    |   \ \     / |        \\
   |______  /  \/\_/ /_______  /
          \/  UART Reader    \/ 
                                    """

print(Fore.CYAN + Style.BRIGHT + bwe + Style.RESET_ALL)

# Search for available ports
pattern = re.compile(r"^(USB-?Serial|USB Serial)\b", re.IGNORECASE)
ports = list(serial.tools.list_ports.comports())
auto_ports = [port[0] for port in ports if pattern.search(port[1])]

# Prompt user for port selection or auto-select if only one is found
if auto_ports:
    if len(auto_ports) > 1:
        print("Multiple UART Devices Found At " + ", ".join(auto_ports) + "\n")
        port = raw_input("Enter COM Port (Example COM4): ")
        digits = ''.join(filter(str.isdigit, port))
        port = 'COM' + digits[:2]
        print("\nOpening " + port + "...\n")
    else:
        port = auto_ports[0]
        print("UART Reader {} Found. Opening {}...\n".format(port[1], auto_ports[0]))
else:
    port = raw_input("Enter COM Port (Example COM4): ")
    digits = ''.join(filter(str.isdigit, port))
    port = 'COM' + digits[:2]

if not port: 
    print(Fore.GREEN + "\nError: No Port Specified. Exiting program." + Style.RESET_ALL)
    print("\nPress Enter to Exit...")
    raw_input()  
    sys.exit(1) 

# Set up serial connection
baud = 115200
sread = serial.Serial(timeout=0.1)  # 0.1 seconds timeout
sread.port = port
sread.baudrate = baud

try:
    sread.open()
except:
    sys.stderr.write("Error Opening COM Port %s. Press Enter to Exit." % sread.portstr)
    raw_input()  
    sys.exit(1) 

# Global running flag
running = True

def on_key_event(e):
    global running

    # Get the title of the active window
    active_window_title = gw.getActiveWindow().title

    # Check if the active window title matches the title of the Python script's window
    if 'BwE UART Reader' in active_window_title:
        if e.name == 'enter' and e.event_type == keyboard.KEY_DOWN:  # Enter key
            #print(Fore.RED + "\nExiting..." + Style.RESET_ALL)
            running = False
        elif e.name == 'space' and e.event_type == keyboard.KEY_DOWN:  # Space key
            print(Fore.YELLOW + "\nClearing Screen..." + Style.RESET_ALL)
            time.sleep(1)
            os.system('cls')
            print(Fore.CYAN + Style.BRIGHT + bwe2 + Style.RESET_ALL)

# Register the key event handler
keyboard.hook(on_key_event)

# UART Reader Banner 2
bwe2 = """
  __________         ___________
  \______   \__  _  _\_   _____/
   |    |  _/\ \/ \/ /|    __)_ 
   |    |   \ \     / |        \\
   |______  /  \/\_/ /_______  /
          \/  UART Reader    \/  {} Opened...
                                    """.format(port)

os.system('cls')
print(Fore.CYAN + Style.BRIGHT + bwe2 + Style.RESET_ALL)

# Create file for logging UART data
now = datetime.datetime.now()
filename = "uart_data_{}-{}-{}_-_{}-{}-{}.txt".format(now.year, now.month, now.day, now.hour, now.minute, now.second)

# Main loop: read from serial port, write to file, print to console
with open(filename, "w") as f:
    try:
        while running:
            data = sread.read(1)
            if data:  # Only proceed if data is not an empty string
                n = sread.inWaiting()
                if n:
                    data = data + sread.read(n)
                sys.stdout.write(data)
                f.write(data) 
    except KeyboardInterrupt:
        pass
    finally:
        sread.close()
        keyboard.unhook_all()  # Unhook all keyboard event handlers
        print(Fore.GREEN + "\nProgram Interrupted by User. Log Saved As " + filename + Style.RESET_ALL)
        sys.stdout.flush() 
        raw_input("\nPress Enter to Exit.") 
        sys.exit(1)

