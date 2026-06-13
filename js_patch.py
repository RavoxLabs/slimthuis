#!/usr/bin/env python3
src = open('index.html', encoding='utf-8').read()

# ================================================================
# 3) Drie nieuwe scenario's invoegen (voor de sluitende ];)
# ================================================================
scen_anchor = "];\n\nconst SVG_HARTSTILSTAND"
nieuwe_scenarios = r"""  {
    naam: 'Gaslek',
    alarm: true,
    svg: `<svg viewBox="0 0 320 150" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#1A1A16" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
      <path d="M84 128 V72 L160 30 L236 72 V128 Z"/>
      <path d="M70 80 L160 28 L250 80"/>
      <line x1="60" y1="128" x2="260" y2="128" stroke="#9A9890" stroke-width="2"/>
      <path d="M144 62 q5 9 0 18 M160 58 q5 10 0 20 M176 62 q5 9 0 18" stroke="#EF9F27" stroke-width="2.5"/>
      <circle cx="160" cy="98" r="12" stroke="#E24B4A" stroke-width="2.5"/>
      <line x1="154" y1="92" x2="166" y2="104" stroke="#E24B4A" stroke-width="2.5"/>
      <line x1="166" y1="92" x2="154" y2="104" stroke="#E24B4A" stroke-width="2.5"/>
    </svg>`,
    stappen: [
      'Ruik je gas? Doe direct: ramen en deuren open, geen elektra aanraken (schakelaar, telefoon, bel, lichtknop) — ook niet uitdoen als ze al aan zijn.',
      'Draai de gasafsluiter dicht — die zit bij de gasmeter. Een kwartslag draaien volstaat.',
      'Verlaat de woning en neem anderen mee. Doe de voordeur achter je dicht maar op de knip, niet op slot.',
      'Bel buiten of op afstand de Gaslekkage-lijn van Enexis of je eigen netbeheerder: 0800-9009 (dag en nacht gratis). Bij acuut gevaar bel je 112.',
      'Ga niet terug naar binnen tot de netbeheerder heeft gezegd dat het veilig is.',
      'Steek geen vlam aan en rook niet in de buurt van het pand.',
    ]
  },
  {
    naam: 'Overstroming',
    svg: `<svg viewBox="0 0 320 150" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#1A1A16" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
      <path d="M84 116 V68 L160 26 L236 68 V116 Z"/>
      <path d="M70 74 L160 22 L250 74"/>
      <line x1="40" y1="130" x2="280" y2="130" stroke="#185FA5" stroke-width="3"/>
      <path d="M40 120 q20 -10 40 0 q20 10 40 0 q20 -10 40 0 q20 10 40 0 q20 -10 40 0" stroke="#185FA5" stroke-width="2.5"/>
      <path d="M240 84 h32 M248 74 l-8 10 M248 94 l-8 -10" stroke="#639922" stroke-width="2.5"/>
    </svg>`,
    stappen: [
      'Volg NL-Alert en de berichten van de regionale rampenzender (Omroep Brabant). Volg altijd de instructies van de hulpdiensten op.',
      'Komt er een evacuatie? Neem je noodpakket mee, sluit gas, water en elektra af en ga naar de afgesproken ontmoetingsplek.',
      'Kom je niet weg? Ga naar de hoogste verdieping. Stuur een bericht naar je noodcontact met je locatie.',
      'Raak geen overstroomd water aan — het kan besmet zijn met riool, chemicaliën of stroom bevatten.',
      'Schakel de elektriciteit uit bij de meterkast als er water in de buurt van stopcontacten of apparaten komt.',
      'Laat na de overstroming een expert de woning controleren voordat je terugkeert — er kunnen constructieschade of gaslekkages zijn.',
    ]
  },
  {
    naam: 'Strenge vorst',
    svg: `<svg viewBox="0 0 320 150" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#1A1A16" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
      <line x1="160" y1="18" x2="160" y2="132"/>
      <line x1="160" y1="75" x2="136" y2="51"/>
      <line x1="160" y1="75" x2="184" y2="51"/>
      <line x1="160" y1="75" x2="136" y2="99"/>
      <line x1="160" y1="75" x2="184" y2="99"/>
      <line x1="120" y1="75" x2="200" y2="75"/>
      <circle cx="160" cy="18" r="5" fill="#185FA5" stroke="#185FA5"/>
      <circle cx="160" cy="132" r="5" fill="#185FA5" stroke="#185FA5"/>
      <circle cx="120" cy="75" r="5" fill="#185FA5" stroke="#185FA5"/>
      <circle cx="200" cy="75" r="5" fill="#185FA5" stroke="#185FA5"/>
      <circle cx="136" cy="51" r="4" fill="#185FA5" stroke="#185FA5"/>
      <circle cx="184" cy="51" r="4" fill="#185FA5" stroke="#185FA5"/>
      <circle cx="136" cy="99" r="4" fill="#185FA5" stroke="#185FA5"/>
      <circle cx="184" cy="99" r="4" fill="#185FA5" stroke="#185FA5"/>
    </svg>`,
    stappen: [
      'Houd de verwarming op minimaal 15–16°C, ook in slaapkamers — onderkoeling is gevaarlijk voor ouderen en jonge kinderen.',
      'Laat bij strenge vorst een kleine druppel water lopen in ruimtes met buitenmuren — dit voorkomt bevroren leidingen.',
      'Zijn leidingen toch bevroren? Warm ze langzaam op met lauw water of een warmwaterkruik. Gebruik nooit een open vlam.',
      'Controleer buren en familie die kwetsbaar zijn of alleen wonen.',
      'Ga niet de weg op als dat niet nodig is. Zijn winterbanden verplicht? In Nederland niet, maar ze kunnen levensreddend zijn bij ijzel.',
      'Zorg voor voldoende verwarming, warme kleding, dekens en warm eten in je noodpakket.',
    ]
  },
];

const SVG_HARTSTILSTAND"""
assert scen_anchor in src
src = src.replace(scen_anchor, nieuwe_scenarios, 1)

# ================================================================
# 4) QR-generator + filter-zoekbalk + print-functie
# ================================================================
fn_anchor = "function setHeaderDate() {"

qr_js = r"""// ---- QR-STICKERS ----
function qrTekenPixel(ctx, x, y, size, cellSize) {
  ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
}

// Kleine zelfstandige QR-encoder voor URL's (versie 2, ECC M)
// We genereren de link slimthuis://product/<id> en coderen die als QR
function maakQRData(text) {
  // Gebruik de qrcode-bibliotheek als die geladen is, anders eigen mini-encoder
  if (window.QRCode) return null; // laten we via library doen
  return text; // fallback tekst
}

function tekenQRCanvas(canvas, tekst) {
  const ctx = canvas.getContext('2d');
  const n = 200;
  ctx.clearRect(0, 0, n, n);
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, n, n);

  if (window.QRCode) {
    // qrcode.js beschikbaar
    try {
      const qr = window.QRCode.create(tekst, { errorCorrectionLevel: 'M' });
      const modules = qr.modules;
      const size = modules.size;
      const cell = Math.floor((n - 16) / size);
      const off = Math.floor((n - size * cell) / 2);
      ctx.fillStyle = '#1A1A16';
      for (let r = 0; r < size; r++) {
        for (let c = 0; c < size; c++) {
          if (modules.get(r, c)) ctx.fillRect(off + c * cell, off + r * cell, cell, cell);
        }
      }
      return;
    } catch(e) {}
  }

  // Fallback: visueel blok met tekst (toont aan dat de lib niet geladen is)
  ctx.fillStyle = '#E8E5DD';
  ctx.fillRect(8, 8, n - 16, n - 16);
  ctx.fillStyle = '#1A1A16';
  ctx.font = 'bold 11px DM Sans, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('QR', n / 2, n / 2 - 6);
  ctx.font = '9px DM Sans, sans-serif';
  ctx.fillText('(kijk zonder internet:', n / 2, n / 2 + 10);
  ctx.fillText('voer ID handmatig in)', n / 2, n / 2 + 22);
}

let qrProductIdx = null;

function laadQRLib() {
  return new Promise((ok) => {
    if (window.QRCode) return ok();
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/qrcode/build/qrcode.min.js';
    s.onload = ok; s.onerror = ok; // doorgaan ook zonder
    document.head.appendChild(s);
  });
}

async function openQR(idx) {
  qrProductIdx = idx;
  const p = producten[idx];
  if (!p) return;
  document.getElementById('qrNaam').textContent = p.naam;
  document.getElementById('qrModal').classList.add('open');
  await laadQRLib();
  const tekst = `slimthuis://product/${p.id}?naam=${encodeURIComponent(p.naam)}&cat=${encodeURIComponent(p.categorie)}`;
  tekenQRCanvas(document.getElementById('qrCanvas'), tekst);
}

function sluitQR() {
  document.getElementById('qrModal').classList.remove('open');
  qrProductIdx = null;
}

function downloadQR() {
  const p = qrProductIdx !== null ? producten[qrProductIdx] : null;
  if (!p) return;
  const canvas = document.getElementById('qrCanvas');
  const link = document.createElement('a');
  link.download = `slimthuis-qr-${p.naam.replace(/[^a-z0-9]/gi, '-').toLowerCase()}.png`;

  // Maak een grotere versie (400×400) met productnaam erbij
  const big = document.createElement('canvas');
  big.width = 400; big.height = 460;
  const bctx = big.getContext('2d');
  bctx.fillStyle = '#fff';
  bctx.fillRect(0, 0, 400, 460);

  // Kopieer QR vergroot
  bctx.drawImage(canvas, 0, 0, 200, 200, 20, 20, 360, 360);

  // Productnaam en categorie
  bctx.fillStyle = '#1A1A16';
  bctx.font = 'bold 16px sans-serif';
  bctx.textAlign = 'center';
  const naamTekst = p.naam.length > 32 ? p.naam.slice(0, 32) + '…' : p.naam;
  bctx.fillText(naamTekst, 200, 408);
  bctx.fillStyle = '#9A9890';
  bctx.font = '13px sans-serif';
  bctx.fillText(p.categorie + (p.datum ? ' · THT ' + p.datum : ''), 200, 428);
  bctx.font = '11px sans-serif';
  bctx.fillText('SlimThuis', 200, 450);

  link.href = big.toDataURL('image/png');
  link.click();
}

// ---- NOODGIDS ZOEKBALK ----
function filterNoodgids(zoek) {
  const q = zoek.trim().toLowerCase();
  const list = document.getElementById('ehboList');
  const detail = document.getElementById('ehboDetail');
  if (detail.classList.contains('open')) closeEhbo();

  if (!q) { renderEhbo(); return; }

  const ehboTreffer = EHBO_DATA.map((item, i) => ({ item, i, type: 'ehbo' }))
    .filter(x => x.item.naam.toLowerCase().includes(q) ||
      x.item.stappen.some(s => (typeof s === 'string' ? s : s.tekst).toLowerCase().includes(q)));
  const scenTreffer = SCENARIO_DATA.map((item, i) => ({ item, i, type: 'scen' }))
    .filter(x => x.item.naam.toLowerCase().includes(q) ||
      x.item.stappen.some(s => s.toLowerCase().includes(q)));

  if (ehboTreffer.length === 0 && scenTreffer.length === 0) {
    list.innerHTML = `<div class="zoek-leeg">Geen resultaten voor "<strong>${zoek}</strong>"</div>`;
    return;
  }

  let html = '';
  if (ehboTreffer.length) {
    html += `<div class="section-label">EHBO</div><div class="card">`;
    ehboTreffer.forEach(({ item, i }) => {
      const kleur = item.urgentie === 'rood' ? '#E24B4A' : item.urgentie === 'oranje' ? '#EF9F27' : '#639922';
      html += `<div class="ehbo-item" onclick="openEhbo(${i})">
        <div class="urgency-dot" style="background:${kleur}"></div>
        <div class="ehbo-name">${item.naam}</div>
        <div class="ehbo-arrow"><svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg></div>
      </div>`;
    });
    html += '</div>';
  }
  if (scenTreffer.length) {
    html += `<div class="section-label">Scenario's</div><div class="card">`;
    scenTreffer.forEach(({ item, i }) => {
      html += `<div class="ehbo-item" onclick="openScenario(${i})">
        <div class="urgency-dot" style="background:#185FA5"></div>
        <div class="ehbo-name">${item.naam}</div>
        <div class="ehbo-arrow"><svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg></div>
      </div>`;
    });
    html += '</div>';
  }
  list.innerHTML = html;
}

// ---- PRINTBARE CHECKLIST ----
function printChecklist() {
  const personen = (huishouden.volw || 2) + (huishouden.kind || 0);
  const liter = personen * 3 * 3;
  const geld = (huishouden.volw || 2) * 70 + (huishouden.kind || 0) * 30;

  const subs = {
    water: `${liter} liter — 3 liter per persoon per dag, voor 3 dagen`,
    geld: `€ ${geld} — in verschillende biljetten en munten`,
  };

  const datum = new Date().toLocaleDateString('nl-NL', { day: 'numeric', month: 'long', year: 'numeric' });
  document.getElementById('printDatum').textContent =
    `Gegenereerd op ${datum} · ${huishouden.volw || 2} volwassenen, ${huishouden.kind || 0} kinderen, ${huishouden.dier || 0} huisdieren`;

  let html = '';
  NOODPAKKET_DATA.forEach(groep => {
    const zichtbaar = groep.items.filter(i =>
      !(i.id === 'huisdier' && (huishouden.dier || 0) === 0) &&
      !(i.id === 'baby' && (huishouden.kind || 0) === 0));
    if (!zichtbaar.length) return;
    html += `<div class="print-groep">${groep.categorie}</div>`;
    zichtbaar.forEach(item => {
      const sub = subs[item.id] || item.sub;
      const vinkje = npChecked.has(item.id)
        ? '<div class="print-box" style="background:#639922;border-color:#639922"></div>'
        : '<div class="print-box"></div>';
      html += `<div class="print-item">
        ${vinkje}
        <div class="print-body">
          <div class="print-naam">${item.naam}</div>
          ${sub ? `<div class="print-hint">${sub}</div>` : ''}
        </div>
      </div>`;
    });
  });

  document.getElementById('printBody').innerHTML = html;
  window.print();
}

function setHeaderDate() {"""
assert fn_anchor in src
src = src.replace(fn_anchor, qr_js, 1)

# ================================================================
# 5) Zoekbalk wissen bij tab-wissel
# ================================================================
oud_tab = """  if (tab === 'ehbo') { closeEhbo(); }"""
nieuw_tab = """  if (tab === 'ehbo') {
    closeEhbo();
    const zoek = document.getElementById('noodgidsZoek');
    if (zoek) { zoek.value = ''; renderEhbo(); }
  }"""
assert oud_tab in src
src = src.replace(oud_tab, nieuw_tab, 1)

open('index.html', 'w', encoding='utf-8').write(src)
print("Deel 2 (JS) klaar")
