import { useEffect, useState, useCallback } from 'react';
import io from 'socket.io-client';

const WS_URL = process.env.REACT_APP_WS_URL || 'http://localhost:5000';

export const useWebSocket = () => {
  const [socket, setSocket] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [latestBrief, setLatestBrief] = useState(null);

  useEffect(() => {
    const socketInstance = io(WS_URL, {
      transports: ['websocket'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5
    });

    socketInstance.on('connect', () => {
      console.log('WebSocket已连接');
      setIsConnected(true);
    });

    socketInstance.on('disconnect', () => {
      console.log('WebSocket已断开');
      setIsConnected(false);
    });

    socketInstance.on('connected', (data) => {
      console.log('服务器欢迎消息:', data);
    });

    socketInstance.on('news:update', (brief) => {
      console.log('收到新简报:', brief);
      setLatestBrief(brief);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.disconnect();
    };
  }, []);

  const subscribeCategory = useCallback((category) => {
    if (socket) {
      socket.emit('subscribe:category', category);
    }
  }, [socket]);

  const unsubscribeCategory = useCallback((category) => {
    if (socket) {
      socket.emit('unsubscribe:category', category);
    }
  }, [socket]);

  return {
    socket,
    isConnected,
    latestBrief,
    subscribeCategory,
    unsubscribeCategory
  };
};
