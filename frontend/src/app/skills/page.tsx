'use client'

import { useState, useEffect } from 'react'
import { Navbar } from '@/components/Navbar'
import { OfflineIndicator } from '@/components/OfflineIndicator'
import { SkillBadge, SkillProgress } from '@/components/SkillBadge'
import { Star, TrendingUp, Award, BookOpen } from 'lucide-react'
import { getLearnerId, getStore, getBadges, getSkillCount } from '@/lib/skill-tracker'

const LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Master']

const LEVEL_COLORS: Record<string, string> = {
  Beginner: 'from-green-600 to-green-500',
  Intermediate: 'from-blue-600 to-blue-500',
  Advanced: 'from-purple-600 to-purple-500',
  Master: 'from-amber-600 to-amber-500',
}

const RECOMMENDED_NEXT = [
  { tag: 'invisible-zipper', name: 'Invisible Zipper', level: 'Intermediate', sessions_remaining: 2 },
  { tag: 'dart', name: 'Darts', level: 'Intermediate', sessions_remaining: 1 },
  { tag: 'pattern-drafting', name: 'Pattern Drafting', level: 'Advanced', sessions_remaining: 4 },
]

interface SkillStore {
  skill_log: Record<string, string[]>
  badges: string[]
  unlocked_levels: string[]
}

export default function SkillsPage() {
  const [store, setStore] = useState<SkillStore>({
    skill_log: {}, badges: [], unlocked_levels: ['Beginner'],
  })
  const [learnerId, setLearnerId] = useState('')

  useEffect(() => {
    setLearnerId(getLearnerId())
    // Load from localStorage
    try {
      const raw = localStorage.getItem('aku_skills')
      if (raw) setStore(JSON.parse(raw))
    } catch {}
  }, [])

  const badges = store.badges
  const skillCount = Object.keys(store.skill_log).length
  const masteredCount = Object.entries(store.skill_log).filter(([, sessions]) => sessions.length >= 3).length
  const overallPct = skillCount > 0 ? Math.round(masteredCount / skillCount * 100) : 0

  return (
    <>
      <Navbar />
      <OfflineIndicator />

      <main className="pt-20 pb-20 px-4 max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-amber-600 rounded-xl flex items-center justify-center">
              <Star className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">Skill Tracker</h1>
              <p className="text-dark-400 text-sm">{learnerId || 'Loading…'}</p>
            </div>
          </div>
        </div>

        {/* Overview stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Badges', value: badges.length, icon: Award, color: 'text-amber-400' },
            { label: 'Skills Practiced', value: skillCount, icon: BookOpen, color: 'text-blue-400' },
            { label: 'Mastered', value: masteredCount, icon: Star, color: 'text-green-400' },
            { label: 'Mastery %', value: `${overallPct}%`, icon: TrendingUp, color: 'text-purple-400' },
          ].map(({ label, value, icon: Icon, color }) => (
            <div key={label} className="bg-dark-800 border border-dark-700 rounded-2xl p-4 text-center">
              <Icon className={`w-5 h-5 mx-auto mb-2 ${color}`} />
              <div className="text-2xl font-bold mb-1">{value}</div>
              <div className="text-xs text-dark-400">{label}</div>
            </div>
          ))}
        </div>

        {/* Badges earned */}
        <div className="bg-dark-800 border border-dark-700 rounded-2xl p-6 mb-6">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <Award className="w-4 h-4 text-amber-400" />
            Badges Earned ({badges.length})
          </h2>
          {badges.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {badges.map(badge => <SkillBadge key={badge} badge={badge} size="md" />)}
            </div>
          ) : (
            <div className="text-center py-8 text-dark-500">
              <Award className="w-10 h-10 mx-auto mb-3 opacity-30" />
              <p className="text-sm">No badges yet — start learning in the Tutor tab!</p>
              <p className="text-xs mt-1">Complete 3 sessions on any skill to earn your first badge.</p>
            </div>
          )}
        </div>

        {/* Level progression */}
        <div className="bg-dark-800 border border-dark-700 rounded-2xl p-6 mb-6">
          <h2 className="font-semibold mb-4">Level Progression</h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {LEVELS.map(level => {
              const unlocked = store.unlocked_levels.includes(level)
              return (
                <div
                  key={level}
                  className={`rounded-xl p-4 text-center border transition-all ${
                    unlocked
                      ? `bg-gradient-to-br ${LEVEL_COLORS[level]} border-transparent text-white`
                      : 'bg-dark-700 border-dark-600 text-dark-500'
                  }`}
                >
                  <div className="text-2xl mb-1">{unlocked ? '🔓' : '🔒'}</div>
                  <div className="font-medium text-sm">{level}</div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Skills practiced */}
        {skillCount > 0 && (
          <div className="bg-dark-800 border border-dark-700 rounded-2xl p-6 mb-6">
            <h2 className="font-semibold mb-4">Skills Practiced</h2>
            <div className="space-y-4">
              {Object.entries(store.skill_log).map(([tag, sessions]) => (
                <SkillProgress
                  key={tag}
                  name={tag.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
                  sessions={sessions.length}
                  required={3}
                  mastered={sessions.length >= 3}
                  level="Intermediate"
                />
              ))}
            </div>
          </div>
        )}

        {/* Recommended next */}
        <div className="bg-dark-800 border border-dark-700 rounded-2xl p-6">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-brand-400" />
            Recommended Next
          </h2>
          <div className="space-y-3">
            {RECOMMENDED_NEXT.map(skill => (
              <div key={skill.tag} className="flex items-center justify-between p-3 bg-dark-700 rounded-xl">
                <div>
                  <div className="font-medium text-sm">{skill.name}</div>
                  <div className="text-xs text-dark-400">{skill.level} · {skill.sessions_remaining} session(s) to mastery</div>
                </div>
                <a
                  href="/tutor"
                  className="text-xs bg-brand-600 hover:bg-brand-700 text-white px-3 py-1.5 rounded-lg transition-colors"
                >
                  Learn
                </a>
              </div>
            ))}
          </div>
        </div>
      </main>
    </>
  )
}
