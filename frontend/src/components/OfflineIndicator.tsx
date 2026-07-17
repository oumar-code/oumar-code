'use client'

import { useEffect, useState } from 'react'
import { WifiOff } from 'lucide-react'

export function OfflineIndicator() {
  const [isOffline, setIsOffline] = useState(false)
  const [queuedCount, setQueuedCount] = useState(0)

  useEffect(() => {
    const updateStatus = () => setIsOffline(!navigator.onLine)
    window.addEventListener('online', updateStatus)
    window.addEventListener('offline', updateStatus)
    updateStatus()
    return () => {
      window.removeEventListener('online', updateStatus)
      window.removeEventListener('offline', updateStatus)
    }
  }, [])

  // Listen for queued messages
  useEffect(() => {
    const handler = (e: CustomEvent) => setQueuedCount(e.detail.count)
    window.addEventListener('offline-queue-update' as any, handler)
    return () => window.removeEventListener('offline-queue-update' as any, handler)
  }, [])

  if (!isOffline) return null

  return (
    <div className="offline-badge">
      <WifiOff className="w-3.5 h-3.5" />
      <span>
        Offline mode
        {queuedCount > 0 && ` — ${queuedCount} queued`}
      </span>
    </div>
  )
}
