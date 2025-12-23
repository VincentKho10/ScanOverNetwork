##
# python-ScanOverNetwork
Open source app to do document scanning over network

# Motivation
One scanner multiple pc, scanning document need to be done near connected computer. In case computer being used then queue happen. To remove queue how about pc running as server waiting a certain get request being called? thats it a server waiting a request and scanning your document for you

# Quick Start
There is two executable file:
```
 - LanScanner_\[version\].exe
 - LanScannerDebug_\[version\].exe
```
Debug will show you what happen during execution if something went wrong.<br><br>
How to use:
```
 - Executable need to be $${\color{red}run\ as\ administrator}$$
 - open your browser
 - type on address bar http://{your address ie: localhost | 192.168.xx.xx}:3000/scan
 - your result could be found on in folder named scanned on the same folder as executable
```

# Usage
To make it public put your executable on shared a folder. then everyone with access to that shared folder could use your scanner
