CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Requirements
 * Installation
 * Configuration
 * Maintainers


INTRODUCTION
------------

This package contains all the resources necessary to configure and launch the Matrix client agent on Linux-based and 
Windows systems. The Matrix server can be found on GitHub here: https://github.com/ryanpepe2000/mscs710-backend.



REQUIREMENTS
------------

python3: https://www.python.org/downloads/

Once python3 is installed, please launch the terminal and navigate to this package's directory. The following command 
must be issued in order for the client agent to function as intended: 

`pip install -r requirements.txt`


CONFIGURATION
-------------
###MacOS
* Open up your terminal command prompt on your Mac and navigate to the home directory by running `cd ~/`.
* Copy the installation path of python3 via the command `which python3`. This should display something like this: `/usr/local/bin/python3`
* Open an empty crontab file via `crontab -e`.
* Start the cron job with the following syntax (you may have to edit this text depending on your python3 installation path as noted above)
``` 
* * * * * cd ~/Downloads/agent && /usr/local/bin/python3 
cron_test.py >> ~/Documents/agent/log.txt 2>&1
```
Please note that '~/Downloads/agent' should be the path to the 
unzipped agent that you downloaded from the Matrix dashboard.
* Type `:q!` to quit the crontab editor.

###Other Linux-based Systems
* Open up your terminal command prompt on your Mac and navigate to the home directory by running `cd ~/`.
* Copy the installation path of python3 via the command `which python3`. This should display something like this: `/usr/local/bin/python3`
* Open an empty crontab file via `crontab -e`.
* Start the cron job with the following syntax (you may have to edit this text depending on your python3 installation path as noted above)
``` 
* * * * * cd ~/Downloads/agent && /usr/local/bin/python3 
cron_test.py >> ~/Documents/agent/log.txt 2>&1
```
Please note that '~/Downloads/agent' should be the path to the 
unzipped agent that you downloaded from the Matrix dashboard.
* Type `:q!` to quit the crontab editor.

###Windows
* Please refer to this guide on scheduling a python file with the Windows Task Scheduler tool: https://datatofish.com/python-script-windows-scheduler/

MAINTAINERS
-----------

 * Ryan Pepe
 * Christian Salterelli