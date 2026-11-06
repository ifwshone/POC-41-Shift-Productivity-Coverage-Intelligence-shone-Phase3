import './globals.css';
import type { Metadata, Viewport } from 'next';
import { Bricolage_Grotesque, DM_Sans, DM_Mono } from 'next/font/google';

const bricolage = Bricolage_Grotesque({
  subsets: ['latin'],
  variable: '--font-bricolage',
});

const dmSans = DM_Sans({
  subsets: ['latin'],
  variable: '--font-dm-sans',
});

const dmMono = DM_Mono({
  subsets: ['latin'],
  weight: ['400', '500'],
  variable: '--font-dm-mono',
});

export const metadata: Metadata = {
  title: 'Shift Productivity & Coverage | Real Rails',
  description: 'Real-Time Operational Intelligence',
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: '#04100b',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${bricolage.variable} ${dmSans.variable} ${dmMono.variable}`} style={{maxWidth:'100vw',overflowX:'hidden'}}>
      <body className="font-sans overflow-x-hidden" style={{maxWidth:'100vw',overflowX:'hidden'}}>{children}</body>
    </html>
  )
}