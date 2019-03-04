# cisco-healthcheck

## Introduction
This python script will run a series of show commands for cisco devices to gather useful information that can be uploaded to Cisco TAC when troubleshooting devices.   The script will create a file for all the output of the files

Normally when a issue occurs, Cisco TAC asks to collect information from network devices.   Sometimes, time is of the essence and therefore, it would be great to run some basic scripts to gather logs while we begin the troubleshooting process.

## Requirements
This module leverages python 3 and the following libraries are required:

netmiko

You can install the required libraries by:

``` pip install netmiko``` 

or 

```pip -f requirements.txt```

## Command Line Options

To execute the module, you can use the following command:

``` python cisco-healthcheck.py```

If you don't provide any options, it will provide you with a simple help menu

```bash
$ python cisco-healthcheck.py -h
Cisco Healthcheck Starting....
usage: cisco-healthcheck.py [-h] [-u user] [-o] ipaddress [ipaddress ...]

Collect required information for a basic Cisco device health check

positional arguments:
  ipaddress   ip addresses of devices to connect to

optional arguments:
  -h, --help  show this help message and exit
  -u user     Username to user to log into switch
  -o          Display output on screen
```

### Command Line Options

* **-h** - display a help screen
* **-u** - specify the username that will be used *(NOTE: the script will prompt you for the current password)*
* **-o** - show the output of the commands to the screen as well as the file
* **hostnames** - a list of IP addresses to gather the statistics for

## Output
The following is a very simple example:

```bash
$ python cisco-healthcheck.py 1.1.1.1 10.94.241.234 10.94.241.235
Cisco Healthcheck Starting....
Username: cisco
Password: 
IP Addresses to check health on: 
1.1.1.1 
10.94.241.234 
10.94.241.235 
Username to authenticate with: cisco
------------------------------------------------------------
Performing a health check on 1.1.1.1
Error connecting to device: Connection to device timed-out: autodetect 1.1.1.1:22
------------------------------------------------------------
Performing a health check on 10.94.241.234
This device is detected to be model type: cisco_xr
Device name is: RP/0/0/CPU0:iosxrv-1#

Executing: 'sh reboot hist' on 10.94.241.234
Executing: 'sh config commit' on 10.94.241.234
Executing: 'sh install active summary' on 10.94.241.234
Executing: 'sh platform' on 10.94.241.234
Executing: 'sh redundancy' on 10.94.241.234
Executing: 'sh diag details' on 10.94.241.234
Executing: 'sh memory summary' on 10.94.241.234
Executing: 'sh watchdog memory-state location all' on 10.94.241.234
Executing: 'sh mem heap summ all' on 10.94.241.234
Executing: 'sh env temp' on 10.94.241.234
Executing: 'sh env voltage' on 10.94.241.234
Executing: 'sh env led' on 10.94.241.234
------------------------------------------------------------
Performing a health check on 10.94.241.235
This device is detected to be model type: cisco_nxos
Device name is: nx-osv-1#

Executing: 'show interface counter error' on 10.94.241.235
Executing: 'show processes cpu history' on 10.94.241.235
Executing: 'show processes cpu sort | ex 0.0' on 10.94.241.235
Executing: 'show sys internal mts buff detail' on 10.94.241.235
Executing: 'show logg onboard exceptional-log' on 10.94.241.235
Executing: 'show spanning-tree active detail | in exe|topo|from' on 10.94.241.235
Executing: 'show policy-map interface control plane' on 10.94.241.235
Executing: 'show module' on 10.94.241.235
Executing: 'show environment | ex OK' on 10.94.241.235
Executing: 'show logg last 100' on 10.94.241.235
Executing: 'show diagnostic events | in Fail|Bad' on 10.94.241.235
Executing: 'show diagnostic results module all' on 10.94.241.235
Executing: 'show environmental temperature | ex Ok' on 10.94.241.235
Executing: 'show environment power' on 10.94.241.235
Executing: 'show processes cpu history' on 10.94.241.235
Executing: 'show module' on 10.94.241.235
Executing: 'show cores vdc-all' on 10.94.241.235
Executing: 'show system internal mts buffer summary' on 10.94.241.235
Executing: 'sho policy-map interface | inc net|nel|drop | ex ": 0" | ex "violated 0" | ex "conformed 0"' on 10.94.241.235
Executing: 'show policy-map interface control-plane | i class|module|trans|drop | ex "0 packets"' on 10.94.241.235
Executing: 'show interface counters errors | exclude "\ 0\ *0\ *0\ *0\ *0\ *0"| ex "\ 0\ *--\ *0\ *0\ *0"' on 10.94.241.235
Executing: 'show interface counter errors | diff' on 10.94.241.235
Executing: 'sho hardware capacity eobc' on 10.94.241.235
Executing: 'sho hardware capacity modulesho hardware internal forwarding l2 table utilization' on 10.94.241.235
Executing: 'show system internal access-list resource utilization | in INSTANCE|Resource|--|Free|Utilization$|[1][0-05-9][0-9]\.' on 10.94.241.235
Executing: 'show hardware rate-limiter' on 10.94.241.235
Executing: 'sho hardware internal cpu-mac eobc stats | grep -a 26 Error.counters' on 10.94.241.235
Executing: 'sho spanning-tree det | i occur|exec|from' on 10.94.241.235
$
```

In addition, the script will produce an output files that contain all the detailed information:

```
$ ls -l *.log
-rw-r--r--  1 cbogdon  staff  24888 Mar  4 18:17 session-log-10.94.241.234.log
-rw-r--r--  1 cbogdon  staff  41067 Mar  4 18:18 session-log-10.94.241.235.log
```

## Customization
The commands.py define three different lists which include all the commands that will be executed by the module.   The following is a very simple example that show what is in that file.   You can customize this by adding the list of commands you wish to execute when the application is run.

```bash
commands_ios=["sh ver",
              "sh license"]

commands_iosxr = ['sh ver']

commands_nxos = ['sh ver']
```


## Limitations
* Currently, the application is only tested with IOS-XR, IOS-XE and NXOS devices.   Any other devices that are detected are ignored
* There is very limited error checking.   If we can't open a connection to the device we will display an error message.

