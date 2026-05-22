'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        <header className="flex justify-between items-center mb-12">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
            Virtual Social World
          </h1>
          <nav className="flex gap-4">
            {!isLoggedIn ? (
              <>
                <button
                  onClick={() => router.push('/login')}
                  className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition"
                >
                  Login
                </button>
                <button
                  onClick={() => router.push('/register')}
                  className="px-6 py-2 border border-gray-600 hover:border-gray-400 rounded-lg transition"
                >
                  Register
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={() => router.push('/map')}
                  className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition"
                >
                  World Map
                </button>
                <button
                  onClick={() => {
                    localStorage.removeItem('access_token');
                    setIsLoggedIn(false);
                    router.push('/');
                  }}
                  className="px-6 py-2 border border-red-600 text-red-500 hover:border-red-400 rounded-lg transition"
                >
                  Logout
                </button>
              </>
            )}
          </nav>
        </header>

        <section className="grid md:grid-cols-2 gap-8 mb-12">
          <div className="bg-gray-900/50 p-8 rounded-xl border border-gray-800">
            <h2 className="text-2xl font-semibold mb-4">🌌 Hierarchical World</h2>
            <p className="text-gray-400 mb-4">
              Explore a deep hierarchy: Galaxy → Planet → Territory → Plot → Object.
              Own land, build structures, and create your own virtual empire.
            </p>
            <ul className="space-y-2 text-gray-300">
              <li>• Multiple levels of ownership</li>
              <li>• Inherited rules and governance</li>
              <li>• Community voting system</li>
            </ul>
          </div>

          <div className="bg-gray-900/50 p-8 rounded-xl border border-gray-800">
            <h2 className="text-2xl font-semibold mb-4">💰 Dual Economy</h2>
            <p className="text-gray-400 mb-4">
              Two currency types: Credits (soft) and Stars (hard).
              Earn through activities or purchase premium content.
            </p>
            <ul className="space-y-2 text-gray-300">
              <li>• Faucet/Sink balance mechanisms</li>
              <li>• Marketplace for trading</li>
              <li>• Transaction audit trail</li>
            </ul>
          </div>
        </section>

        <section className="bg-gray-900/50 p-8 rounded-xl border border-gray-800">
          <h2 className="text-2xl font-semibold mb-4">🏛️ Self-Governance</h2>
          <p className="text-gray-400 mb-6">
            Community-driven rules and decisions. Propose changes, vote on policies,
            and appeal unfair decisions through a transparent governance system.
          </p>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-gray-800/50 p-4 rounded-lg">
              <h3 className="font-semibold mb-2">📋 Proposals</h3>
              <p className="text-sm text-gray-400">Create and discuss new rules</p>
            </div>
            <div className="bg-gray-800/50 p-4 rounded-lg">
              <h3 className="font-semibold mb-2">🗳️ Voting</h3>
              <p className="text-sm text-gray-400">Weight-based community votes</p>
            </div>
            <div className="bg-gray-800/50 p-4 rounded-lg">
              <h3 className="font-semibold mb-2">⚖️ Appeals</h3>
              <p className="text-sm text-gray-400">Fair dispute resolution</p>
            </div>
          </div>
        </section>

        <footer className="mt-12 text-center text-gray-500 text-sm">
          <p>Built with Next.js, FastAPI, PostgreSQL, Redis, and WebSockets</p>
          <p className="mt-2">© 2024 Virtual Social World Platform</p>
        </footer>
      </div>
    </main>
  );
}
