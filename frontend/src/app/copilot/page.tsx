'use client'

import { useState } from 'react'
import { Navbar } from '@/components/Navbar'
import { OfflineIndicator } from '@/components/OfflineIndicator'
import ReactMarkdown from 'react-markdown'
import toast from 'react-hot-toast'
import { Briefcase, Loader2, Copy, CheckCircle } from 'lucide-react'
import type { TechPack, PriceQuote, FabricEstimate } from '@/types'

interface CopilotResult {
  tech_pack: TechPack
  price_quote: PriceQuote
  fabric_estimate: FabricEstimate
  summary_md: string
}

export default function CopilotPage() {
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<CopilotResult | null>(null)
  const [copied, setCopied] = useState(false)
  const [activeTab, setActiveTab] = useState<'summary' | 'techpack' | 'price'>('summary')

  const generate = async () => {
    if (!description.trim()) {
      toast.error('Please describe the garment')
      return
    }
    setLoading(true)
    try {
      const resp = await fetch('/api/copilot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description }),
      })
      const data = await resp.json()
      setResult(data)
      setActiveTab('summary')
      toast.success('Tech pack generated!')
    } catch {
      toast.error('Failed to generate tech pack')
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = () => {
    if (!result?.summary_md) return
    navigator.clipboard.writeText(result.summary_md)
    setCopied(true)
    toast.success('Copied to clipboard')
    setTimeout(() => setCopied(false), 2000)
  }

  const EXAMPLE_DESCRIPTIONS = [
    'Corporate ankara blazer, size 14, navy/gold print, 3/4 sleeves, notch lapel, 2 welt pockets',
    'Mermaid lace gown, size 10, ivory, sweetheart neckline, invisible zip, floor length',
    'Modern buba and sokoto, size 16, yellow/green ankara, tapered trouser, structured collar',
    'Fit-and-flare dress, size 12, chiffon, halter neck, midi length, hidden zip at back',
  ]

  return (
    <>
      <Navbar />
      <OfflineIndicator />

      <main className="pt-20 pb-20 px-4 max-w-5xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center">
              <Briefcase className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">Tailor Co-pilot</h1>
              <p className="text-dark-400 text-sm">GPT-5.6 + Codex · Tech pack, fabric estimate & price quote</p>
            </div>
          </div>
        </div>

        {/* Input */}
        <div className="bg-dark-800 border border-dark-700 rounded-2xl p-6 mb-6">
          <label className="block text-sm font-medium mb-3">Describe your garment</label>
          <textarea
            value={description}
            onChange={e => setDescription(e.target.value)}
            placeholder="e.g. Corporate ankara blazer, size 14, navy/gold print, 3/4 sleeves, notch lapel, 2 welt pockets, fully lined..."
            rows={4}
            className="w-full bg-dark-700 border border-dark-600 focus:border-brand-600 rounded-xl px-4 py-3 text-sm resize-none focus:outline-none placeholder-dark-500 transition-colors"
          />
          <div className="flex flex-wrap gap-2 mt-3">
            {EXAMPLE_DESCRIPTIONS.map(ex => (
              <button
                key={ex}
                onClick={() => setDescription(ex)}
                className="text-xs bg-dark-700 hover:bg-dark-600 border border-dark-600 text-dark-300 hover:text-white px-3 py-1.5 rounded-full transition-colors truncate max-w-xs"
              >
                {ex.slice(0, 50)}…
              </button>
            ))}
          </div>
          <button
            onClick={generate}
            disabled={loading || !description.trim()}
            className="mt-4 w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl transition-colors"
          >
            {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Generating…</> : <><Briefcase className="w-4 h-4" /> Generate Tech Pack</>}
          </button>
        </div>

        {/* Results */}
        {result && (
          <div className="animate-slide-up">
            {/* Tabs */}
            <div className="flex gap-1 bg-dark-800 border border-dark-700 rounded-xl p-1 mb-4">
              {(['summary', 'techpack', 'price'] as const).map(tab => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors capitalize ${activeTab === tab ? 'bg-dark-600 text-white' : 'text-dark-400 hover:text-white'}`}
                >
                  {tab === 'techpack' ? 'Tech Pack' : tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>

            {activeTab === 'summary' && (
              <div className="bg-dark-800 border border-dark-700 rounded-2xl p-6">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="font-semibold">Summary</h2>
                  <button onClick={copyToClipboard} className="flex items-center gap-1.5 text-xs text-dark-400 hover:text-white transition-colors">
                    {copied ? <CheckCircle className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
                    {copied ? 'Copied!' : 'Copy'}
                  </button>
                </div>
                <div className="prose prose-sm">
                  <ReactMarkdown>{result.summary_md}</ReactMarkdown>
                </div>
              </div>
            )}

            {activeTab === 'techpack' && (
              <div className="bg-dark-800 border border-dark-700 rounded-2xl p-6 space-y-4">
                <h2 className="font-semibold mb-4">Technical Specification</h2>
                <div className="grid sm:grid-cols-2 gap-3">
                  {Object.entries(result.tech_pack)
                    .filter(([k]) => !['special_notes', 'construction_order', 'description'].includes(k))
                    .map(([key, value]) => (
                      <div key={key} className="flex gap-3">
                        <span className="text-dark-400 text-sm capitalize min-w-[120px]">{key.replace(/_/g, ' ')}</span>
                        <span className="text-sm font-medium">{String(value)}</span>
                      </div>
                    ))}
                </div>
                {result.tech_pack.special_notes?.length > 0 && (
                  <div>
                    <h3 className="font-medium mb-2 text-sm text-dark-300">Special Notes</h3>
                    <ul className="space-y-1">
                      {result.tech_pack.special_notes.map((note, i) => (
                        <li key={i} className="text-sm text-dark-300 flex gap-2"><span className="text-brand-400">•</span>{note}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {result.tech_pack.construction_order?.length > 0 && (
                  <div>
                    <h3 className="font-medium mb-2 text-sm text-dark-300">Construction Order</h3>
                    <ol className="space-y-1">
                      {result.tech_pack.construction_order.map((step, i) => (
                        <li key={i} className="text-sm text-dark-300">{step}</li>
                      ))}
                    </ol>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'price' && (
              <div className="bg-dark-800 border border-dark-700 rounded-2xl p-6 space-y-6">
                <h2 className="font-semibold">Price Quote</h2>
                <div className="grid sm:grid-cols-2 gap-4">
                  {/* Breakdown table */}
                  <div className="space-y-3">
                    {[
                      { label: 'Fabric', value: result.price_quote.fabric_cost_ngn },
                      { label: 'Labour', value: result.price_quote.labour_cost_ngn },
                      { label: 'Overhead', value: result.price_quote.overhead_ngn },
                      { label: 'Profit', value: result.price_quote.profit_ngn },
                    ].map(({ label, value }) => (
                      <div key={label} className="flex justify-between text-sm">
                        <span className="text-dark-400">{label}</span>
                        <span>₦{value.toLocaleString()}</span>
                      </div>
                    ))}
                    <div className="flex justify-between font-bold border-t border-dark-600 pt-3">
                      <span>Total</span>
                      <span className="text-brand-400 text-lg">₦{result.price_quote.total_ngn.toLocaleString()}</span>
                    </div>
                    <div className="text-xs text-dark-500 text-right">≈ ${result.price_quote.total_usd_approx} USD</div>
                  </div>
                  {/* Fabric estimate */}
                  <div className="bg-dark-700 rounded-xl p-4 space-y-2">
                    <h3 className="font-medium text-sm mb-3">Fabric Estimate</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between"><span className="text-dark-400">Type</span><span className="capitalize">{result.fabric_estimate.fabric_type}</span></div>
                      <div className="flex justify-between"><span className="text-dark-400">Yards needed</span><span>{result.fabric_estimate.yards}</span></div>
                      <div className="flex justify-between"><span className="text-dark-400">Price/yard</span><span>₦{result.fabric_estimate.price_per_yard_ngn.toLocaleString()}</span></div>
                      <div className="flex justify-between font-medium border-t border-dark-600 pt-2"><span>Fabric cost</span><span>₦{result.fabric_estimate.fabric_cost_ngn.toLocaleString()}</span></div>
                    </div>
                    <p className="text-xs text-amber-400 mt-2">{result.fabric_estimate.note}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </>
  )
}
