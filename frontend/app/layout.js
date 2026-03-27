import './globals.css'
import { Providers } from './providers'
import Navbar from './components/Navbar'

export const metadata = {
  title: 'Autonomous AI Travel Planner',
  description: 'AI-driven personalized travel plans and vacation planning.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <Navbar />
          <main className="container">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  )
}
