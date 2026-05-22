import { io, Socket } from 'socket.io-client';

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

let socket: Socket | null = null;

export const getSocket = (): Socket => {
  if (!socket) {
    socket = io(WS_URL, {
      transports: ['websocket'],
      autoConnect: false,
    });
  }
  return socket;
};

export const connectSocket = (token?: string): Promise<Socket> => {
  return new Promise((resolve, reject) => {
    const s = getSocket();
    
    if (token) {
      s.auth = { token };
    }

    s.on('connect', () => {
      console.log('WebSocket connected');
      resolve(s);
    });

    s.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
      reject(error);
    });

    s.connect();
  });
};

export const disconnectSocket = (): void => {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
};

export default {
  getSocket,
  connectSocket,
  disconnectSocket,
};
