import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { FrameData } from '../types/tracking';
import { TacticalEvent } from '../types/events';

const SOCKET_URL = 'http://localhost:5000';

export function useWebSocket() {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [latestFrame, setLatestFrame] = useState<FrameData | null>(null);
  const [tacticalEvents, setTacticalEvents] = useState<TacticalEvent[]>([]);

  useEffect(() => {
    const newSocket = io(SOCKET_URL, {
      transports: ['websocket'],
    });

    newSocket.on('connect', () => {
      console.log('Connected to WebSocket server');
      setIsConnected(true);
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
      setIsConnected(false);
    });

    newSocket.on('tracking_update', (data: FrameData) => {
      setLatestFrame(data);
    });

    newSocket.on('tactical_event', (event: TacticalEvent) => {
      setTacticalEvents((prev) => [...prev, event].slice(-10)); // Keep last 10 events
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  return { isConnected, latestFrame, tacticalEvents };
}
