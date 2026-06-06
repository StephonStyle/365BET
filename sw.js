const CACHE = '365BET-v2.2.70';
self.addEventListener('install',function(e){
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(['/365BET/']);}));
});
self.addEventListener('activate',function(e){
  e.waitUntil(
    caches.keys().then(function(ks){return Promise.all(ks.filter(function(k){return k!==CACHE;}).map(function(k){return caches.delete(k);}));})
    .then(function(){return clients.claim();})
  );
});
self.addEventListener('fetch',function(e){
  e.respondWith(
    caches.match(e.request).then(function(r){return r||fetch(e.request).then(function(r2){return caches.open(CACHE).then(function(c){c.put(e.request,r2.clone());return r2;});});})
  );
});
