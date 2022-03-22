# Passport booker - Svenska polisen

> A cross-platform script to book first available time for getting a passport in Sweden

Eftersom polisen fortfarande inte har fixat fler tider för att boka pass så kommer detta skript att hitta den första möjliga tiden att boka pass och reservera den. Denna metod kommer högst troligt inte längre fungera efter **två veckor** då polisen ska uppdatera systemet för att förhindra bot-reservationer [(källa)](https://www.expressen.se/dinapengar/sa-ska-polisen-stoppa-fulbokningen-av-pass/).

Ett liknande skript finns redan [(jonkpirateboy/Pass-fur-alle)](https://github.com/jonkpirateboy/Pass-fur-alle) men det är anpassat för Mac och har inget grafiskt gränssnitt för att välja parametrar. Jämfört med detta som är enklare att installera, funkar på alla operativsystem och har grafiskt gränssnitt för att välja datum, antal personer osv.

## Instructions

> Prerequisites: python3, pip

1. Install playwright:

   ```sh
   pip install playwright
   playwright install
   ```

2. Download the script

3. Run the script:

   ```sh
   python main.py
   ```

4. Follow onscreen instructions

5. Wait for a time to become available, a popup will appear (the page reloads itself in the background)
