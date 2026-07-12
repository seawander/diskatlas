/* diskatlas service worker — makes the atlas load instantly on repeat visits
 * and work fully offline once cached. Lives at the repo root so its scope
 * covers the whole site (a SW can only control paths at or below its own URL).
 *
 * No-op under file:// — registration is guarded in index.html, and browsers
 * don't expose service workers there anyway, so double-click use is unaffected.
 *
 * Strategy:
 *   - images/*  -> cache-first  (crops are effectively immutable; large; loaded
 *                  on demand in the detail panel — cache them as they're viewed)
 *   - shell     -> stale-while-revalidate (html/css/js/data/icons): serve the
 *                  cached copy instantly, refresh from network in the background
 *                  so new code and freshly-built data.js are picked up next load.
 *
 * Bump VERSION whenever this file's caching logic changes to force a clean slate.
 */
var VERSION = 'diskatlas-v1';
var SHELL = VERSION + '-shell';
var IMGS = VERSION + '-img';

var SHELL_ASSETS = [
  './',
  './index.html',
  './frontend/style.css',
  './frontend/data.js',
  './frontend/constellations.js',
  './frontend/i18n.js',
  './frontend/app.js',
  './frontend/site.webmanifest',
  './frontend/logo.svg',
  './frontend/favicon.png',
  './frontend/apple-touch-icon.png'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(SHELL)
      .then(function (c) { return c.addAll(SHELL_ASSETS); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== SHELL && k !== IMGS) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // never touch cross-origin

  if (url.pathname.indexOf('/images/') !== -1) {
    e.respondWith(cacheFirst(req, IMGS));
  } else {
    e.respondWith(staleWhileRevalidate(req, SHELL));
  }
});

function cacheFirst(req, cacheName) {
  return caches.open(cacheName).then(function (cache) {
    return cache.match(req).then(function (hit) {
      return hit || fetch(req).then(function (res) {
        if (res && res.ok) cache.put(req, res.clone());
        return res;
      });
    });
  });
}

function staleWhileRevalidate(req, cacheName) {
  return caches.open(cacheName).then(function (cache) {
    return cache.match(req).then(function (hit) {
      var net = fetch(req).then(function (res) {
        if (res && res.ok) cache.put(req, res.clone());
        return res;
      }).catch(function () { return hit; });
      return hit || net;
    });
  });
}
