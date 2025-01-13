# Подготовка виртуальной машины

## Склонируйте репозиторий

Склонируйте репозиторий проекта:

```
git clone https://github.com/yandex-praktikum/mle-project-sprint-4-v001.git
```

## Активируйте виртуальное окружение

Используйте то же самое виртуальное окружение, что и созданное для работы с уроками. Если его не существует, то его следует создать.

Создать новое виртуальное окружение можно командой:

```
python3 -m venv env_recsys_start
```

После его инициализации следующей командой

```
. env_recsys_start/bin/activate
```

установите в него необходимые Python-пакеты следующей командой

```
pip install -r requirements.txt
```

### Скачайте файлы с данными

Для начала работы понадобится три файла с данными:
- [tracks.parquet](https://storage.yandexcloud.net/mle-data/ym/tracks.parquet)
- [catalog_names.parquet](https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet)
- [interactions.parquet](https://storage.yandexcloud.net/mle-data/ym/interactions.parquet)
 
Скачайте их в директорию локального репозитория. Для удобства вы можете воспользоваться командой wget:

```
wget https://storage.yandexcloud.net/mle-data/ym/tracks.parquet

wget https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet

wget https://storage.yandexcloud.net/mle-data/ym/interactions.parquet

wget https://storage.yandexcloud.net/recsys/data/top_popular.parquet
```

## Запустите Jupyter Lab

Запустите Jupyter Lab в командной строке

```
jupyter lab --ip=0.0.0.0 --no-browser
```

# Расчёт рекомендаций

Код для выполнения первой части проекта находится в файле `recommendations.ipynb`. Изначально, это шаблон. Используйте его для выполнения первой части проекта.

git clone <ссылка-на-ваш-репозиторий>
cd mle-priject-sprint-4-v004
Experiment ID: 49 
Путь recommendations в S3: 's3://s3-student-mle-20240229-5bc7b923c4/49/74b90c3cbd5948d281d50fbe4a50108a/artifacts'

Загрузить рекомендации:
run = client.get_run('74b90c3cbd5948d281d50fbe4a50108a')
artifact_uri = run.info.artifact_riu
mlflow.artifacts.download_artifacts(artifact_uri, dst_path="../fails_recommendation")

# Сервис рекомендаций

Код сервиса рекомендаций находится в файле `recommendations_service.py`.

cd app - переходим в директорию с микросервисом
uvicorn recommendation_service:app - запуск сервиса рекомендаций
uvicorn events_service:app --port 8010  - запуск сервиса Event Store
uvicorn features_service:app --port 8020 - запуск сервиса Feature Store


# Инструкции для тестирования сервиса

Код для тестирования сервиса находится в файле `test_service.py`.
    для пользователя без персональных рекомендаций,
    для пользователя с персональными рекомендациями, но без онлайн-истории,
    для пользователя с персональными рекомендациями и онлайн-историей.

В итоговых рекомендациях смешиваются персональные и оналйн рекомендации путем чередования.

