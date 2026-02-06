import './globals.css';
import type { Metadata } from 'next';
import Providers from './providers';

export const metadata: Metadata = {
  title: 'Modern Todo App',
  description: 'A beautifully designed todo list application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
      </head>
      <body className="bg-gray-50 min-h-screen font-sans">
        <Providers>
          <div className="max-w-4xl mx-auto px-4 py-8">
            {children}
          </div>
        </Providers>
      </body>
    </html>
  );
}
