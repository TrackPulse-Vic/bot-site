// // Cache name
// const CACHE_NAME = 'trackpulse-vic-cache-v1';

// // Files to cache
// const urlsToCache = [
//     '/',
//     '/web.html',
//     '/logs/viewer.html',
//     // Add any other assets you want to cache
// ];

// // Install event - cache files
// self.addEventListener('install', event => {
//     event.waitUntil(
//         caches.open(CACHE_NAME)
//             .then(cache => {
//                 return cache.addAll(urlsToCache);
//             })
//     );
// });

// // Fetch event - serve cached content when offline
// self.addEventListener('fetch', event => {
//     event.respondWith(
//         caches.match(event.request)
//             .then(response => {
//                 // Return cached response if found, otherwise fetch from network
//                 return response || fetch(event.request);
//             })
//     );
// });

// // Activate event - clean up old caches
// self.addEventListener('activate', event => {
//     const cacheWhitelist = [CACHE_NAME];
//     event.waitUntil(
//         caches.keys().then(cacheNames => {
//             return Promise.all(
//                 cacheNames.map(cacheName => {
//                     if (!cacheWhitelist.includes(cacheName)) {
//                         return caches.delete(cacheName);
//                     }
//                 })
//             );
//         })
//     );
// });