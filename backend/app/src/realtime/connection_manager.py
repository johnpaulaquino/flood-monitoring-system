import time
from threading import Lock

from fastapi import WebSocket


class ConnectionManager:
     __instance = None
     __lock = Lock()

     def __init__(self):
          self.active_connections: dict[str, WebSocket] = {}

     def __new__(cls, *args, **kwargs):
          with cls.__lock:
               if cls.__instance is None:
                    cls.__instance = super().__new__(*args, **kwargs)
                    time.sleep(0.01)
               return cls.__instance

     async def connect_socket(self, user_id: str, websocket: WebSocket):
          await websocket.accept()
          self.active_connections[user_id] = websocket

     async def disconnect(self, user_id):
          try:
               self.active_connections.pop(user_id)
          except Exception as e:
               raise e

     async def send_personal_messages(self, message, user_id):
          try:
               websocket: WebSocket = self.active_connections.get(user_id)
               if websocket:
                    await websocket.send_json(message)
          except Exception as e:
               raise e

     async def send_message_broadcast(self, message):
          try:
               for k,v in self.active_connections.items():
                    await v.send_json(message)
          except Exception as e:
               raise e
