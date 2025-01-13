import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles 
from contextlib import asynccontextmanager

import requests
from recommendations import Recommendations

logger = logging.getLogger("uvicorn.error")
logging.basicConfig(filename="test_service.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


features_store_url = "http://127.0.0.1:8020"
events_store_url = "http://127.0.0.1:8010" 

rec_store = Recommendations()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # код ниже (до yield) выполнится только один раз при запуске сервиса
    logger.info("Starting")
    
    rec_store.load(
        "personal",
        "./recommendations.parquet",
        columns=["user_id", "item_id", "cb_score"])
    rec_store.load(
        "default",
        "./top_popular_2.parquet",
        columns=["item_id", "popularity_score"])
    
    
    yield

    # этот код выполнится только один раз при остановке сервиса
    logger.info("Stopping")

app = FastAPI(title="recommendations", lifespan=lifespan)


@app.post("/recommendations_offline")
async def recommendations_offline(user_id: int, k: int = 100):
    """
    Возвращает список рекомендаций длиной k для пользователя user_id
    """
    recs = rec_store.get(user_id, k)
    return {"recs": recs}

def dedup_ids(ids):
    """
    Дедублицирует список идентификаторов, оставляя только первое вхождение
    """
    seen = set()
    ids = [id for id in ids if not (id in seen or seen.add(id))]

    return ids

@app.post("/recommendations_online")
async def recommendations_online(user_id: int, k: int = 100):
    """
    Возвращает список онлайн-рекомендаций длиной k для пользователя user_id
    """

    headers = {"Content-type": "application/json", "Accept": "text/plain"}

    # получаем 3 последние события пользователя
    params = {"user_id": user_id, "k": 3}
    resp = requests.post(events_store_url + "/get", headers=headers, params=params)
    events = resp.json()
    events = events["events"]

    # получаем список айтемов, похожих на последние три, с которыми взаимодействовал пользователь
    items = []
    scores = []
    for item_id in events:
        params = {"item_id": item_id, "k": k}
        resp = requests.post(features_store_url + "/similar_items", headers=headers, params=params)
        
        item_similar_items = resp.json()
        item_similar_items = item_similar_items["i2i"]
        
        items += item_similar_items["item_id_2"]
        scores += item_similar_items["similar_score"]
        
    # сортируем похожие объекты по scores в убывающем порядке
    combined = list(zip(items, scores))
    logger.info(combined)
    combined = sorted(combined, key=lambda x: x[1], reverse=True)
    combined = [item for item, _ in combined]
    # удаляем дубликаты, чтобы не выдавать одинаковые рекомендации
    recs = dedup_ids(combined)

    return {"recs": recs}

@app.post("/recommendations")
async def recommendations(user_id: int, k: int = 100):
    """
    Возвращает список рекомендаций длиной k для пользователя user_id
    """

    recs_offline = await recommendations_offline(user_id, k)
    recs_online = await recommendations_online(user_id, k)

    recs_offline = recs_offline["recs"]
    recs_online = recs_online["recs"]

    recs_blended = []

    min_length = min(len(recs_offline), len(recs_online))
    # чередуем элементы из списков, пока позволяет минимальная длина
    for i in range(min_length):
        recs_blended.append(recs_offline[i])
        recs_blended.append(recs_online[i])

    # добавляем оставшиеся элементы в конец
    if len(recs_offline) > min_length:
        recs_blended.extend(recs_offline[min_length:])
    elif len(recs_online) > min_length:
        recs_blended.extend(recs_online[min_length:])

    # удаляем дубликаты
    recs_blended = dedup_ids(recs_blended)

    # оставляем только первые k рекомендаций
    recs_blended = recs_blended[:k]

    return {"recs": recs_blended}


