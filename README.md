# Automatic passport booker - Boka pass automatiskt hos Svenska polisen

> A cross-platform script to book first available time for getting a passport in Sweden - Ett skript som automatiskt bokar pass hos polisen

Eftersom polisen fortfarande inte har fixat fler tider för att boka pass så kommer detta skript att hitta den första möjliga tiden att boka pass och reservera den. Denna metod kommer högst troligt inte längre fungera efter **två veckor** då polisen ska uppdatera systemet för att förhindra bot-reservationer [(källa)](https://www.expressen.se/dinapengar/sa-ska-polisen-stoppa-fulbokningen-av-pass/).

![User interface](https://i.imgur.com/a0jFgia.png)
![Location user interface](https://i.imgur.com/VM1XKI5.png)

Ett liknande skript finns redan [(jonkpirateboy/Pass-fur-alle)](https://github.com/jonkpirateboy/Pass-fur-alle) som kan automatisk genomföra slutsteget för bokningar som använder den lite mer komplicerade mjukvaran [Selenium](https://www.selenium.dev/) (jämfört med [playwright](https://playwright.dev/python/)) och har inget grafiskt gränssnitt för att välja parametrar. Mitt skript saknar automatisk genomförelse av bokningen men är lättare att installera och har ett grafiskt gränssnitt.

## Instructions

> Prerequisites: python3.7 (or higher), pip

1. Install playwright:

   ```sh
   pip install --upgrade pip
   pip install playwright
   playwright install chromium
   ```

2. Download the script

3. Run the script:

   ```sh
   python main.py
   ```

4. Follow onscreen instructions

5. Wait for a time to become available, a popup will appear (the page reloads itself in the background)

6. Optional: force-quit the script anytime by pressing CTRL+C (ignore any errors that appear)
