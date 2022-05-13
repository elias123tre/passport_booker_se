# Hitta lediga tider för bokning av pass hos polisen

> **VIKTIGT!!** Denna branch uppdateras inte och fungerar inte heller i nuläget! Denna version skriven i Node.JS skrevs innan men är deprecated nu, se branch `main` för ett fungerande program!

1. Installera plugins: `npm install`
2. Ändra raden `const THRESHOLD = new Date(...)` i `index.js` till det senaste datumet som ska reserveras automatiskt, valfri ort kan också väljas (annars söks alla orter)
3. Kör skriptet: `npm run start` och vänta
4. När en tid hittas reserveras den och en screenshot (sparas som `booking.png`) tas på bokningen och notifikation visas
5. Fyll i personuppgifter och genomför bokningen (bör göras direkt så man inte blir utloggad pga inaktivitet)
6. På sidan med bokningsbekräftelsen kan playwright skriptet fortsättas och då tas en screenshot på bokningsbekräftelsen (sparas som `bekräftelse.png`)
7. Du har nu en bokad tid, verifiera att bekraftelse kommit via epost eller sms
