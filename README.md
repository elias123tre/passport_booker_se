# Automatic passport booker - Boka pass automatiskt hos Svenska polisen

> A cross-platform script to book first available time for getting a passport in Sweden - Ett skript som automatiskt bokar pass hos polisen

Eftersom polisen fortfarande inte har fixat fler tider för att boka pass så kommer detta skript att hitta den första möjliga tiden att boka pass och reservera den. Denna metod kommer högst troligt inte längre fungera efter **två veckor** då polisen ska uppdatera systemet för att förhindra bot-reservationer [(källa)](https://www.expressen.se/dinapengar/sa-ska-polisen-stoppa-fulbokningen-av-pass/).

![User interface](https://i.imgur.com/a0jFgia.png)
![Location user interface](https://i.imgur.com/VM1XKI5.png)

### Relaterade/liknande projekt:
- [jonkpirateboy/Pass-fur-alle](https://github.com/jonkpirateboy/Pass-fur-alle) - has automatic booking confirming feature
- [kalkih/passport-appointment-bot](https://github.com/kalkih/passport-appointment-bot) - has prebuilt executables, SUPER easy to install (check this out if you have any problems with the others)
- This project - has graphical interface for parameter selection

## Instructions

> Note: beware that on Mac you may need to enable extensive permissions to install python, puppeteer or run the script. I don't have a Mac to test on so if you encounter this, Google the error message and how to solve it.

1. Install python:

   a. Open terminal
   
   _Windows_: type `powershell` in the search bar (lower left corner) then right click on `Windows PowerShell` and press `Run as administrator`

   _Mac_: open the terminal, preferably by typing `terminal` into the spotlight search bar (upper right corner) then select terminal
   
   b. Check if it is already installed
   
   _Windows & mac_: type `python --version` then enter, if it displays a python version starting with 3.7 or grater, continue to step 2
   
   c. If not installed (previous output shows that the command was not found)
   
   Install python from official source: https://www.python.org/downloads/  
   Check the box for `Add Python 3.x to PATH` if it appears
   
   If you get stuck on this step, search for how to install python for your operating system

2. Install playwright:

   Close the terminal/console from step 1.a. and a new one the same way. Then type the following lines one by one and press enter after each one.

   _Windows_:  
   ```sh
   $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
   python -m pip install --upgrade pip
   python -m pip install playwright
   playwright install chromium
   ```
   
   _Mac_:  
   ```sh
   python3 -m pip install --upgrade pip
   python3 -m pip install playwright
   playwright install chromium
   ```

3. [Download the script](https://raw.githubusercontent.com/elias123tre/passport_booker_se/main/main.py) (press CTRL+S to save the file, select Downloads folder)

4. Run the script:
   
   Type the following lines one by one into the new terminal/console that you openend in step 2.

   _Windows_:  
   ```sh
   cd ~/Downloads
   python main.py
   ```
   
   _Mac_:  
   ```sh
   cd ~/Downloads
   python3 main.py
   ```

5. Follow onscreen instructions and enter the details about your search

6. Wait for a time to become available, a popup will appear (the page reloads itself in the background to search for new times).  
   Note: if the booking isn't verified/completed manually (entering personal details) after the popup has appeared, it will be lost after some time due to inactivity

7. Optional: force-quit the script anytime by closing the browser or by pressing CTRL+C in the terminal/console (ignore any errors that appear)
