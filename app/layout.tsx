import type { Metadata } from 'next'
import { Geist, Geist_Mono } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import './globals.css'

const _geist = Geist({ subsets: ["latin"] });
const _geistMono = Geist_Mono({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: 'Iside Systems SRLS',
  description: 'Software, AI, Audio - Consulenza e sviluppo a Milano',
  generator: 'v0.app',
  keywords: ['software', 'AI', 'audio', 'consulenza', 'Milano', 'sviluppo'],
  authors: [{ name: 'Alessandro Saccoia', url: 'https://www.alessandrosaccoia.com' }],
  openGraph: {
    title: 'Iside Systems SRLS',
    description: 'Software, AI, Audio - Consulenza e sviluppo a Milano',
    url: 'https://isidesystems.com',
    siteName: 'Iside Systems SRLS',
    locale: 'it_IT',
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'Iside Systems SRLS',
    description: 'Software, AI, Audio - Consulenza e sviluppo a Milano',
  },
  robots: {
    index: true,
    follow: true,
  },
  icons: {
    icon: [
      {
        url: '/icon-light-32x32.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        url: '/icon-dark-32x32.png',
        media: '(prefers-color-scheme: dark)',
      },
      {
        url: '/icon.svg',
        type: 'image/svg+xml',
      },
    ],
    apple: '/apple-icon.png',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="it" className="bg-background">
      <body className="font-sans antialiased">
        {children}
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
