/**
 * Aku Fashion Service Worker
 * ==========================
 * Provides offline-first caching for the fashion app.
 *
 * Strategy:
 * - App shell (HTML/CSS/JS): Cache-first
 * - API calls: Network-first with fallback to cached responses
 * - Tutor conversations: Queue offline requests for later sync
 */

const CACHE_NAME = 'aku-fashion-v1'
const API_CACHE_NAME = 'aku-fashion-api-v1'

// App shell files to pre-cache
const PRECACHE_URLS = [
  '/',
  '/tutor',
  '/copilot',
  '/design',
  '/skills',
  '/gallery',
]

// Install: pre-cache app shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Pre-caching app shell')
      return cache.addAll(PRECACHE_URLS)
    }).then(() => self.skipWaiting())
  )
})

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(
        names
          .filter((name) => name !== CACHE_NAME && name !== API_CACHE_NAME)
          .map((name) => caches.delete(name))
      )
    ).then(() => self.clients.claim())
  )
})

// Fetch: intercept requests
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  // Skip non-GET requests to external origins
  if (request.method !== 'GET' && !url.pathname.startsWith('/api/')) {
    return
  }

  // API routes: network-first, cache fallback
  if (url.pathname.startsWith('/api/')) {
    if (request.method !== 'GET') return  // Let POST API calls through

    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response.ok) {
            const clone = response.clone()
            caches.open(API_CACHE_NAME).then((cache) => cache.put(request, clone))
          }
          return response
        })
        .catch(() =>
          caches.match(request).then((cached) =>
            cached ?? new Response(
              JSON.stringify({ error: 'offline', text: 'You are offline. Request queued for sync.' }),
              { headers: { 'Content-Type': 'application/json' } }
            )
          )
        )
    )
    return
  }

  // App shell: cache-first
  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached
      return fetch(request).then((response) => {
        if (response.ok && response.type === 'basic') {
          const clone = response.clone()
          caches.open(CACHE_NAME).then((cache) => cache.put(request, clone))
        }
        return response
      })
    })
  )
})

// Background sync (when supported)
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-offline-queue') {
    event.waitUntil(syncOfflineQueue())
  }
})

async function syncOfflineQueue() {
  console.log('[SW] Syncing offline queue...')
  // Notify all clients to flush their queue
  const clients = await self.clients.matchAll()
  clients.forEach((client) => client.postMessage({ type: 'SYNC_QUEUE' }))
}
