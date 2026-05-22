'use client';

import { useState, useEffect, useRef } from 'react';
import { getSocket, connectSocket, disconnectSocket } from '@/lib/socket';

interface Message {
  id?: number;
  room: string;
  username: string;
  content: string;
  timestamp?: string;
}

interface ChatBoxProps {
  room?: string;
  username: string;
}

export default function ChatBox({ room = 'global', username }: ChatBoxProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [connected, setConnected] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    
    connectSocket(token)
      .then((socket) => {
        setConnected(true);

        socket.on('chat_message', (data: Message) => {
          setMessages((prev) => [...prev, data]);
        });

        socket.on('disconnect', () => {
          setConnected(false);
        });

        return () => {
          socket.off('chat_message');
        };
      })
      .catch((error) => {
        console.error('Failed to connect to chat:', error);
      });

    return () => {
      disconnectSocket();
    };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = () => {
    if (!input.trim()) return;

    const socket = getSocket();
    if (socket && connected) {
      const message: Message = {
        room,
        username,
        content: input,
        timestamp: new Date().toISOString(),
      };
      
      socket.emit('chat_message', message);
      setInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-96 bg-gray-900 rounded-xl border border-gray-800">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-800">
        <h3 className="font-semibold">Chat {room !== 'global' ? `(${room})` : ''}</h3>
        <div className={`text-xs px-2 py-1 rounded ${connected ? 'bg-green-900 text-green-400' : 'bg-red-900 text-red-400'}`}>
          {connected ? '● Online' : '○ Offline'}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 text-sm mt-8">
            No messages yet. Start the conversation!
          </div>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.username === username ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[70%] p-3 rounded-lg ${
                  msg.username === username
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-200'
                }`}
              >
                {msg.username !== username && (
                  <div className="text-xs font-medium mb-1 opacity-75">{msg.username}</div>
                )}
                <div className="text-sm">{msg.content}</div>
                {msg.timestamp && (
                  <div className="text-xs mt-1 opacity-50">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-800">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type a message..."
            className="flex-1 px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 text-white text-sm"
            disabled={!connected}
          />
          <button
            onClick={sendMessage}
            disabled={!connected || !input.trim()}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-lg font-semibold transition text-sm"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
