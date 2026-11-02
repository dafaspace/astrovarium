/* The bridge's service worker, under the old worker's name so every installed
   copy of the old app finds it at its next check and is replaced by it. It
   deletes the old app's caches and keeps only this page, so the bridge opens
   offline too: the charts stored here can still be saved as a file without a
   connection. */
const CACHE = 'astrotrip-bridge-1';
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(['./', './manifest.json'])).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  /* Every page of the old app, index.html or a deep link, is the bridge now. */
  if (req.mode === 'navigate') {
    e.respondWith(fetch('./').then(res => {
      if (res.ok) { const c = res.clone(); e.waitUntil(caches.open(CACHE).then(x => x.put('./', c))); }
      return res;
    }).catch(() => caches.match('./')));
    return;
  }
  e.respondWith(fetch(req).catch(() => caches.match(req)));
});
