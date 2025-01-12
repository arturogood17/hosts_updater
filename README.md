# hosts_updater
A script to update your hosts file.

This super simple script tries to update your host from a specific web page.
It will extract the information from a web page and update your hosts
from an specific line.

1. Run Powershell as administrator:

2. Access the path where your script is with something similar to: cd C:\Users\<your user>\<folder where your .py is>
2. Then run the script with:
Start-Process powershell -Verb RunAs -ArgumentList "wsl python3 /mnt/c/Users/<your user>/<folder where your .py is>/hosts_updater.py; Read-Host 'Press Enter to close'"

This will run the script as an administrator and you will be able to see if it works