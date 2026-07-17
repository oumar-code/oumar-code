/**
 * Shared types for the Aku Fashion frontend.
 */

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  skill_tags?: string[]
  timestamp: Date
  isStreaming?: boolean
}

export interface SkillData {
  tag: string
  name: string
  sessions: number
  mastery_required: number
  mastered: boolean
  progress_pct: number
}

export interface ProgressSummary {
  learner_id: string
  unlocked_levels: string[]
  badges: string[]
  badge_count: number
  total_skills_practiced: number
  skills_mastered: number
  overall_mastery_pct: number
  skills_by_level: Record<string, SkillData[]>
}

export interface TechPack {
  garment_name: string
  description: string
  category: string
  silhouette: string
  fabric_type: string
  fabric_yards: number
  colour: string
  lining?: string
  closure?: string
  sleeves?: string
  collar?: string
  pockets?: string
  complexity: 'simple' | 'moderate' | 'complex' | 'couture'
  estimated_hours: number
  special_notes: string[]
  construction_order: string[]
}

export interface PriceQuote {
  complexity: string
  labour_hours: number
  fabric_cost_ngn: number
  labour_cost_ngn: number
  overhead_ngn: number
  profit_ngn: number
  total_ngn: number
  total_usd_approx: number
  breakdown_pct: Record<string, number>
}

export interface FabricEstimate {
  fabric_type: string
  yards: number
  price_per_yard_ngn: number
  fabric_cost_ngn: number
  cost_with_markup_ngn: number
  note: string
}

export interface Design {
  id: string
  title: string
  designer: string
  description: string
  tags: string[]
  image_url: string
  likes: number
  comments_count: number
  skill_level: string
  fabric_type: string
  created_at: number
}

export interface PatternPiece {
  name: string
  width: number
  height: number
  svg: string
}

export interface OfflineQueueItem {
  id: string
  request_type: string
  payload: Record<string, unknown>
  created_at: number
  status: 'pending' | 'done' | 'failed'
}
