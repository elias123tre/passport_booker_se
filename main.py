"""Python script to book first available time for getting a passport in Sweden"""

import datetime
import sys
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from random import randint
from tkinter import Tk
from time import sleep

from playwright.sync_api import sync_playwright

LOCATIONS = [
    "blekinge",
    "dalarna",
    "gotland",
    "gavleborg",
    "halland",
    "jamtland",
    "jonkoping",
    "kalmar",
    "kronoberg",
    "norrbotten",
    "skane",
    "stockholm",
    "sodermanland",
    "uppsala",
    "varmland",
    "vasterbotten",
    "vasternorrland",
    "vastmanland",
    "vastragotaland",
    "orebro",
    "ostergotland",
]

root = Tk()
root.title("Passport booker - Svenska polisen")
root.geometry('325x250')
root.bind('<Control-c>', root.quit)

ttk.Label(root, text="Plats (län):").grid(row=0, column=0)
location = tk.StringVar(root)
ttk.OptionMenu(root, location, "stockholm", *LOCATIONS).grid(row=0, column=1)

ttk.Label(root, text="Antal personer:").grid(row=2, column=0)
people = ttk.Entry(root)
people.grid(row=2, column=1)
people.insert(0, "1")

ttk.Label(root, text="Sista möjliga datum:").grid(row=3, column=0)
date_field = ttk.Entry(root)
date_field.grid(row=3, column=1)
dt = datetime.datetime.now().date()
dt += datetime.timedelta(days=30)
date_field.insert(0, dt.strftime("%Y-%m-%d"))

ttk.Button(root, text="Hitta tid", command=root.quit).grid(
    row=4, column=0, columnspan=2)

root.protocol("WM_DELETE_WINDOW", lambda: sys.exit())
root.mainloop()
root.withdraw()

try:
    last_date = datetime.datetime.strptime(date_field.get(), "%Y-%m-%d")
except ValueError:
    print("Felaktigt datum")
    sys.exit(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    browser.on("disconnected", lambda: sys.exit())
    page = browser.new_page()
    page.goto(
        f"https://bokapass.nemoq.se/Booking/Booking/Index/{location.get()}")
    page.locator('input:has-text("Boka ny tid")').click()
    # Check "Jag har tagit del av informationen ovan"
    page.locator('input[type="checkbox"]').check()

    ppl_selector = page.locator('select[name="NumberOfPeople"]')
    ppl_selector.select_option(people.get())

    page.locator("text=Nästa").click()

    page.wait_for_load_state("domcontentloaded")
    checkboxes = page.locator("text=Ja, jag bor i Sverige")
    count = checkboxes.count()
    if count != int(people.get()):
        print("Hittade inte alla radioknappar")
        sys.exit(1)
    for i in range(count):
        checkboxes.nth(i).click()

    page.locator("text=Nästa").click()

    expeditions = page.locator('select[name="SectionId"]')
    option_tags = expeditions.locator("option")
    options = [option_tags.nth(i).text_content()
               for i in range(option_tags.count())]

    popup = Tk()
    popup.title("Välj passexpedition (ort)")
    popup.geometry('350x200')
    popup.bind('<Control-c>', popup.quit)
    popup.protocol("WM_DELETE_WINDOW", lambda: sys.exit())

    ttk.Label(popup, text="Passexpedition:").grid(row=0, column=0)
    expedition = tk.StringVar(popup)
    ttk.OptionMenu(popup, expedition,
                   options[0], *options).grid(row=0, column=1)

    ttk.Button(popup, text="Fortsätt", command=popup.quit).grid(
        row=4, column=0, columnspan=2)

    popup.mainloop()
    if popup.winfo_ismapped():
        popup.withdraw()

    expeditions.select_option(label=expedition.get())

    try:
        while True:
            page.locator('input:has-text("Första lediga tid")').click()

            page.wait_for_load_state("domcontentloaded")
            page.goto(f"{page.url}#SectionId", wait_until="domcontentloaded")
            times = page.locator('[data-function="timeTableCell"]')
            for time in (times.nth(i) for i in range(times.count())):
                datestring = time.get_attribute("data-fromdatetime")
                date = datetime.datetime.strptime(
                    datestring, "%Y-%m-%d %H:%M:%S")
                if date < last_date:
                    raw_info = time.locator("../ancestor::table").inner_text()
                    info = "\n".join(
                        l for l in raw_info.splitlines() if l and l[2] != ':')
                    time.click()
                    page.screenshot(path="tider.png", full_page=True)
                    page.locator('[aria-label="submit"]').click()

                    message = "\n".join(
                        [f"En ledig bokning {date} har hittats:",
                         info,
                         "Vill du behålla denna tid?"
                         ])
                    root.bell()
                    keep = messagebox.askyesno("Behåll denna tid?", message)
                    if not keep:
                        page.locator("text=Tillbaka").click()
                        page.wait_for_timeout(randint(500, 1_000))
                        continue

                    input("Tryck enter när du bokat färdigt för att spara en skärmdump")
                    page.screenshot(path="bokning.png", full_page=True)

            wait = randint(15_000, 30_000)
            print(
                f"Väntar {round(wait / 1000, 2)} sekunder innan nästa försök")
            page.wait_for_timeout(wait)
    except (KeyboardInterrupt, SystemExit):
        print("trying to quit")
        browser.close()
        # root.quit()
        root.destroy()
        # popup.quit()
        popup.destroy()
        sys.exit()
