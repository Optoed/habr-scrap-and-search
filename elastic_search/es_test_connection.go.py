from elasticsearch import Elasticsearch

# Подключаемся к Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

# Проверяем подключение
if es.ping():
    print("Успешное подключение к Elasticsearch!")

    # Получаем информацию о кластере
    info = es.info()
    print(f"Версия Elasticsearch: {info['version']['number']}")
    print(f"Имя кластера: {info['cluster_name']}")
    print(f"Имя узла: {info['name']}")

    # Проверяем существующие индексы
    indices = es.cat.indices(format="json")
    print(f"Количество индексов: {len(indices)}")

else:
    print("Не удалось подключиться к Elasticsearch")