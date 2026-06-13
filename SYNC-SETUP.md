# SlimThuis — synchronisatie & delen instellen (Supabase)

Hiermee kun je inloggen via e-mail, gegevens synchroniseren tussen apparaten
en je huishouden delen met huisgenoten via een deelcode. Kosten: € 0
(gratis Supabase-tier is ruim voldoende). Duurt ongeveer 10 minuten.

## Stap 1 — Maak een Supabase-project

1. Ga naar https://supabase.com en maak een gratis account.
2. Klik op **New project**. Kies een naam (bijv. `slimthuis`), een sterk
   databasewachtwoord (bewaar dit) en als regio **eu-central-1 (Frankfurt)**
   of **eu-west** — dan staan de gegevens binnen de EU (AVG).
3. Wacht tot het project klaar is (± 2 minuten).

## Stap 2 — Zet de database op

1. Open in het dashboard de **SQL Editor**.
2. Plak de volledige inhoud van `supabase-setup.sql` en klik **Run**.
   Dit maakt de tabellen, beveiligingsregels en deelcode-functies aan.

## Stap 3 — Sta je website toe

1. Ga naar **Authentication → URL Configuration**.
2. Zet bij *Site URL* het adres van je site, bijvoorbeeld
   `https://jouwnaam.github.io/slimthuis/`
   (dit is waar de inloglink uit de e-mail naartoe wijst).

## Stap 4 — Vul de sleutels in

1. Ga naar **Project Settings → API**. Je ziet daar:
   - **Project URL** (bijv. `https://abcdefgh.supabase.co`)
   - **anon public** sleutel (lange tekenreeks)
2. Open `index.html` en zoek bovenin het script naar:

   ```js
   const SYNC_URL = '';
   const SYNC_KEY = '';
   ```

3. Vul beide in en zet de site opnieuw online (bij GitHub: bestand
   opnieuw uploaden / committen). Hoog meteen in `sw.js` de cacheversie op.

> De anon-sleutel is bedoeld om openbaar in de site te staan — de
> beveiliging zit in de Row Level Security-regels uit stap 2: iedereen
> kan uitsluitend het eigen huishouden lezen en bijwerken.

## Hoe het werkt voor gebruikers

1. Onderaan **Vandaag** staat nu "Delen & synchroniseren".
2. E-mailadres invullen → inloglink in de mail → klaar, geen wachtwoord.
3. **Start een huishouden** (jouw huidige gegevens worden de gedeelde set)
   en geef de **deelcode** van 6 tekens aan je huisgenoot.
4. Huisgenoot logt in en kiest **Sluit aan** met die code — vanaf dan zien
   jullie elkaars wijzigingen vrijwel direct (realtime), op alle apparaten.

Goed om te weten:
- De app blijft offline-first: zonder internet werkt alles gewoon door en
  wordt er gesynchroniseerd zodra er weer verbinding is.
- Sluit je aan bij een bestaand huishouden, dan nemen de gedeelde gegevens
  het over op jouw apparaat.
- Bij gelijktijdige wijzigingen wint de laatste schrijfactie (het hele
  huishouden deelt één gegevensset).

## Volgende stap (later): pushmeldingen

Echte pushmeldingen bij gesloten app ("Paracetamol verloopt morgen") kunnen
met een Supabase **Edge Function + cron** die Web Push-berichten verstuurt.
Dat is een losse klus met eigen sleutelbeheer (VAPID) — logisch om op te
pakken zodra de sync in gebruik is.
