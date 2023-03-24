mport os
import re
import time
from netmiko import ConnectHandler
import getpass

#prompts user for username and password
user = input("Enter your username: ")
pword = getpass.getpass()

# Define seed device
seed_device = {
    'device_type': 'cisco_ios',
    'ip': '10.0.0.2',
    'username': user,
    'password': pword, 
}

# Enter the filename for the output text file
output_file = 'cdp_neighbors.txt'

# Enter the command to execute
command = 'show cdp neighbor detail'

# Create a function to extract IP addresses from the output of the "show cdp neighbor detail" command
def extract_ip_addresses(output):
    ip_regex = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    ip_addresses = re.findall(ip_regex, output)
    return list(set(ip_addresses))

# Connect to the seed device and execute the command
with ConnectHandler(**seed_device) as device:
    output = device.send_command(command)
    output2 = device.send_command(command,use_textfsm=True)

    for ip in output2:
        platform = ip['platform']
        ciscoIP = ip['management_ip']
        if (platform.startswith("cisco WS-C")):
            print(platform)
            print(ciscoIP)
            with open(output_file, 'a+') as file:
                file.seek(0)
                file.write(ciscoIP + '\n')
        else:
            print(platform)

output_file_final = open('cdp_neighbors.txt', 'r')

for host in output_file_final:
    host = host.strip()
    cdp_devices = {
        'device_type': 'cisco_ios',
        'ip': host,
        'username': user,
        'password': pword, 
    }

    with ConnectHandler(**cdp_devices) as cdp_device:
        output = cdp_device.send_command(command)
        output3 = cdp_device.send_command(command,use_textfsm=True)

        for ip in output3:
            platform = ip['platform']
            ciscoIP = ip['management_ip']
            if (platform.startswith("cisco WS-C")):
                print(platform)
                print(ciscoIP)
                with open(output_file, "r") as file:
                    file_contents = file.read()
                if ciscoIP not in file_contents:
                    # Write the variable to the file
                    with open(output_file, "a") as file:
                        file.write(ciscoIP + '\n')
                #with open(output_file, 'a+') as file:
                    #file.seek(0)
                    #file.write(ciscoIP + '\n')
            else:
                print(platform)
