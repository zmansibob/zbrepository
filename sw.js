const CACHE_NAME = 'zb-wcrep-v1';

const CORE_ASSETS = [
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

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      const networkFetch = fetch(e.request).then((networkResponse) => {
        // Cache text files or JSON on the fly
        if (e.request.url.includes('/txt/') || e.request.url.includes('.json')) {
          const cacheCopy = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(e.request, cacheCopy);
          });
        }
        return networkResponse;
      }).catch(() => cachedResponse);

      // Return cache first for speed, but always fetch updates for content
      return cachedResponse || networkFetch;
    })
  );
});