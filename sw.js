const CACHE_NAME = 'zb-wcrep-v1.0.1'; // Increment this string to force android update cascades!

const CORE_ASSETS = [
  '/zbrepository/', // Cache the root scope directly
  '/zbrepository/index.html',
  '/zbrepository/zb_poatharry.html',
  '/zbrepository/zb_poatharry.json',
  '/zbrepository/zb_runher.html',
  '/zbrepository/zb_askey.html',
  '/zbrepository/zb_voiceme.html',
  '/zbrepository/zb_wc_anime.html',
  '/zbrepository/img/zb_repicon_192.png',
  '/zbrepository/img/zb_repicon_512.png'
];

// 1. Install - Populate core application Shell assets
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('SW: Pre-caching Core Shell App assets');
      return cache.addAll(CORE_ASSETS);
    })
  );
  self.skipWaiting(); // Forces the waiting service worker to activate immediately
});

// 2. Activate - Crucial cleanup loop to delete older cache layers
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('SW: Purging legacy cache container:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim()) // Takes control of all open pages immediately
  );
});

// 3. Fetch Strategy
self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      const networkFetch = fetch(e.request).then((networkResponse) => {
        // Validate valid server response before processing caching layers
        if (networkResponse && networkResponse.status === 200) {
          const url = e.request.url;

          // Dynamic tracking: Cache text fields, runtime scripts, or data objects on the fly
          if (url.includes('/oldtxt/') || url.includes('/txt/') || url.endsWith('.json') || url.endsWith('.txt')) {
            const cacheCopy = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(e.request, cacheCopy);
            });
          }
        }
        return networkResponse;
      }).catch(() => cachedResponse);

      // Return local memory instantly for speed performance optimization, fallback onto live request streams
      return cachedResponse || networkFetch;
    })
  );
});