# SlimThuis

Voorraadbeheer, noodpakket-checklist (Denk vooruit / Rijksoverheid), EHBO-gids en
scenario's voor noodsituaties — in één app die volledig offline werkt.

Alle gegevens blijven op het apparaat van de gebruiker (localStorage).
Er is geen server, geen account en geen tracking.

## Online zetten via GitHub Pages (gratis)

1. Maak op github.com een nieuw repository aan, bijvoorbeeld `slimthuis`
   (Public, zonder extra opties).
2. Klik op **uploading an existing file** (of: Add file → Upload files) en
   sleep **alle bestanden uit deze map** erin:
   `index.html`, `manifest.webmanifest`, `sw.js` en de vier `icon-*.png` bestanden.
3. Klik op **Commit changes**.
4. Ga naar **Settings → Pages**. Kies bij *Build and deployment*:
   Source = **Deploy from a branch**, Branch = **main**, map = **/ (root)**. Opslaan.
5. Na een paar minuten staat de app op:
   `https://<jouw-gebruikersnaam>.github.io/slimthuis/`

## Op je eigen website

Upload alle bestanden uit deze map naar een map op je webserver
(bijvoorbeeld via FTP naar `/slimthuis/`). Meer is het niet — er is geen
database of serverconfiguratie nodig. Zorg wel dat je site via **https** draait:
dat is nodig voor de camera (barcodescanner), het offline werken en het
installeren als app.

## Wat krijg je op https vanzelf cadeau

- **Installeerbaar als app**: bezoekers kunnen SlimThuis op hun beginscherm
  zetten (Android: "Toevoegen aan startscherm", iPhone: Deel → "Zet op beginscherm").
- **Werkt offline**: na het eerste bezoek slaat de service worker (`sw.js`)
  alles op. Valt internet weg, dan blijven de noodgids, checklist en voorraad
  gewoon werken — precies waar de app voor bedoeld is.
- **Barcodescanner**: de camera werkt alleen op https. Automatisch scannen
  werkt in Chrome en Edge (en op Android); op iPhone-Safari kan de barcode
  handmatig getypt worden. Het opzoeken van de productnaam (Open Food Facts)
  vereist internet.

## Synchronisatie & delen met huisgenoten (optioneel)

Standaard werkt alles lokaal, zonder account. Wil je inloggen, sync tussen
apparaten en delen via een deelcode? Volg dan `SYNC-SETUP.md` — je koppelt
dan een gratis Supabase-database. Zonder die koppeling verbergt de app de
functie netjes.

## Een nieuwe versie uitbrengen

Pas `index.html` aan en verhoog in `sw.js` het versienummer
(`slimthuis-v1` → `slimthuis-v2`). Bezoekers krijgen de nieuwe versie dan
automatisch bij hun volgende bezoek.

## Let op

- Gegevens staan per apparaat én per browser in localStorage. Browserdata
  wissen = gegevens kwijt.
- De EHBO-stappen en scenario's zijn een geheugensteun en vervangen geen
  EHBO-cursus. Bron noodpakket: denkvooruit.nl (Rijksoverheid).
