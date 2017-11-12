# glin-dashbutton
use Amazon DASH-Button for glin

Dependencies
------------
 - pyzmq
 - scapy-python3
 
Usage
-----
### as script 
as root: ``python dash.py "12:34:56:78:90:ab" "tcp://127.0.0.1:6607"``
 
optional Parameter: ``-i <interface>``: select interface to listen

### Run without root on Linux
It is also possible to run the script itself without root, but using capabilities. 
1. Compile the script using niutka: ``nuitka --recurse-on --python-version=3.6 dash.py``
2. Then set capabilities: ``sudo setcap cap_net_raw=ep ./dash.exe``
3. And run without root: ``./dash.exe "12:34:56:78:90:ab" "tcp://127.0.0.1:6607"``
