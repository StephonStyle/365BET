const CACHE = '365BET-v3.12.08';
self.addEventListener('install',function(e){
  self.skipWaiting();
});
self.addEventListener('activate',function(e){
  e.waitUntil(
    caches.keys().then(function(ks){return Promise.all(ks.map(function(k){return caches.delete(k);}));})
    .then(function(){return clients.claim();})
  );
});
self.addEventListener('fetch',function(e){
  // Network first — always try server, fallback to cache if offline
  e.respondWith(
    fetch(e.request).catch(function(){return caches.match(e.request);})
  );
});
