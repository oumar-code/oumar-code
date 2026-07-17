import Link from 'next/link'
import { GraduationCap, Briefcase, Palette, Star, Users, Scissors, Wifi, WifiOff, ArrowRight } from 'lucide-react'
import { Navbar } from '@/components/Navbar'
import { OfflineIndicator } from '@/components/OfflineIndicator'

const features = [
  {
    href: '/tutor',
    icon: GraduationCap,
    title: 'AI Fashion Tutor',
    description: 'Learn tailoring step-by-step from an AI coach. Ask anything: zippers, darts, sleeves, patterns. Get badges as you master each skill.',
    badge: 'GPT-5.6',
    color: 'from-orange-500 to-amber-500',
  },
  {
    href: '/copilot',
    icon: Briefcase,
    title: 'Tailor Co-pilot',
    description: 'Turn a garment description or inspo photo into a full tech pack, fabric estimate, and price quote — ready to share with your client.',
    badge: 'GPT-5.6 + Codex',
    color: 'from-blue-500 to-indigo-500',
  },
  {
    href: '/design',
    icon: Palette,
    title: 'Pattern Generator',
    description: 'Enter your measurements → get SVG pattern pieces for bodice, skirt, or dress. Codex-generated pattern math, professional output.',
    badge: 'Codex',
    color: 'from-purple-500 to-pink-500',
  },
  {
    href: '/skills',
    icon: Star,
    title: 'Skill Tracker',
    description: 'Track your progress through Beginner → Intermediate → Advanced → Master. Earn badges for every technique you master.',
    badge: 'Progress',
    color: 'from-green-500 to-teal-500',
  },
  {
    href: '/gallery',
    icon: Users,
    title: 'Community Gallery',
    description: 'Discover designs from tailors and fashion students. Share your work, get feedback, and find inspiration from the community.',
    badge: 'Community',
    color: 'from-rose-500 to-red-500',
  },
]

const stats = [
  { label: 'Techniques Covered', value: '50+' },
  { label: 'Skill Badges', value: '20' },
  { label: 'Works Offline', value: '100%' },
  { label: 'Powered By', value: 'GPT-5.6' },
]

export default function HomePage() {
  return (
    <>
      <Navbar />
      <OfflineIndicator />

      <main className="pt-16">
        {/* Hero */}
        <section className="relative overflow-hidden px-4 py-24 sm:py-32">
          {/* Background gradient */}
          <div className="absolute inset-0 bg-gradient-to-br from-brand-900/20 via-dark-900 to-dark-900" />
          <div className="absolute top-20 left-1/2 -translate-x-1/2 w-96 h-96 bg-brand-600/10 rounded-full blur-3xl" />

          <div className="relative max-w-4xl mx-auto text-center">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 bg-brand-600/10 border border-brand-600/30 rounded-full px-4 py-1.5 text-sm text-brand-400 mb-6">
              <Scissors className="w-3.5 h-3.5" />
              OpenAI Build Week · AI Fashion Skills App
            </div>

            <h1 className="text-5xl sm:text-7xl font-bold leading-tight mb-6">
              Learn tailoring with{' '}
              <span className="gradient-text">AI that works</span>
              <br />
              even offline
            </h1>

            <p className="text-xl text-dark-300 max-w-2xl mx-auto mb-10">
              Aku is your AI fashion tutor and co-pilot — powered by GPT-5.6 and Codex.
              Teaches step-by-step, tracks your skills, generates patterns,
              and works where internet is unreliable.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/tutor"
                className="flex items-center justify-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold px-8 py-4 rounded-xl transition-colors text-lg"
              >
                <GraduationCap className="w-5 h-5" />
                Start Learning
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                href="/design"
                className="flex items-center justify-center gap-2 bg-dark-800 hover:bg-dark-700 border border-dark-600 text-white font-semibold px-8 py-4 rounded-xl transition-colors text-lg"
              >
                <Palette className="w-5 h-5" />
                Generate Pattern
              </Link>
            </div>
          </div>
        </section>

        {/* Stats */}
        <section className="border-y border-dark-800 bg-dark-900/50">
          <div className="max-w-5xl mx-auto px-4 py-10 grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map(({ label, value }) => (
              <div key={label} className="text-center">
                <div className="text-3xl font-bold gradient-text mb-1">{value}</div>
                <div className="text-sm text-dark-400">{label}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Features */}
        <section className="max-w-6xl mx-auto px-4 py-20">
          <h2 className="text-3xl font-bold text-center mb-4">Everything a tailor needs</h2>
          <p className="text-dark-400 text-center mb-12 max-w-xl mx-auto">
            From learning the basics to running a fashion business — all powered by AI that
            works side-by-side with you.
          </p>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map(({ href, icon: Icon, title, description, badge, color }) => (
              <Link
                key={href}
                href={href}
                className="group bg-dark-800 border border-dark-700 rounded-2xl p-6 card-hover flex flex-col gap-4"
              >
                <div className="flex items-start justify-between">
                  <div className={`w-12 h-12 bg-gradient-to-br ${color} rounded-xl flex items-center justify-center`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <span className="text-xs bg-dark-700 text-dark-300 px-2.5 py-1 rounded-full">{badge}</span>
                </div>
                <div>
                  <h3 className="font-semibold text-lg mb-2 group-hover:text-brand-400 transition-colors">{title}</h3>
                  <p className="text-dark-400 text-sm leading-relaxed">{description}</p>
                </div>
                <div className="flex items-center gap-1 text-brand-500 text-sm font-medium mt-auto">
                  Open <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </Link>
            ))}
          </div>
        </section>

        {/* Offline feature callout */}
        <section className="max-w-6xl mx-auto px-4 pb-20">
          <div className="bg-gradient-to-br from-amber-600/10 to-brand-600/10 border border-amber-600/20 rounded-2xl p-8 md:p-12 flex flex-col md:flex-row items-center gap-8">
            <div className="flex-shrink-0 w-20 h-20 bg-amber-600/20 rounded-2xl flex items-center justify-center">
              <WifiOff className="w-10 h-10 text-amber-400" />
            </div>
            <div>
              <h3 className="text-2xl font-bold mb-3">Built for low-connectivity environments</h3>
              <p className="text-dark-300 leading-relaxed max-w-2xl">
                Most AI apps stop working without reliable internet. Aku doesn&apos;t. Lessons are
                cached locally, questions queue offline and sync when you&apos;re back online, and
                pattern generation works client-side. Because tailors in Lagos, Accra, and Nairobi
                deserve great tools too.
              </p>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="border-t border-dark-800 px-4 py-10 text-center text-dark-500 text-sm">
          <div className="flex items-center justify-center gap-2 mb-2">
            <div className="w-6 h-6 bg-brand-600 rounded flex items-center justify-center">
              <Scissors className="w-3.5 h-3.5 text-white" />
            </div>
            <span className="font-semibold text-white">Aku Fashion</span>
          </div>
          <p>Built for OpenAI Build Week · GPT-5.6 + Codex working side-by-side</p>
          <p className="mt-1">Empowering tailors and fashion students across Africa 🌍</p>
        </footer>
      </main>
    </>
  )
}
