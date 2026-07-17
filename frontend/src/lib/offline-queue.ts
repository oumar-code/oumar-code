/**
 * Offline queue for the browser side.
 * Stores requests in localStorage when offline; syncs when online.
 */

import type { OfflineQueueItem } from '@/types'

const QUEUE_KEY = 'aku_offline_queue'

export function getQueue(): OfflineQueueItem[] {
  if (typeof window === 'undefined') return []
  try {
    return JSON.parse(localStorage.getItem(QUEUE_KEY) ?? '[]')
  } catch {
    return []
  }
}

export function enqueue(request_type: string, payload: Record<string, unknown>): OfflineQueueItem {
  const item: OfflineQueueItem = {
    id: crypto.randomUUID().slice(0, 8),
    request_type,
    payload,
    created_at: Date.now(),
    status: 'pending',
  }
  const queue = getQueue()
  queue.push(item)
  localStorage.setItem(QUEUE_KEY, JSON.stringify(queue))
  dispatchQueueUpdate(queue.filter(q => q.status === 'pending').length)
  return item
}

export function pendingCount(): number {
  return getQueue().filter(q => q.status === 'pending').length
}

export async function flushQueue(
  processorFn: (item: OfflineQueueItem) => Promise<unknown>
): Promise<number> {
  const queue = getQueue()
  const pending = queue.filter(q => q.status === 'pending')
  let done = 0

  for (const item of pending) {
    try {
      await processorFn(item)
      item.status = 'done'
      done++
    } catch {
      item.status = 'failed'
    }
  }

  localStorage.setItem(QUEUE_KEY, JSON.stringify(queue))
  dispatchQueueUpdate(queue.filter(q => q.status === 'pending').length)
  return done
}

function dispatchQueueUpdate(count: number) {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(
      new CustomEvent('offline-queue-update', { detail: { count } })
    )
  }
}
