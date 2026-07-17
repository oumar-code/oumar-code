import { clsx } from 'clsx'

interface SkillBadgeProps {
  badge: string
  size?: 'sm' | 'md' | 'lg'
  animate?: boolean
}

export function SkillBadge({ badge, size = 'md', animate = false }: SkillBadgeProps) {
  const emoji = badge.split(' ')[0]
  const label = badge.split(' ').slice(1).join(' ')

  return (
    <div
      className={clsx(
        'inline-flex items-center gap-1.5 rounded-full border border-brand-600/40 bg-brand-600/10 font-medium',
        animate && 'badge-pop',
        size === 'sm' && 'text-xs px-2.5 py-1',
        size === 'md' && 'text-sm px-3 py-1.5',
        size === 'lg' && 'text-base px-4 py-2',
      )}
    >
      <span>{emoji}</span>
      <span className="text-brand-300">{label}</span>
    </div>
  )
}

interface SkillProgressProps {
  name: string
  sessions: number
  required: number
  mastered: boolean
  level: string
}

export function SkillProgress({ name, sessions, required, mastered, level }: SkillProgressProps) {
  const pct = Math.min(100, Math.round((sessions / required) * 100))

  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between text-sm">
        <span className={mastered ? 'text-white font-medium' : 'text-dark-300'}>{name}</span>
        <div className="flex items-center gap-2">
          {mastered && <span className="text-green-400 text-xs">✓ Mastered</span>}
          <span className="text-dark-500 text-xs">{sessions}/{required}</span>
        </div>
      </div>
      <div className="skill-bar">
        <div className="skill-bar-fill" style={{ width: `${pct}%` }} />
      </div>
      <div className="text-xs text-dark-500">{level}</div>
    </div>
  )
}
