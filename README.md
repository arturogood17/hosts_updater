# hosts_updater
A script to update your hosts file.

This super simple script tries to update your host from a specific web page.
It will extract the information from a web page and update your hosts
from an specific line.

You have to run this script in powershell:

1. Access the path where your script is with something similar to: cd \\wsl$\Ubuntu\home\<your user here>\<folder where your .py file is>\
2. Then run the script with:
Start-Process powershell -Verb RunAs -ArgumentList "wsl python3 /home/<your user here>/<folder where your file is>/hosts_updater.py; Read-Host 'Press Enter to close'"

This will run the script as an administrator and you'll be able to see if the script worked or not.