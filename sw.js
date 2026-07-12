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
 *
 * Freshness: when the background revalidation of frontend/data.js brings back
 * a DIFFERENT version than the one just served from cache (the atlas redeploys
 * several times a day), the SW posts {type:'atlas-updated'} to all open pages;
 * app.js shows a localized "tap to reload" toast. Comparison uses the ETag /
 * Last-Modified validators, so it never happens on a first (uncached) load.
 */
var VERSION = 'diskatlas-v2';
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
        if (res && res.ok) {
          var fresher = hit && isDataJs(req) && validatorChanged(hit, res);
          var stored = cache.put(req, res.clone());
          if (fresher) stored.then(notifyClients);   // cache updated first, then toast
          /* the Pages deploy stamps asset URLs with ?v=<sha> (cache busting):
             drop entries for the SAME file under an older stamp, so the shell
             cache holds exactly one copy per asset instead of one per deploy */
          stored.then(function () { pruneStaleQueries(cache, req); });
        }
        return res;
      }).catch(function () { return hit; });
      return hit || net;
    });
  });
}

function isDataJs(req) {
  return new URL(req.url).pathname.indexOf('/frontend/data.js') !== -1;
}

/* Only claim "changed" when BOTH responses carry the same kind of validator
   and it differs — a missing header must never produce a false toast. */
function validatorChanged(oldRes, newRes) {
  var a = oldRes.headers.get('etag'), b = newRes.headers.get('etag');
  if (a && b) return a !== b;
  a = oldRes.headers.get('last-modified'); b = newRes.headers.get('last-modified');
  if (a && b) return a !== b;
  return false;
}

function notifyClients() {
  self.clients.matchAll({ type: 'window' }).then(function (cs) {
    cs.forEach(function (c) { c.postMessage({ type: 'atlas-updated' }); });
  });
}

function pruneStaleQueries(cache, req) {
  var url = new URL(req.url);
  cache.keys().then(function (keys) {
    keys.forEach(function (k) {
      var u = new URL(k.url);
      if (u.pathname === url.pathname && u.search !== url.search) cache.delete(k);
    });
  });
}
