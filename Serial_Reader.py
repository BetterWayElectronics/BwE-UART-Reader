import sys
import serial
import serial.tools.list_ports
import time

bwe = """
                    .__       .__                            .___            
  ______ ___________|__|____  |  |_______   ____ _____     __| _/___________ 
 /  ___// __ \_  __ \  \__  \ |  |\_  __ \_/ __ \\__   \   / __ |/ __ \_  __ \\
 \___ \\\  ___/|  | \/  |/ __ \|  |_|  | \/\  ___/ / __ \_/ /_/ \  ___/|  | \/
/____  >\___  >__|  |__(____  /____/__|    \___  >____  /\____ |\___  >__|   
     \/     \/              \/                 \/     \/      \/    \/       
                                   BwE <3
     """
     
print bwe

ports = list(serial.tools.list_ports.comports())
auto_ports = []
for port in ports:
    if "USB Serial Port" in port[1]:
        auto_ports.append(port[0])

if auto_ports:
    if len(auto_ports) > 1:
        print("\033[33mMultiple UART Devices Found At " + ", ".join(auto_ports) + "\033[0m\n")
        port = raw_input("Enter COM Port (Example COM4): ")
    else:
        print("\033[32mUART Reader Found At " + auto_ports[0] + "\033[0m\n")
        port = auto_ports[0]
else:
    port = raw_input("Enter COM Port (Example COM4): ")


if not port: 
    print("\nError: No port specified. Exiting program.")
    print ("\033[0m\nPress Enter to Exit...")
    raw_input()  
    sys.exit(1) 
        
baud = 115200

sread = serial.Serial()
sread.port = port
sread.baudrate = baud

try:
    sread.open()
except:
    sys.stderr.write("Error opening serial port %s\n" % (sread.portstr) )
    sys.exit(1)

# Ask the user if they want the data to be presented as binary
binary_response = raw_input("Output & Save Serial As Hex? (y/n): ")

try:
    # Open a file to save the serial data
    if binary_response.lower() == "y":
        print "\nWaiting...\n"
        with open("serial_data.bin", "wb") as f:
            while 1:
                # Read from serial port, blocking
                data = sread.read(1)

                # If there is more than 1 byte, read the rest
                n = sread.inWaiting()
                if n:
                    data = data + sread.read(n)

                # Print the data to the console
                sys.stdout.write(data.encode("hex").upper())  #printing hexadecimal
                # Write the data to the file
                f.write(data)

    else:
        print "\nWaiting...\n"
        with open("serial_data.txt", "w") as f:
            while 1:
                # Read from serial port, blocking
                data = sread.read(1)

                # If there is more than 1 byte, read the rest
                n = sread.inWaiting()
                if n:
                    data = data + sread.read(n)

                # Print the data to the console
                sys.stdout.write(data)
                # Write the data to the file
                f.write(data) 

except KeyboardInterrupt:
    pass
finally:
    sread.close()
    print("\n\nProgram interrupted by user. Press Enter to Exit.")
    raw_input()  
    sys.exit(1) 
