'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Scissors, GraduationCap, Briefcase, Palette, Star, Users } from 'lucide-react'
import { clsx } from 'clsx'

const navItems = [
  { href: '/', label: 'Home', icon: Scissors },
  { href: '/tutor', label: 'Tutor', icon: GraduationCap },
  { href: '/copilot', label: 'Co-pilot', icon: Briefcase },
  { href: '/design', label: 'Design', icon: Palette },
  { href: '/skills', label: 'Skills', icon: Star },
  { href: '/gallery', label: 'Gallery', icon: Users },
]

export function Navbar() {
  const pathname = usePathname()

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-dark-900/80 backdrop-blur-xl border-b border-dark-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-brand-500 to-brand-700 rounded-lg flex items-center justify-center">
              <Scissors className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-lg gradient-text">Aku Fashion</span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-1">
            {navItems.map(({ href, label, icon: Icon }) => (
              <Link
                key={href}
                href={href}
                className={clsx(
                  'flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                  pathname === href
                    ? 'bg-brand-600 text-white'
                    : 'text-dark-300 hover:text-white hover:bg-dark-800'
                )}
              >
                <Icon className="w-4 h-4" />
                {label}
              </Link>
            ))}
          </div>

          {/* Build Week badge */}
          <div className="hidden md:flex items-center gap-2 text-xs text-dark-400">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            OpenAI Build Week
          </div>
        </div>
      </div>

      {/* Mobile bottom nav */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-dark-900/95 backdrop-blur-xl border-t border-dark-700 px-2 py-2 flex justify-around">
        {navItems.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className={clsx(
              'flex flex-col items-center gap-0.5 p-2 rounded-lg text-xs font-medium transition-colors',
              pathname === href
                ? 'text-brand-400'
                : 'text-dark-400 hover:text-white'
            )}
          >
            <Icon className="w-5 h-5" />
            <span className="text-[10px]">{label}</span>
          </Link>
        ))}
      </div>
    </nav>
  )
}
