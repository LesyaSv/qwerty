import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI

logger = logging.getLogger("uvicorn.error")

class SimilarItems:

    def __init__(self):
        self._similar_items = None

    def load(self, path, **kwargs):
        """
        Загружаем данные из файла
        """
        logger.info(f"Loading data from {path}")
        self._similar_items = pd.read_parquet(path, **kwargs)
        # Убедимся, что у нас есть нужные столбцы
        if not all(col in self._similar_items.columns for col in ["item_id_1", "item_id_2", "similar_score"]):
            logger.error("Data does not contain required columns")
            raise ValueError("Data must contain item_id_1, item_id_2, and score columns")
        # Индексируем данные для быстрого доступа
        self._similar_items.set_index("item_id_1", inplace=True)
        logger.info("Loaded")

    def get(self, item_id: int, k: int = 9):
        """
        Возвращает список похожих объектов
        """
        try:
            i2i = self._similar_items.loc[item_id].head(k)
            i2i = i2i.round(2)
            i2i = i2i[["item_id_2", "similar_score"]].to_dict(orient="list")

        except KeyError:
            logger.error("No recommendations found for item_id: %s", item_id)
            i2i = {"item_id_2": [], "similar_score": []}

        return i2i

sim_items_store = SimilarItems()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # код ниже (до yield) выполнится только один раз при запуске сервиса
    sim_items_store.load(
        path="./similar_items.parquet",  # Замените на путь к вашему файлу
        columns=["item_id_1", "item_id_2", "similar_score"],
    )
    logger.info("Ready!")
    # код ниже выполнится только один раз при остановке сервиса
    yield

# создаём приложение FastAPI
app = FastAPI(title="features", lifespan=lifespan)

@app.post("/similar_items")
async def recommendations(item_id: int, k: int = 9):
    """
    Возвращает список похожих объектов длиной k для item_id
    """
    i2i = sim_items_store.get(item_id, k)
    logger.info(i2i)
    return {"i2i": i2i}
