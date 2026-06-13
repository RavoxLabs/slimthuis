// SlimThuis service worker — maakt de app volledig offline bruikbaar.
// Nieuwe versie uitbrengen? Verhoog het versienummer hieronder.
const CACHE = 'slimthuis-v2';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './icon-512-maskable.png',
  './icon-180.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // Alleen GET-verzoeken cachen; API-verkeer (Supabase) altijd live
  if (e.request.method !== 'GET') return;
  if (url.hostname.includes('supabase.co') || url.hostname.includes('jsdelivr.net')) return;

  // Barcode-opzoekingen (Open Food Facts) altijd live — nooit cachen
  if (url.hostname.includes('openfoodfacts.org')) return;

  // Pagina-navigatie: eerst netwerk (zodat updates binnenkomen), offline terugvallen op cache
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request)
        .then((r) => {
          const kopie = r.clone();
          caches.open(CACHE).then((c) => c.put('./index.html', kopie));
          return r;
        })
        .catch(() => caches.match('./index.html'))
    );
    return;
  }

  // Overig (icons, lettertypen): eerst cache, anders netwerk en daarna bewaren
  e.respondWith(
    caches.match(e.request).then((hit) => {
      if (hit) return hit;
      return fetch(e.request).then((r) => {
        if (r.ok && (url.origin === location.origin || url.hostname.includes('fonts.g'))) {
          const kopie = r.clone();
          caches.open(CACHE).then((c) => c.put(e.request, kopie));
        }
        return r;
      });
    })
  );
});
