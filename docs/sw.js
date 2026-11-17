/* Old address only: replaces the calendar's old service worker, clears its saved copy and reloads the page,
   so the old app shows the "new home" card instead of the cached calendar. */
self.addEventListener('install',function(){self.skipWaiting()});
self.addEventListener('activate',function(e){e.waitUntil((async function(){
  for(const k of await caches.keys())await caches.delete(k);
  await self.registration.unregister();
  for(const c of await self.clients.matchAll({type:'window'}))try{c.navigate(c.url)}catch(x){}
})())});
