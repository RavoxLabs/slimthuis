#!/usr/bin/env python3
src = open('index.html', encoding='utf-8').read()

# ================================================================
# 1) CSS
# ================================================================
css_anchor = "  /* SYNC */"
css_new = """  /* QR-STICKERS */
  .qr-modal {
    position: fixed; inset: 0; background: rgba(20,19,16,0.88);
    display: none; align-items: center; justify-content: center;
    z-index: 300; padding: 20px;
  }
  .qr-modal.open { display: flex; }
  .qr-inner {
    background: #fff; border-radius: var(--radius); padding: 24px;
    width: 100%; max-width: 360px; text-align: center;
  }
  .qr-inner h3 { font-size: 16px; margin-bottom: 4px; color: #1A1A16; }
  .qr-naam { font-size: 13px; color: #6B6860; margin-bottom: 16px; }
  .qr-canvas { display: block; margin: 0 auto 16px; }
  .qr-acties { display: flex; gap: 8px; }
  .qr-acties button {
    flex: 1; border: none; padding: 11px; border-radius: var(--radius-sm);
    font-family: inherit; font-size: 13px; cursor: pointer;
  }
  .qr-dl { background: var(--green); color: #fff; }
  .qr-sl { background: var(--bg2); color: var(--text2); }
  .qr-knop {
    width: 32px; height: 32px; border: none; background: transparent;
    cursor: pointer; color: var(--text3); flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    border-radius: 6px; transition: color 0.15s;
  }
  .qr-knop:hover { color: var(--text); }
  .qr-knop svg { width: 15px; height: 15px; stroke: currentColor; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }

  /* ZOEKBALK */
  .zoek-wrap { padding: 0 0 10px; position: relative; }
  .zoek-wrap input {
    width: 100%; padding: 11px 38px 11px 14px;
    border: 1px solid var(--border); border-radius: var(--radius-sm);
    font-family: inherit; font-size: 14px; background: var(--surface);
    color: var(--text);
  }
  .zoek-wrap input:focus { outline: none; border-color: var(--border2); }
  .zoek-wrap svg {
    position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
    width: 16px; height: 16px; stroke: var(--text3); fill: none;
    stroke-width: 2; stroke-linecap: round; pointer-events: none;
  }
  .zoek-leeg { font-size: 14px; color: var(--text3); text-align: center; padding: 24px 16px; }

  /* PRINT */
  @media print {
    body > *:not(#print-overlay) { display: none !important; }
    #print-overlay { display: block !important; }
  }
  #print-overlay {
    display: none;
    font-family: 'DM Sans', sans-serif;
    color: #1A1A16;
    padding: 20px;
    max-width: 600px;
    margin: 0 auto;
  }
  .print-titel { font-size: 22px; font-weight: 500; margin-bottom: 4px; }
  .print-sub { font-size: 12px; color: #6B6860; margin-bottom: 18px; }
  .print-groep { font-size: 11px; font-weight: 500; text-transform: uppercase;
    letter-spacing: 0.08em; color: #9A9890; margin: 14px 0 6px; border-top: 1px solid #E8E5DD; padding-top: 10px; }
  .print-item { display: flex; align-items: flex-start; gap: 10px; padding: 6px 0;
    border-bottom: 0.5px solid #E8E5DD; }
  .print-item:last-child { border-bottom: none; }
  .print-box { width: 16px; height: 16px; border: 1.5px solid #9A9890; border-radius: 4px; flex-shrink: 0; margin-top: 1px; }
  .print-body { flex: 1; }
  .print-naam { font-size: 13px; }
  .print-hint { font-size: 11px; color: #9A9890; margin-top: 1px; }
  .print-footer { font-size: 10px; color: #9A9890; margin-top: 18px; border-top: 1px solid #E8E5DD; padding-top: 8px; }

  /* SYNC */"""
assert css_anchor in src
src = src.replace(css_anchor, css_new, 1)

# ================================================================
# 2) HTML: QR-knopje in product-rij, zoekbalk in Noodgids,
#    QR-modal, print-overlay, print-knop in noodpakket
# ================================================================

# QR-knopje toevoegen in elke product-rij (vóór de delete-knop)
oud_rij = """      <div class="product-date">${p.datum ? formatDate(p.datum) : '—'}</div>
      <button class="product-delete" onclick="deleteProduct(${idx})" title="Verwijderen">"""
nieuw_rij = """      <div class="product-date">${p.datum ? formatDate(p.datum) : '—'}</div>
      <button class="qr-knop" onclick="event.stopPropagation(); openQR(${idx})" title="QR-sticker">
        <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 14h3v3h-3zM17 17h3v3h-3zM14 20h3"/></svg>
      </button>
      <button class="product-delete" onclick="event.stopPropagation(); deleteProduct(${idx})" title="Verwijderen">"""
assert oud_rij in src
src = src.replace(oud_rij, nieuw_rij, 1)

# Zoekbalk in de Noodgids (vóór de ehboList)
oud_ehbo_html = """    <div id="ehboList"></div>
    <div id="ehboDetail" class="ehbo-detail"></div>"""
nieuw_ehbo_html = """    <div class="zoek-wrap">
      <input type="search" id="noodgidsZoek" placeholder="Zoek in de noodgids…" oninput="filterNoodgids(this.value)">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
    </div>
    <div id="ehboList"></div>
    <div id="ehboDetail" class="ehbo-detail"></div>"""
assert oud_ehbo_html in src
src = src.replace(oud_ehbo_html, nieuw_ehbo_html, 1)

# Print-knop in noodpakket (na de progress-kaart, vóór de lijst)
oud_np = """    <div id="noodpakketList"></div>
    <div class="ehbo-note">"""
nieuw_np = """    <div id="noodpakketList"></div>
    <div style="padding: 0 0 4px;">
      <button class="scan-btn" onclick="printChecklist()" style="margin-bottom:0">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
        Afdrukken / opslaan als PDF
      </button>
    </div>
    <div class="ehbo-note">"""
assert oud_np in src
src = src.replace(oud_np, nieuw_np, 1)

# QR-modal (vóór de scan-modal)
scan_modal_anchor = '<div class="scan-modal" id="scanModal">'
qr_modal = """<div class="qr-modal" id="qrModal">
  <div class="qr-inner">
    <h3>QR-sticker</h3>
    <div class="qr-naam" id="qrNaam"></div>
    <canvas class="qr-canvas" id="qrCanvas" width="200" height="200"></canvas>
    <div class="qr-acties">
      <button class="qr-dl" onclick="downloadQR()">Opslaan als PNG</button>
      <button class="qr-sl" onclick="sluitQR()">Sluiten</button>
    </div>
  </div>
</div>
""" + scan_modal_anchor
assert scan_modal_anchor in src
src = src.replace(scan_modal_anchor, qr_modal, 1)

# Print-overlay (voor de toast)
toast_anchor = '<div class="toast" id="toast"></div>'
print_overlay = """<div id="print-overlay">
  <div class="print-titel">SlimThuis — Noodpakket-checklist</div>
  <div class="print-sub" id="printDatum"></div>
  <div id="printBody"></div>
  <div class="print-footer">Bron: Denkvooruit.nl (Rijksoverheid) · Controleer elk half jaar op volledigheid en houdbaarheid · slimthuis.app</div>
</div>
""" + toast_anchor
assert toast_anchor in src
src = src.replace(toast_anchor, print_overlay, 1)

open('index.html', 'w', encoding='utf-8').write(src)
print("Deel 1 (CSS + HTML) klaar")
