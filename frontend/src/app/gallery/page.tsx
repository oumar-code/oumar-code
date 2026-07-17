'use client'

import { useState } from 'react'
import { Navbar } from '@/components/Navbar'
import { OfflineIndicator } from '@/components/OfflineIndicator'
import { Users, Heart, Search, Filter, TrendingUp } from 'lucide-react'
import type { Design } from '@/types'

// Mock gallery data — seeded from fashion/gallery.py
const MOCK_DESIGNS: Design[] = [
  {
    id: '1', title: 'Modern Buba & Sokoto', designer: 'Fatima Aliyu',
    description: 'A sleek corporate reinterpretation of the classic buba and sokoto. Tailored fit, notch lapel collar, tapered ankle-length sokoto. Perfect for the modern African professional woman.',
    tags: ['buba-sokoto', 'corporate', 'ankara', 'womens-wear'], image_url: '',
    likes: 47, comments_count: 12, skill_level: 'Advanced', fabric_type: 'ankara', created_at: Date.now() - 86400 * 1000,
  },
  {
    id: '2', title: 'Kente Wrap Dress', designer: 'Kofi Mensah',
    description: 'Floor-length wrap dress in authentic Ghanaian kente cloth. V-neckline, flutter sleeves, adjustable tie waist.',
    tags: ['kente', 'wrap-dress', 'ghana', 'floor-length'], image_url: '',
    likes: 62, comments_count: 8, skill_level: 'Advanced', fabric_type: 'kente', created_at: Date.now() - 86400 * 2000,
  },
  {
    id: '3', title: 'Ankara Blazer (Power Shoulder)', designer: 'Chioma Okafor',
    description: 'Power-shoulder ankara blazer with structural padding. Single-breasted, welt pockets, fully lined. Demonstrates full tailoring construction.',
    tags: ['blazer', 'ankara', 'power-shoulder', 'corporate'], image_url: '',
    likes: 89, comments_count: 24, skill_level: 'Advanced', fabric_type: 'ankara', created_at: Date.now() - 86400 * 3000,
  },
  {
    id: '4', title: 'Lace Mermaid Evening Gown', designer: 'Amina Ibrahim',
    description: 'Floor-length mermaid gown in Nigerian guipure lace. Sweetheart neckline, invisible zipper, godets at knee for flare.',
    tags: ['lace', 'mermaid', 'evening-gown', 'couture'], image_url: '',
    likes: 134, comments_count: 41, skill_level: 'Master', fabric_type: 'lace', created_at: Date.now() - 86400 * 4000,
  },
  {
    id: '5', title: 'Beginner Pencil Skirt', designer: 'Grace Adeyemi',
    description: 'My very first pencil skirt! Invisible zipper at back, waistband with interfacing. Learned so much about pressing.',
    tags: ['pencil-skirt', 'beginner', 'cotton', 'first-project'], image_url: '',
    likes: 28, comments_count: 15, skill_level: 'Beginner', fabric_type: 'cotton', created_at: Date.now() - 86400 * 5000,
  },
  {
    id: '6', title: 'Aso-oke Senator Agbada', designer: 'Babatunde Lawson',
    description: 'Traditional Nigerian agbada in hand-woven aso-oke. Three-piece set with embroidered neckline and cuffs. Wedding ceremony piece.',
    tags: ['agbada', 'aso-oke', 'traditional', 'mens-wear'], image_url: '',
    likes: 203, comments_count: 67, skill_level: 'Master', fabric_type: 'aso-oke', created_at: Date.now() - 86400 * 6000,
  },
  {
    id: '7', title: 'Chiffon Ruffle Blouse', designer: 'Ngozi Eze',
    description: 'Flowy chiffon blouse with cascading ruffle front. French seams throughout. Trick: stay-stitch every edge before cutting chiffon.',
    tags: ['blouse', 'chiffon', 'ruffles', 'french-seams'], image_url: '',
    likes: 41, comments_count: 9, skill_level: 'Intermediate', fabric_type: 'chiffon', created_at: Date.now() - 86400 * 7000,
  },
  {
    id: '8', title: 'Ankara Shift Dress', designer: 'Aisha Mohammed',
    description: 'Clean minimalist shift dress in bold geometric ankara. A-line silhouette, round neck, invisible zipper at centre back.',
    tags: ['shift-dress', 'ankara', 'a-line', 'everyday-wear'], image_url: '',
    likes: 56, comments_count: 18, skill_level: 'Intermediate', fabric_type: 'ankara', created_at: Date.now() - 86400 * 8000,
  },
]

const SKILL_LEVELS = ['All', 'Beginner', 'Intermediate', 'Advanced', 'Master']
const FABRIC_TYPES = ['All', 'ankara', 'lace', 'kente', 'aso-oke', 'chiffon', 'cotton']

const FABRIC_EMOJI: Record<string, string> = {
  ankara: '🌍', lace: '✨', kente: '🇬🇭', 'aso-oke': '👑', chiffon: '🌸', cotton: '🌿',
}

const LEVEL_COLORS: Record<string, string> = {
  Beginner: 'bg-green-600/20 text-green-400 border-green-600/30',
  Intermediate: 'bg-blue-600/20 text-blue-400 border-blue-600/30',
  Advanced: 'bg-purple-600/20 text-purple-400 border-purple-600/30',
  Master: 'bg-amber-600/20 text-amber-400 border-amber-600/30',
}

export default function GalleryPage() {
  const [search, setSearch] = useState('')
  const [levelFilter, setLevelFilter] = useState('All')
  const [fabricFilter, setFabricFilter] = useState('All')
  const [sortBy, setSortBy] = useState<'popular' | 'recent'>('popular')
  const [likedIds, setLikedIds] = useState<Set<string>>(new Set())

  const toggleLike = (id: string) => {
    setLikedIds(prev => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }

  const filtered = MOCK_DESIGNS
    .filter(d => {
      const q = search.toLowerCase()
      const matchSearch = !q || d.title.toLowerCase().includes(q) ||
        d.description.toLowerCase().includes(q) || d.tags.some(t => t.includes(q))
      const matchLevel = levelFilter === 'All' || d.skill_level === levelFilter
      const matchFabric = fabricFilter === 'All' || d.fabric_type === fabricFilter
      return matchSearch && matchLevel && matchFabric
    })
    .sort((a, b) => sortBy === 'popular' ? b.likes - a.likes : b.created_at - a.created_at)

  return (
    <>
      <Navbar />
      <OfflineIndicator />

      <main className="pt-20 pb-20 px-4 max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-rose-600 rounded-xl flex items-center justify-center">
              <Users className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">Community Gallery</h1>
              <p className="text-dark-400 text-sm">Designs by tailors and fashion students · Share · Get feedback</p>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-dark-800 border border-dark-700 rounded-2xl p-4 mb-6 space-y-3">
          {/* Search */}
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-dark-400" />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search designs, techniques, fabrics…"
              className="w-full bg-dark-700 border border-dark-600 focus:border-brand-600 rounded-xl pl-9 pr-4 py-2.5 text-sm focus:outline-none transition-colors"
            />
          </div>

          <div className="flex flex-wrap gap-2">
            {/* Level filter */}
            <div className="flex gap-1">
              {SKILL_LEVELS.map(level => (
                <button
                  key={level}
                  onClick={() => setLevelFilter(level)}
                  className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${levelFilter === level ? 'bg-brand-600 border-brand-600 text-white' : 'bg-dark-700 border-dark-600 text-dark-400 hover:text-white'}`}
                >
                  {level}
                </button>
              ))}
            </div>
            {/* Sort */}
            <div className="ml-auto flex gap-1">
              <button
                onClick={() => setSortBy('popular')}
                className={`text-xs flex items-center gap-1 px-3 py-1.5 rounded-full border transition-colors ${sortBy === 'popular' ? 'bg-brand-600 border-brand-600 text-white' : 'bg-dark-700 border-dark-600 text-dark-400 hover:text-white'}`}
              >
                <TrendingUp className="w-3 h-3" /> Popular
              </button>
              <button
                onClick={() => setSortBy('recent')}
                className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${sortBy === 'recent' ? 'bg-brand-600 border-brand-600 text-white' : 'bg-dark-700 border-dark-600 text-dark-400 hover:text-white'}`}
              >
                Recent
              </button>
            </div>
          </div>
        </div>

        {/* Stats bar */}
        <div className="flex items-center gap-4 text-sm text-dark-400 mb-6">
          <span>{filtered.length} design{filtered.length !== 1 ? 's' : ''}</span>
          <span>·</span>
          <span>{MOCK_DESIGNS.reduce((s, d) => s + d.likes, 0)} likes</span>
          <span>·</span>
          <span>{new Set(MOCK_DESIGNS.map(d => d.designer)).size} designers</span>
        </div>

        {/* Grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map(design => (
            <div key={design.id} className="bg-dark-800 border border-dark-700 rounded-2xl overflow-hidden card-hover">
              {/* Image placeholder */}
              <div className="h-48 bg-gradient-to-br from-dark-700 to-dark-600 flex items-center justify-center">
                <div className="text-center">
                  <div className="text-4xl mb-2">{FABRIC_EMOJI[design.fabric_type] ?? '🧵'}</div>
                  <div className="text-xs text-dark-500 capitalize">{design.fabric_type}</div>
                </div>
              </div>

              <div className="p-4">
                {/* Title + level */}
                <div className="flex items-start justify-between gap-2 mb-2">
                  <h3 className="font-semibold text-sm leading-tight">{design.title}</h3>
                  <span className={`text-xs px-2 py-0.5 rounded-full border flex-shrink-0 ${LEVEL_COLORS[design.skill_level] ?? ''}`}>
                    {design.skill_level}
                  </span>
                </div>

                <p className="text-xs text-dark-400 mb-3 line-clamp-2">{design.description}</p>

                {/* Tags */}
                <div className="flex flex-wrap gap-1 mb-3">
                  {design.tags.slice(0, 3).map(tag => (
                    <span key={tag} className="text-xs bg-dark-700 text-dark-400 px-2 py-0.5 rounded-full">#{tag}</span>
                  ))}
                </div>

                {/* Footer */}
                <div className="flex items-center justify-between">
                  <span className="text-xs text-dark-500">by {design.designer}</span>
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-dark-500">{design.comments_count} comments</span>
                    <button
                      onClick={() => toggleLike(design.id)}
                      className={`flex items-center gap-1 text-xs transition-colors ${likedIds.has(design.id) ? 'text-rose-400' : 'text-dark-400 hover:text-rose-400'}`}
                    >
                      <Heart className={`w-3.5 h-3.5 ${likedIds.has(design.id) ? 'fill-current' : ''}`} />
                      {design.likes + (likedIds.has(design.id) ? 1 : 0)}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-20 text-dark-500">
            <Users className="w-12 h-12 mx-auto mb-3 opacity-30" />
            <p>No designs match your search.</p>
          </div>
        )}
      </main>
    </>
  )
}
