# **DISCLAIMER** - Port scanning a host without permission can be considered an attack. don't use this without permission 
# Only use it on devices that have your permission
import socket
import subprocess
import sys
from datetime import datetime
import os

# Gets service name by port so it can print it out to the user
def get_service_name(port):
    try:
        service_name = socket.getservbyport(port)
        return service_name
    except:
        return None

# In order to clear the screen, different commands are used in windows and linux. This allows for usage in both
if os.name == 'nt':
	subprocess.call('cls', shell=True)
else:
	subprocess.call('clear', shell=True)

# Gets IP from user
remoteServer = input("Enter host IP: ")
remoteServerIP = socket.gethostbyname(remoteServer)

# Allows for the user to search in a custom range of ports
try:
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        raise ValueError("Invalid port range. Ports must be between 1 and 65535, and the starting port must be less than or equal to the ending port.")
except ValueError as e:
    print(f"Invalid port number - {e}")
    sys.exit()

# Creates a custom made banner indicating that the scan is processing
print("-" * 60)
print("Scanning host", remoteServerIP)
print("-" * 60) 

# Takes the starting time of the process for later 
t1 = datetime.now()

# Searches through the rang of points
try:
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Sets the max amount of time that a port can be checked to keep the process moving quickly
        socket.setdefaulttimeout(0.1)
        result = sock.connect_ex((remoteServerIP, port))
		# If port is open
        if result == 0:
            service_name = get_service_name(port)
			# Displays open ports and info
            if service_name:
                print(f"Port {port}: Open - Service: {service_name}")
            else:
                print(f"Port {port}: Open - No service information found")
        sock.close()

# Allows user to exit prgram
except KeyboardInterrupt:
	print("Ctrl+C pressed to end program")
	sys.exit()

# Invalid IP/Hostname entered
except socket.gaierror:
	print("Hostname couldn't be resolved")
	sys.exit()

# Ending Time frame
t2 = datetime.now()

# Displays how long the process took
total = t2 - t1
total_seconds = total.total_seconds()
format_total_time = f"{total_seconds:.2f}"
print(f"Scan Completed in: {format_total_time} seconds")