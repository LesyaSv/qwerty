import requests
import logging
logging.basicConfig(filename='test_service.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

recommendations_url = "http://127.0.0.1:8000"
features_store_url = "http://127.0.0.1:8020"
events_store_url = "http://127.0.0.1:8010"

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


#для пользователя без персональных рекомендаций
user_id = 1024
event_item_ids = [44137831, 51975785, 46409994]

for event_item_id in event_item_ids:
    resp = requests.post(events_store_url + "/put", 
                         headers=headers, 
                         params={"user_id": user_id, "item_id": event_item_id})

params = {"user_id": 1024, 'k': 10}
resp_offline = requests.post(recommendations_url + "/recommendations_offline", headers=headers, params=params)
resp_online = requests.post(recommendations_url + "/recommendations_online", headers=headers, params=params)
resp_blended = requests.post(recommendations_url + "/recommendations", headers=headers, params=params)

recs_offline = resp_offline.json()["recs"]
recs_online = resp_online.json()["recs"]
recs_blended = resp_blended.json()["recs"]

logging.info("Рекомендации для пользователя без персональных рекомендаций:")
logging.info(f"Топ_популярные: {recs_offline}")
logging.info(f"Онлайн рекомендации: {recs_online}")
logging.info(f"Общие рекомендации: {recs_blended}")


#рекомендации для пользователя с персональными рекомендациями, но без онлайн-истории:
params = {"user_id": 3, 'k': 10}

resp = requests.post(events_store_url + "/put", 
                         headers=headers, 
                         params={"user_id": 3, "item_id": 0})

resp_offline = requests.post(recommendations_url + "/recommendations_offline", headers=headers, params=params)
resp_online = requests.post(recommendations_url + "/recommendations_online", headers=headers, params=params)
resp_blended = requests.post(recommendations_url + "/recommendations", headers=headers, params=params)

recs_offline = resp_offline.json()["recs"]
recs_online = resp_online.json()["recs"]
recs_blended = resp_blended.json()["recs"]

logging.info("Рекомендации для пользователя с персональными рекомендациями, но без онлайн истории:")
logging.info(f"Персональные рекомендации: {recs_offline}")
logging.info(f"Онлайн рекомендации: {recs_online}")
logging.info(f"Общие рекомендации: {recs_blended}")


#для пользователя с персональными рекомендациями и онлайн-историей:
user_id = 4
event_item_ids = [44137831, 51975785, 46409994]

for event_item_id in event_item_ids:
    resp = requests.post(events_store_url + "/put", 
                         headers=headers, 
                         params={"user_id": user_id, "item_id": event_item_id})

params = {"user_id": 4, 'k': 10}

resp_offline = requests.post(recommendations_url + "/recommendations_offline", headers=headers, params=params)
resp_online = requests.post(recommendations_url + "/recommendations_online", headers=headers, params=params)
resp_blended = requests.post(recommendations_url + "/recommendations", headers=headers, params=params)

recs_offline = resp_offline.json()["recs"]
recs_online = resp_online.json()["recs"]
recs_blended = resp_blended.json()["recs"]

logging.info("Рекомендации для пользователя с персональными рекомендациями и онлайн историей:")
logging.info(f"Персональные рекомендации: {recs_offline}")
logging.info(f"Онлайн рекомендации: {recs_online}")
logging.info(f"Общие рекомендации: {recs_blended}")



