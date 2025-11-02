from elasticsearch import Elasticsearch

es = Elasticsearch(["http://localhost:9200"])

# Проверяем существование индекса
if es.indices.exists(index="habr_articles"):
    print("Индекс habr_articles создан успешно!")

    # Получаем информацию об индексе
    index_info = es.indices.get(index="habr_articles")
    print("Настройки индекса:")
    print(f"   - Анализатор: {list(index_info['habr_articles']['settings']['index'].get('analysis', {}).keys())}")

    # Считаем количество документов
    count = es.count(index="habr_articles")['count']
    print(f"Документов в индексе: {count}")
else:
    print("Индекс habr_articles не найден")