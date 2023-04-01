import { useState, useEffect } from "react";

const useWebSocket = () => {
  const [webSocket, setWebSocket] = useState(null);
  const [status, setStatus] = useState("disconnected");

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:9000");
    socket.onopen = () => {
      setStatus("connected");
    };
    socket.onclose = () => {
      setStatus("disconnected");
    };
    setWebSocket(socket);

    return () => {
      socket.close();
    };
  }, []);

  return [webSocket, status];
};

export default useWebSocket;
