'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('username');
    if (token) {
      setIsLoggedIn(true);
      if (user) setUsername(user);
    }
  }, []);

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        <header className="flex justify-between items-center mb-12">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
            Виртуальный Социальный Мир
          </h1>
          <nav className="flex gap-4">
            {!isLoggedIn ? (
              <>
                <button
                  onClick={() => router.push('/login')}
                  className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition"
                >
                  Войти
                </button>
                <button
                  onClick={() => router.push('/register')}
                  className="px-6 py-2 border border-gray-600 hover:border-gray-400 rounded-lg transition"
                >
                  Регистрация
                </button>
              </>
            ) : (
              <>
                <span className="px-4 py-2 text-gray-300 flex items-center">
                  👋 {username}
                </span>
                <button
                  onClick={() => router.push('/map')}
                  className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition"
                >
                  Карта мира
                </button>
                <button
                  onClick={() => {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    localStorage.removeItem('username');
                    setIsLoggedIn(false);
                    setUsername('');
                    router.push('/');
                  }}
                  className="px-6 py-2 border border-red-600 text-red-500 hover:border-red-400 rounded-lg transition"
                >
                  Выйти
                </button>
              </>
            )}
          </nav>
        </header>

        <section className="grid md:grid-cols-2 gap-8 mb-12">
          <div className="bg-gray-900/50 p-8 rounded-xl border border-gray-800">
            <h2 className="text-2xl font-semibold mb-4">🌌 Иерархический Мир</h2>
            <p className="text-gray-400 mb-4">
              Исследуйте глубокую иерархию: Галактика → Планета → Территория → Участок → Объект.
              Владейте землёй, стройте сооружения и создавайте свою виртуальную империю.
            </p>
            <ul className="space-y-2 text-gray-300">
              <li>• Многоуровневая система владения</li>
              <li>• Наследуемые правила и управление</li>
              <li>• Система голосования сообщества</li>
            </ul>
          </div>

          <div className="bg-gray-900/50 p-8 rounded-xl border border-gray-800">
            <h2 className="text-2xl font-semibold mb-4">💰 Двойная Экономика</h2>
            <p className="text-gray-400 mb-4">
              Два типа валюты: Кредиты (мягкая) и Звёзды (твёрдая).
              Зарабатывайте через активность или покупайте премиум контент.
            </p>
            <ul className="space-y-2 text-gray-300">
              <li>• Сбалансированные механизмы Faucet/Sink</li>
              <li>• Маркетплейс для торговли</li>
              <li>• Аудит всех транзакций</li>
            </ul>
          </div>
        </section>

        <section className="bg-gray-900/50 p-8 rounded-xl border border-gray-800">
          <h2 className="text-2xl font-semibold mb-4">🏛️ Самоуправление</h2>
          <p className="text-gray-400 mb-6">
            Управление сообществом через правила и решения. Предлагайте изменения, голосуйте за политики,
            подавайте апелляции на несправедливые решения через прозрачную систему управления.
          </p>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-gray-800/50 p-4 rounded-lg">
              <h3 className="font-semibold mb-2">📋 Предложения</h3>
              <p className="text-sm text-gray-400">Создавайте и обсуждайте новые правила</p>
            </div>
            <div className="bg-gray-800/50 p-4 rounded-lg">
              <h3 className="font-semibold mb-2">🗳️ Голосование</h3>
              <p className="text-sm text-gray-400">Взвешенные голоса сообщества</p>
            </div>
            <div className="bg-gray-800/50 p-4 rounded-lg">
              <h3 className="font-semibold mb-2">⚖️ Апелляции</h3>
              <p className="text-sm text-gray-400">Справедливое разрешение споров</p>
            </div>
          </div>
        </section>

        <footer className="mt-12 text-center text-gray-500 text-sm">
          <p>Создано с использованием Next.js, FastAPI, PostgreSQL, Redis и WebSocket</p>
          <p className="mt-2">© 2024 Платформа Виртуальный Социальный Мир</p>
        </footer>
      </div>
    </main>
  );
}
