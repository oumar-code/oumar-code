import type { Metadata } from 'next'
import { Toaster } from 'react-hot-toast'
import './globals.css'

export const metadata: Metadata = {
  title: 'Aku Fashion — AI Tailoring & Fashion Skills',
  description:
    'Learn tailoring and fashion design with an AI tutor that works even without reliable internet. ' +
    'Built for tailors, fashion students, and learners across Africa.',
  keywords: [
    'tailoring', 'fashion', 'AI tutor', 'sewing', 'pattern drafting',
    'ankara', 'African fashion', 'offline-first', 'skills',
  ],
  authors: [{ name: 'Oumar' }],
  openGraph: {
    title: 'Aku Fashion — AI Tailoring & Fashion Skills',
    description: 'AI-powered tailoring tutor and fashion co-pilot. Works offline.',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#e85f00" />
      </head>
      <body className="bg-dark-900 text-white min-h-screen font-sans">
        {children}
        <Toaster
          position="bottom-right"
          toastOptions={{
            style: {
              background: '#1a1a1a',
              color: '#fff',
              border: '1px solid #333',
            },
          }}
        />
      </body>
    </html>
  )
}
