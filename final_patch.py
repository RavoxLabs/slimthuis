#!/usr/bin/env python3
src = open('index.html', encoding='utf-8').read()

# ================================================================
# 1) CSS — donkere modus + instellingen-knop + import/export UI
# ================================================================
css_root = """  :root {
    --bg: #F5F2EC;
    --bg2: #EDEAE2;
    --surface: #FFFFFF;
    --border: rgba(0,0,0,0.10);
    --border2: rgba(0,0,0,0.16);
    --text: #1A1A16;
    --text2: #6B6860;
    --text3: #9A9890;
    --green: #3B6D11;
    --green-bg: #EAF3DE;
    --amber: #854F0B;
    --amber-bg: #FAEEDA;
    --red: #A32D2D;
    --red-bg: #FCEBEB;
    --blue: #185FA5;
    --blue-bg: #E6F1FB;
    --radius: 12px;
    --radius-sm: 8px;
  }"""
dark_css = css_root + """

  /* DONKERE MODUS */
  [data-theme="dark"] {
    --bg: #18181B;
    --bg2: #27272A;
    --surface: #1F1F22;
    --border: rgba(255,255,255,0.08);
    --border2: rgba(255,255,255,0.14);
    --text: #F4F4F5;
    --text2: #A1A1AA;
    --text3: #71717A;
    --green: #7FC654;
    --green-bg: #1C2E14;
    --amber: #F5A623;
    --amber-bg: #2E2208;
    --red: #F87171;
    --red-bg: #2E1515;
    --blue: #60A5FA;
    --blue-bg: #172035;
  }

  /* INSTELLINGEN-KNOP IN HEADER */
  .header-btn {
    width: 36px; height: 36px;
    border: none; background: transparent; cursor: pointer;
    color: var(--text3); display: flex; align-items: center;
    justify-content: center; border-radius: 8px; transition: color 0.15s;
    flex-shrink: 0;
  }
  .header-btn:hover { color: var(--text); }
  .header-btn svg { width: 18px; height: 18px; stroke: currentColor; fill: none; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }

  /* INSTELLINGEN DRAWER */
  .drawer-overlay {
    position: fixed; inset: 0; background: rgba(0,0,0,0.45);
    z-index: 400; display: none; align-items: flex-end;
  }
  .drawer-overlay.open { display: flex; }
  .drawer {
    background: var(--surface); border-radius: 20px 20px 0 0;
    width: 100%; max-width: 480px; margin: 0 auto;
    padding: 8px 0 env(safe-area-inset-bottom, 16px);
    animation: slideUp 0.22s ease;
  }
  @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
  .drawer-handle { width: 36px; height: 4px; background: var(--border2); border-radius: 2px; margin: 10px auto 16px; }
  .drawer-titel { font-size: 15px; font-weight: 500; color: var(--text); padding: 0 20px 14px; border-bottom: 0.5px solid var(--border); }
  .drawer-rij {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 20px; border-bottom: 0.5px solid var(--border);
    cursor: pointer;
  }
  .drawer-rij:last-child { border-bottom: none; }
  .drawer-rij svg { width: 18px; height: 18px; stroke: var(--text2); fill: none; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0; }
  .drawer-body { flex: 1; }
  .drawer-naam { font-size: 14px; color: var(--text); }
  .drawer-sub { font-size: 12px; color: var(--text3); margin-top: 1px; }

  /* TOGGLE SCHAKELAAR */
  .toggle {
    width: 44px; height: 26px; background: var(--bg2);
    border-radius: 13px; position: relative; flex-shrink: 0;
    transition: background 0.2s; cursor: pointer; border: none;
  }
  .toggle.aan { background: var(--green); }
  .toggle::after {
    content: ''; position: absolute; top: 3px; left: 3px;
    width: 20px; height: 20px; border-radius: 50%;
    background: #fff; transition: transform 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.2);
  }
  .toggle.aan::after { transform: translateX(18px); }

  /* EXPORT/IMPORT KNOPPEN */
  .io-knoppen { display: flex; gap: 8px; padding: 14px 20px 0; }
  .io-knoppen button {
    flex: 1; padding: 11px; border-radius: var(--radius-sm);
    font-family: inherit; font-size: 13px; cursor: pointer; border: 1px solid var(--border2);
    background: var(--surface); color: var(--text2); transition: all 0.15s;
  }
  .io-knoppen button:hover { border-color: var(--green); color: var(--green); }
  .io-sub { font-size: 11px; color: var(--text3); padding: 6px 20px 14px; line-height: 1.5; }"""
assert css_root in src
src = src.replace(css_root, dark_css, 1)

# Donkere modus ook voor QR-modal inner (altijd licht voor printen)
src = src.replace(
    "  .qr-inner {\n    background: #fff; border-radius: var(--radius); padding: 24px;",
    "  .qr-inner {\n    background: #fff; color: #1A1A16; border-radius: var(--radius); padding: 24px;"
)

# ================================================================
# 2) HTML — instellingen-knop in header, drawer na body
# ================================================================
oud_header = """<div class="header">
  <div class="logo">Slim<span>Thuis</span></div>
  <div class="header-date" id="headerDate"></div>
</div>"""
nieuw_header = """<div class="header">
  <div class="logo">Slim<span>Thuis</span></div>
  <div class="header-date" id="headerDate"></div>
  <button class="header-btn" onclick="openInstellingen()" aria-label="Instellingen">
    <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
  </button>
</div>"""
assert oud_header in src
src = src.replace(oud_header, nieuw_header, 1)

# Drawer vóór de toast
toast_anchor = '<div class="toast" id="toast"></div>'
drawer = """<div class="drawer-overlay" id="instellingenDrawer" onclick="sluitInstellingen(event)">
  <div class="drawer">
    <div class="drawer-handle"></div>
    <div class="drawer-titel">Instellingen</div>

    <div class="drawer-rij" onclick="toggleDonker()">
      <svg viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      <div class="drawer-body">
        <div class="drawer-naam">Donkere modus</div>
        <div class="drawer-sub">Volgt je systeeminstelling, of handmatig instellen</div>
      </div>
      <button class="toggle" id="donkerToggle" onclick="event.stopPropagation(); toggleDonker()"></button>
    </div>

    <div class="io-knoppen">
      <button onclick="exportData()">
        ↑ Back-up exporteren
      </button>
      <button onclick="document.getElementById('importInput').click()">
        ↓ Back-up importeren
      </button>
    </div>
    <div class="io-sub">Exporteer al je gegevens als één JSON-bestand. Handy bij een nieuwe telefoon of browser, of als je de data wil overzetten naar een huisgenoot.</div>
    <input type="file" id="importInput" accept=".json" style="display:none" onchange="importData(event)">

    <div class="drawer-rij" onclick="if(confirm('Wil je echt alle gegevens wissen? Dit kan niet ongedaan worden gemaakt.')) resetAlles()">
      <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/></svg>
      <div class="drawer-body">
        <div class="drawer-naam" style="color:var(--red)">Alle gegevens wissen</div>
        <div class="drawer-sub">Voorraad, noodpakket, noodplan en instellingen</div>
      </div>
    </div>

    <div class="io-sub" style="padding-top:10px">SlimThuis v3 · Alle gegevens staan uitsluitend op dit apparaat.<br>Bron noodpakket: denkvooruit.nl (Rijksoverheid)</div>
  </div>
</div>
""" + toast_anchor
assert toast_anchor in src
src = src.replace(toast_anchor, drawer, 1)

# ================================================================
# 3) JS — donkere modus + export/import + instellingen-drawer
# ================================================================
fn_anchor = "function setHeaderDate() {"
io_js = r"""// ---- DONKERE MODUS ----
let donkerVoorkeur = localStorage.getItem('slimthuis_thema'); // 'licht' | 'donker' | null

function pasDonkerToe(animatie) {
  const systeemDonker = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const donker = donkerVoorkeur === 'donker' || (donkerVoorkeur !== 'licht' && systeemDonker);
  document.documentElement.setAttribute('data-theme', donker ? 'dark' : 'light');
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = donker ? '#18181B' : '#F5F2EC';
  const tog = document.getElementById('donkerToggle');
  if (tog) tog.classList.toggle('aan', donker);
}

function toggleDonker() {
  const huidig = document.documentElement.getAttribute('data-theme') === 'dark';
  donkerVoorkeur = huidig ? 'licht' : 'donker';
  localStorage.setItem('slimthuis_thema', donkerVoorkeur);
  pasDonkerToe();
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
  if (!donkerVoorkeur) pasDonkerToe();
});

// ---- INSTELLINGEN-DRAWER ----
function openInstellingen() {
  pasDonkerToe();
  document.getElementById('instellingenDrawer').classList.add('open');
}
function sluitInstellingen(e) {
  if (e.target === document.getElementById('instellingenDrawer')) {
    document.getElementById('instellingenDrawer').classList.remove('open');
  }
}

// ---- EXPORT / IMPORT ----
const BACKUP_VERSIE = 3;

function exportData() {
  const data = {
    versie: BACKUP_VERSIE,
    exportDatum: new Date().toISOString(),
    producten,
    npChecked: [...npChecked],
    huishouden,
    eigenNummers,
    noodplan,
    checks,
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `slimthuis-backup-${new Date().toISOString().slice(0,10)}.json`;
  a.click();
  URL.revokeObjectURL(a.href);
  showToast('Back-up geëxporteerd');
}

function importData(e) {
  const bestand = e.target.files[0];
  if (!bestand) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    try {
      const d = JSON.parse(ev.target.result);
      if (!d.versie || !d.exportDatum) throw new Error('Ongeldig bestand');

      if (!confirm(`Back-up van ${new Date(d.exportDatum).toLocaleDateString('nl-NL')} importeren?\n\nJe huidige gegevens worden overschreven.`)) return;

      if (Array.isArray(d.producten)) {
        producten = d.producten;
        localStorage.setItem('slimthuis_producten', JSON.stringify(producten));
      }
      if (Array.isArray(d.npChecked)) {
        npChecked = new Set(d.npChecked);
        localStorage.setItem('slimthuis_noodpakket', JSON.stringify(d.npChecked));
      }
      if (d.huishouden) {
        huishouden = d.huishouden;
        localStorage.setItem('slimthuis_huishouden', JSON.stringify(huishouden));
      }
      if (d.eigenNummers) {
        eigenNummers = d.eigenNummers;
        localStorage.setItem('slimthuis_nummers', JSON.stringify(eigenNummers));
      }
      if (d.noodplan) {
        noodplan = d.noodplan;
        localStorage.setItem('slimthuis_noodplan', JSON.stringify(noodplan));
      }
      if (d.checks) {
        checks = d.checks;
        localStorage.setItem('slimthuis_checks', JSON.stringify(checks));
      }

      renderProducten(); updateStats(); renderTodayAlerts();
      renderNoodpakket(); renderNoodplan(); renderScore();
      document.getElementById('instellingenDrawer').classList.remove('open');
      showToast('Back-up geïmporteerd ✓');
    } catch (err) {
      showToast('Importeren mislukt — controleer het bestand');
    }
    e.target.value = '';
  };
  reader.readAsText(bestand);
}

function resetAlles() {
  ['slimthuis_producten','slimthuis_noodpakket','slimthuis_huishouden',
   'slimthuis_nummers','slimthuis_noodplan','slimthuis_checks','slimthuis_thema',
   'slimthuis_sync'].forEach(k => localStorage.removeItem(k));
  location.reload();
}

function setHeaderDate() {"""
assert fn_anchor in src
src = src.replace(fn_anchor, io_js, 1)

# pasDonkerToe aanroepen bij init
init_anchor = "setHeaderDate();"
assert init_anchor in src
src = src.replace(init_anchor, "pasDonkerToe();\nsetHeaderDate();", 1)

open('index.html', 'w', encoding='utf-8').write(src)
print("Patch klaar")
