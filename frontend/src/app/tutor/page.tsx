'use client'

import { useState, useRef, useEffect, useCallback } from 'react'
import { Navbar } from '@/components/Navbar'
import { OfflineIndicator } from '@/components/OfflineIndicator'
import { SkillBadge } from '@/components/SkillBadge'
import ReactMarkdown from 'react-markdown'
import toast from 'react-hot-toast'
import { Send, Mic, Image, RotateCcw, Sparkles } from 'lucide-react'
import { enqueue } from '@/lib/offline-queue'
import { logSkills } from '@/lib/skill-tracker'
import type { ChatMessage } from '@/types'

const WELCOME_MSG: ChatMessage = {
  id: 'welcome',
  role: 'assistant',
  content: `Welcome to **Aku** — your AI Fashion Tutor! 🎓✂️

I'm here to teach you tailoring and fashion design step-by-step.

**Try asking me:**
- "How do I sew an invisible zipper?"
- "Teach me about darts"
- "How do I set in sleeves properly?"
- "Help me work with ankara fabric"
- "What's the difference between a dart and a tuck?"

Works offline too — your lessons are saved locally. 📴`,
  skill_tags: [],
  timestamp: new Date(),
}

const SUGGESTIONS = [
  'How do I sew an invisible zipper on ankara?',
  'Teach me about darts step by step',
  'How do I set in sleeves without puckers?',
  'How do I price my tailoring work?',
  'What is pattern grading?',
]

export default function TutorPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MSG])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [newBadges, setNewBadges] = useState<string[]>([])
  const [sessionId] = useState(() => crypto.randomUUID().slice(0, 8))
  const bottomRef = useRef<HTMLDivElement>(null)
  const fileRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = useCallback(async (userText: string, imageBase64?: string) => {
    if (!userText.trim() && !imageBase64) return
    setLoading(true)

    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: userText || '(image uploaded)',
      timestamp: new Date(),
    }
    setMessages(prev => [...prev, userMsg])
    setInput('')

    // Build history for API
    const history = [...messages, userMsg]
      .filter(m => m.id !== 'welcome')
      .map(m => ({ role: m.role, content: m.content }))

    try {
      let response: Response
      if (!navigator.onLine) {
        enqueue('tutor_chat', { message: userText, imageBase64 })
        const offlineMsg: ChatMessage = {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: '📴 **Offline mode** — your message has been queued and will be answered when you\'re back online.\n\nMeanwhile, here\'s a tip: review your previous lessons in this chat.',
          skill_tags: [],
          timestamp: new Date(),
        }
        setMessages(prev => [...prev, offlineMsg])
        setLoading(false)
        return
      }

      response = await fetch('/api/tutor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: history, imageBase64 }),
      })

      const data = await response.json()
      const assistantMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: data.text,
        skill_tags: data.skill_tags ?? [],
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, assistantMsg])

      // Log skills
      if (data.skill_tags?.length) {
        logSkills(data.skill_tags, sessionId)
        // Check for new badges (simplified)
        if (data.skill_tags.length >= 2) {
          const badge = '🎯 Fast Learner'
          setNewBadges(prev => [...prev, badge])
          toast.success(`Badge earned: ${badge}!`, { icon: '🏆', duration: 4000 })
          setTimeout(() => setNewBadges(prev => prev.filter(b => b !== badge)), 5000)
        }
      }
    } catch (err) {
      toast.error('Failed to get response. Please try again.')
    } finally {
      setLoading(false)
    }
  }, [messages, sessionId])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage(input)
  }

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => {
      sendMessage('Analyse this garment and provide pattern + sewing instructions.', reader.result as string)
    }
    reader.readAsDataURL(file)
  }

  const reset = () => {
    setMessages([WELCOME_MSG])
    setInput('')
  }

  return (
    <>
      <Navbar />
      <OfflineIndicator />

      <div className="flex flex-col h-screen pt-16">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-dark-800 bg-dark-900/80 backdrop-blur">
          <div>
            <h1 className="font-bold text-lg flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-brand-400" />
              AI Fashion Tutor
            </h1>
            <p className="text-xs text-dark-400">GPT-5.6 · Teaching mode · Offline-first</p>
          </div>
          <button onClick={reset} className="p-2 rounded-lg hover:bg-dark-800 text-dark-400 hover:text-white transition-colors">
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4 max-w-3xl w-full mx-auto">
          {messages.map(msg => (
            <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 bg-brand-600 rounded-full flex-shrink-0 mr-2 flex items-center justify-center text-xs font-bold mt-1">A</div>
              )}
              <div className={msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-ai'}>
                {msg.role === 'assistant' ? (
                  <div className="prose prose-sm text-sm">
                    <ReactMarkdown>{msg.content.replace(/```skill_tags[\s\S]*?```/g, '')}</ReactMarkdown>
                  </div>
                ) : (
                  <p className="text-sm">{msg.content}</p>
                )}
                {msg.skill_tags && msg.skill_tags.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mt-3 pt-3 border-t border-dark-600">
                    {msg.skill_tags.filter(t => t !== 'welcome' && t !== 'onboarding').map(tag => (
                      <span key={tag} className="text-xs bg-dark-700 text-dark-300 px-2 py-0.5 rounded-full">#{tag}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start animate-fade-in">
              <div className="w-8 h-8 bg-brand-600 rounded-full flex-shrink-0 mr-2 flex items-center justify-center text-xs font-bold">A</div>
              <div className="chat-bubble-ai flex items-center gap-2">
                <div className="flex gap-1">
                  {[0, 1, 2].map(i => (
                    <div key={i} className="w-2 h-2 rounded-full bg-brand-400 animate-bounce" style={{ animationDelay: `${i * 0.15}s` }} />
                  ))}
                </div>
                <span className="text-dark-400 text-sm">Thinking…</span>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* Suggestions */}
        {messages.length <= 1 && (
          <div className="px-4 pb-2 max-w-3xl w-full mx-auto">
            <div className="flex flex-wrap gap-2">
              {SUGGESTIONS.map(s => (
                <button
                  key={s}
                  onClick={() => sendMessage(s)}
                  className="text-xs bg-dark-800 border border-dark-700 hover:border-brand-600 text-dark-300 hover:text-white px-3 py-1.5 rounded-full transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="border-t border-dark-800 bg-dark-900/80 backdrop-blur px-4 py-4">
          <div className="max-w-3xl mx-auto">
            <form onSubmit={handleSubmit} className="flex gap-2 items-end">
              <div className="flex-1 bg-dark-800 border border-dark-700 focus-within:border-brand-600 rounded-xl overflow-hidden transition-colors">
                <textarea
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(e) } }}
                  placeholder="Ask about any tailoring technique…"
                  rows={1}
                  className="w-full bg-transparent px-4 py-3 text-sm resize-none focus:outline-none placeholder-dark-500"
                />
              </div>
              <input ref={fileRef} type="file" accept="image/*" onChange={handleImageUpload} className="hidden" />
              <button
                type="button"
                onClick={() => fileRef.current?.click()}
                className="p-3 rounded-xl bg-dark-800 border border-dark-700 hover:border-brand-600 text-dark-400 hover:text-white transition-colors"
                title="Upload garment photo"
              >
                <Image className="w-5 h-5" />
              </button>
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="p-3 rounded-xl bg-brand-600 hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed text-white transition-colors"
              >
                <Send className="w-5 h-5" />
              </button>
            </form>
          </div>
        </div>
      </div>
    </>
  )
}
