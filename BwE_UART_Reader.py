import sys
import serial
import serial.tools.list_ports
import time
import datetime
import re
import os
from colorama import init, Fore, Style

bwe = """
  __________         ___________
  \______   \__  _  _\_   _____/
   |    |  _/\ \/ \/ /|    __)_ 
   |    |   \ \     / |        \\
   |______  /  \/\_/ /_______  /
          \/  UART Reader    \/ 
                                    """
     
print(Fore.CYAN + Style.BRIGHT + bwe + Style.RESET_ALL)

pattern = re.compile(r"^(USB-?Serial|USB Serial)\b", re.IGNORECASE)
ports = list(serial.tools.list_ports.comports())
auto_ports = []

for port in ports:
    if pattern.search(port[1]):
        auto_ports.append(port[0])


if auto_ports:
    if len(auto_ports) > 1:
        print("Multiple UART Devices Found At " + ", ".join(auto_ports) + "\n")
        port = raw_input("Enter COM Port (Example COM4): ")
        digits = ''.join(filter(str.isdigit, port))
        port = 'COM' + digits[:2]
        print("\nOpening " + port + "...\n")
    else:
        print("UART Reader " + port[1] + " Found. Opening " + auto_ports[0] + "...\n")
        port = auto_ports[0]
else:
    port = raw_input("Enter COM Port (Example COM4): ")
    digits = ''.join(filter(str.isdigit, port))
    port = 'COM' + digits[:2]

if not port: 
    print("\nError: No Port Specified. Exiting program.")
    print ("\nPress Enter to Exit...")
    raw_input()  
    sys.exit(1) 
        
baud = 115200

sread = serial.Serial()
sread.port = port
sread.baudrate = baud

try:
    sread.open()
except:
    sys.stderr.write("\nError Opening COM Port %s. Press Enter to Exit." % sread.portstr)
    raw_input()  
    sys.exit(1) 

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

now = datetime.datetime.now()
filename = "uart_data_{}-{}-{}_-_{}-{}-{}.txt".format(now.year, now.month, now.day, now.hour, now.minute, now.second)

with open(filename, "w") as f:
    try:
        while 1:
            data = sread.read(1)
            n = sread.inWaiting()
            if n:
                data = data + sread.read(n)
            sys.stdout.write(data)
            f.write(data) 

    except KeyboardInterrupt:
        pass
    finally:
        sread.close()
        print("\n\nProgram Interrupted by User. Log Saved As " + filename + "\n\nPress Enter to Exit.")
        raw_input()  
        sys.exit(1) 
