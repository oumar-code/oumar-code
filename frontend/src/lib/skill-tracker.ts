/**
 * Skill tracker — browser-side localStorage persistence.
 */

import type { ProgressSummary, SkillData } from '@/types'

const SKILLS_KEY = 'aku_skills'
const LEARNER_ID_KEY = 'aku_learner_id'

export function getLearnerId(): string {
  if (typeof window === 'undefined') return 'guest'
  let id = localStorage.getItem(LEARNER_ID_KEY)
  if (!id) {
    id = 'learner-' + crypto.randomUUID().slice(0, 6)
    localStorage.setItem(LEARNER_ID_KEY, id)
  }
  return id
}

interface SkillStore {
  skill_log: Record<string, string[]>
  badges: string[]
  unlocked_levels: string[]
}

export function getStore(): SkillStore {
  if (typeof window === 'undefined') {
    return { skill_log: {}, badges: [], unlocked_levels: ['Beginner'] }
  }
  try {
    return JSON.parse(localStorage.getItem(SKILLS_KEY) ?? 'null') ?? {
      skill_log: {},
      badges: [],
      unlocked_levels: ['Beginner'],
    }
  } catch {
    return { skill_log: {}, badges: [], unlocked_levels: ['Beginner'] }
  }
}

function saveStore(store: SkillStore) {
  localStorage.setItem(SKILLS_KEY, JSON.stringify(store))
}

export function logSkills(tags: string[], sessionId: string): string[] {
  const store = getStore()
  const newBadges: string[] = []

  for (const tag of tags) {
    if (!store.skill_log[tag]) store.skill_log[tag] = []
    if (!store.skill_log[tag].includes(sessionId)) {
      store.skill_log[tag].push(sessionId)
    }
  }

  saveStore(store)
  return newBadges
}

export function getBadges(): string[] {
  return getStore().badges
}

export function getSkillCount(): number {
  const store = getStore()
  return Object.keys(store.skill_log).length
}
