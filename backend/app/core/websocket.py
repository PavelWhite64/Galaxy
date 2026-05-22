"""
WebSocket connection manager for real-time communication.
"""
from typing import Dict, List, Optional
from fastapi import WebSocket


class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        # Store active connections: {user_id: websocket}
        self.active_connections: Dict[int, WebSocket] = {}
        # Store room subscriptions: {room_name: [user_ids]}
        self.rooms: Dict[str, List[int]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int) -> None:
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: int) -> None:
        """Remove a disconnected user."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        # Remove from all rooms
        for room_name in list(self.rooms.keys()):
            if user_id in self.rooms[room_name]:
                self.rooms[room_name].remove(user_id)
                if not self.rooms[room_name]:
                    del self.rooms[room_name]
    
    async def send_personal_message(self, message: dict, user_id: int) -> None:
        """Send a message to a specific user."""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_json(message)
            except Exception:
                self.disconnect(user_id)
    
    async def broadcast_to_room(self, message: dict, room_name: str) -> None:
        """Broadcast a message to all users in a room."""
        if room_name in self.rooms:
            for user_id in self.rooms[room_name]:
                await self.send_personal_message(message, user_id)
    
    async def join_room(self, user_id: int, room_name: str) -> None:
        """Add a user to a room."""
        if room_name not in self.rooms:
            self.rooms[room_name] = []
        if user_id not in self.rooms[room_name]:
            self.rooms[room_name].append(user_id)
    
    async def leave_room(self, user_id: int, room_name: str) -> None:
        """Remove a user from a room."""
        if room_name in self.rooms and user_id in self.rooms[room_name]:
            self.rooms[room_name].remove(user_id)
    
    async def broadcast(self, message: dict) -> None:
        """Broadcast a message to all connected users."""
        for user_id in list(self.active_connections.keys()):
            await self.send_personal_message(message, user_id)


# Global instance
manager = ConnectionManager()
