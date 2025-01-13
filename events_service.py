from fastapi import FastAPI
from collections import deque

class EventStore:
    def __init__(self, max_events_per_user=10):
        self.events = {}
        self.max_events_per_user = max_events_per_user

    def put(self, user_id, item_id):
        """
        Сохраняет событие
        """
        # Получаем события пользователя, если они есть
        user_events = self.events.get(user_id, deque(maxlen=self.max_events_per_user))
        
        # Добавляем новое событие в начало
        user_events.appendleft(item_id)
        
        # Сохраняем обновленный список событий
        self.events[user_id] = user_events
        #user_events = self.events.put(user_id, item_id)
        #self.events[user_id] = [item_id] + user_events[: self.max_events_per_user]
    
    def get(self, user_id, k):
        """
        Возвращает события для пользователя
        """
        user_events = list(self.events[user_id])[:k]
        
        # Возвращаем последние k событий
        return user_events

# Создаём экземпляр EventStore
events_store = EventStore()

# Создаём приложение FastAPI
app = FastAPI(title="events")

@app.post("/put")
async def put(user_id: int, item_id: int):
    """
    Сохраняет событие для user_id, item_id
    """
    events_store.put(user_id, item_id)
    return {"result": "ok"}

@app.post("/get")
async def get(user_id: int, k: int = 10):
    """
    Возвращает список последних k событий для пользователя user_id
    """
    events = events_store.get(user_id, k)
    return {"events": events}
