import commands
import argparse
from getpass import getpass
from netmiko import SSHDetect, ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException


print("Cisco Healthcheck Starting....")

parser = argparse.ArgumentParser(description='Collect required information for a basic Cisco device health check')
parser.add_argument("ipaddress",nargs='+',help="ip addresses of devices to connect to")
parser.add_argument('-u',metavar='user',dest='username',help='Username to user to log into switch',action='store')
parser.add_argument('-o',dest='onscreen',action='store_true',help="Display output on screen")
args=parser.parse_args()


ipaddress = args.ipaddress
username=args.username
onscreen = args.onscreen

if username == None:
    username = input("Username: ")


password = getpass(prompt="Password: ")

print ("IP Addresses to check health on: ")
for hosts in args.ipaddress:
    print (hosts+" ")
print ("Username to authenticate with: " + username)


# Iterate through the devices that were passed and attempt to gather information.
for device in ipaddress:


    remote_device = {'device_type': 'autodetect',
                    'host': device,
                    'username': username,
                    'password': password}

    print ("------------------------------------------------------------")
    print ("Performing a health check on "+device)

    # Try to detect the type of deevice
    try:

        guesser = SSHDetect(**remote_device,timeout=10)
    except (NetMikoAuthenticationException, NetMikoTimeoutException) as e:
        print("Error connecting to device: "+str(e))
        continue

    best_match = guesser.autodetect()

    print("This device is detected to be model type: " + best_match)

    if best_match not in ['cisco_ios', 'cisco_nxos', 'cisco_xr']:
        print("ERROR: " + best_match + " is not currently supported in this revision")
        continue
    else:

        remote_device['device_type'] = best_match

        ssh_connection = ConnectHandler(**remote_device)

        ssh_connection.open_session_log("session-log-"+device+".log", mode=u'write')

        # enter enable mode
        ssh_connection.enable()

        # prepend the command prompt to the result (used to identify the local host)
        result = ssh_connection.find_prompt() + "\n"
        print ("Device name is: "+result)

        # execute the show cdp neighbor detail command
        # we increase the delay_factor for this command, because it take some time if many devices are seen by CDP

        if best_match == 'cisco_ios':
            cmds = commands.commands_ios
        elif best_match == 'cisco_nxos':
            cmds = commands.commands_nxos
        elif best_match == 'cisco_xr':
            cmds = commands.commands_iosxr


    for command in cmds:
        print("Executing: '" + command + "' on " + device)

        result = ssh_connection.send_command(command)

        if onscreen:
            print(result)

        # close SSH connection
    ssh_connection.close_session_log()
    ssh_connection.disconnect()

