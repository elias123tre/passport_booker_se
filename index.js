const { chromium, errors } = require("playwright")
const notifier = require("node-notifier")

// CHANGE THIS LINE!: last date that can automatically be booked
const THRESHOLD = new Date("2022-07-28 ")

// OPTIONAL: change this line to the location where to book, omit if every location
const LOCATION = null // Change `null` to ex. "Haninge"

// OPTIONAL: change this line to the number of people to book for
const NUMBER_OF_PEOPLE = 3

// OPTIONAL: locations to not reserve time for otherwise empty array
const SKIP_LOCATIONS = ["Rinkeby", "Norrtälje", "Täby", "Södertälje"]

/**
 * @param {number} min
 * @param {number} max
 */
function getRandomIntInclusive(min, max) {
  min = Math.ceil(min)
  max = Math.floor(max)
  return Math.floor(Math.random() * (max - min + 1) + min) //The maximum is inclusive and the minimum is inclusive
}

/**
 * Random timeout in milliseconds
 * @returns
 */
function getRandomTimeout() {
  return getRandomIntInclusive(15_000, 30_000)
}

;(async () => {
  const browser = await chromium.launch({
    headless: false,
    // slowMo: 100,
    // devtools: true,
  })
  const context = await browser.newContext()

  // Open new page
  const page = await context.newPage()

  await page.goto("https://bokapass.nemoq.se/Booking/Booking/Index/stockholm")

  await page.locator('input:has-text("Boka ny tid")').click()

  // Check "Jag har tagit del av informationen ovan"
  await page.locator('input[type="checkbox"]').check()

  await page
    .locator('select[name="NumberOfPeople"]')
    .selectOption(NUMBER_OF_PEOPLE.toString())

  await page.locator("text=Nästa").click()

  await page.waitForLoadState("domcontentloaded")
  const checkboxes = page.locator("text=Ja, jag bor i Sverige")
  const count = await checkboxes.count()
  for (let i = 0; i < count; ++i) {
    await checkboxes.nth(i).click()
  }

  await page.locator("text=Nästa").click()

  // Optional: select certain location
  if (LOCATION) {
    await page
      .locator('select[name="SectionId"]')
      .selectOption({ label: LOCATION })
  }

  let backoff = getRandomTimeout()
  outer: while (true) {
    // Get new times
    await page
      .locator('input:has-text("Första lediga tid")')
      .click()
      .catch(async (e) => {
        console.error(e)
        await page.pause()
      })
    // Locate times
    await page.waitForLoadState("domcontentloaded")
    await page.goto(`${page.url()}#SectionId`, {
      waitUntil: "domcontentloaded",
    })
    const times = page.locator('[data-function="timeTableCell"]')

    // Iterate over time cards
    const count = await times.count()
    for (let i = 0; i < count; i++) {
      let elem = times.nth(i)
      const date = new Date(await elem.getAttribute("data-fromdatetime"))
      if (date < THRESHOLD) {
        const info = await elem.locator("../ancestor::table").innerText()
        const infoLines = info.split(/\n+/)
        const formatted = [
          infoLines.slice(0, infoLines.length - 3).join("\n"),
          infoLines.slice(infoLines.length - 3).join(" "),
        ].join("\n")
        // Skip blacklisted locations
        if (SKIP_LOCATIONS.some((search) => formatted.includes(search))) {
          continue
        }
        await page.waitForTimeout(100)
        // select the time
        elem.click()

        console.log("Tid hittad:", date.toLocaleString())
        await page.screenshot({ fullPage: true, path: "booking.png" })
        console.log(formatted)

        await page.locator('[aria-label="submit"]').click()

        // Windows notification on new booking
        notifier.notify({
          title: "Pass bokningstid hittad!",
          message: formatted,
          sound: "C:\\Windows\\Media\\Alarm05.wav",
          icon: "C:\\Users\\Elias\\Downloads\\pass\\passport.png",
          wait: false,
        })
        break outer
      }
    }

    console.time("waited")
    try {
      // wait 1 sec or backoff between tries
      await page.waitForSelector(
        "text=Du har gjort för många 'första lediga tid' sökningar, var vänlig och vänta en stund.",
        { timeout: getRandomTimeout() }
      )
      console.log("Rate limit reached, backing off:", backoff / 1000, "seconds")
      await page.waitForTimeout(backoff)
      backoff *= 5
    } catch (error) {
      if (error instanceof errors.TimeoutError) {
        // console.log(
        //   "No rate limit, waiting random amount of seconds between tries"
        // )
        backoff = getRandomTimeout()
      } else {
        throw error
      }
    }
    console.timeEnd("waited")
  }

  await page.pause()

  await page.screenshot({ fullPage: true, path: "bekräftelse.png" })

  // ---------------------
  await context.close()
  await browser.close()
})()
