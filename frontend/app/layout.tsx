import type { Metadata } from 'next';
import { IBM_Plex_Mono, Space_Grotesk } from 'next/font/google';
import type { ReactNode } from 'react';

import './globals.css';
import { Providers } from '../components/Providers';

const sans = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-sans',
});

const mono = IBM_Plex_Mono({
  subsets: ['latin'],
  weight: ['400', '500'],
  variable: '--font-mono',
});

export const metadata: Metadata = {
  title: 'InsureFlow | AI Insurance Recommendation Dashboard',
  description:
    'Customer-facing AI insurance recommendation dashboard powered by Google ADK, Gemini, SQL tools, and RAG.',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang='en'>
      <body className={`${sans.variable} ${mono.variable}`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
