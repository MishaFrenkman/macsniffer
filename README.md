# Macsniffer

### About

This script reacts on connection/disconnection of a specific device in your local network based on its MAC 

### Usage

- -h (--help) for arguments usage
- run with sudo
- provide your own network and device information
- edit push() with your own script
- nmap must be installed

### Known Bugs

iPhones tend to switch to a kind of sleep-mode when not in use and disconnect from the network. <br>
Depends on the usecase you could set -s to 30 minutes or longer, to prevent false positives.
