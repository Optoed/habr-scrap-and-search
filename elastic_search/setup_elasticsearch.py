import os

from elasticsearch import Elasticsearch
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_habr_index(es_client):
    """Создает индекс для статей Habr с русским анализатором"""

    index_settings = {
        "settings": {
            "analysis": {
                "filter": {
                    "russian_stop": {
                        "type": "stop",
                        "stopwords": "_russian_"
                    },
                    "russian_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    },
                    "russian_synonyms": {
                        "type": "synonym",
                        "synonyms": [
                            "программирование, кодинг, разработка",
                            "js, javascript, джаваскрипт",
                            "js фреймворки, javascript фреймворки, javascript фреймворк, react, react.js, vue.js, vue, angular",
                            "python, питон, пайтон",
                            "java, джава, java spring",
                            "c++, cpp, плюсы",
                            "ai, искусственный интеллект, ml, машинное обучение, мл",
                            "db, база данных, database, бд",
                            "api, интерфейс программирования, апи, апишка",
                            "web, веб, интернет, инет",
                            "mobile, мобильный, android, ios"
                        ]
                    }
                },
                "analyzer": {
                    "russian_analyzer": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "russian_stop",
                            "russian_stemmer",
                            "russian_synonyms"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "url": {"type": "keyword"},
                "title": {
                    "type": "text",
                    "analyzer": "russian_analyzer",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "author": {
                    "type": "text",
                    "analyzer": "russian_analyzer"
                },
                "date": {"type": "date"},
                "hubs": {
                    "type": "text",
                    "analyzer": "russian_analyzer"
                },
                "tags": {
                    "type": "text",
                    "analyzer": "russian_analyzer"
                },
                "text": {
                    "type": "text",
                    "analyzer": "russian_analyzer"
                }
            }
        }
    }

    # Удаляем индекс если существует
    if es_client.indices.exists(index="habr_articles"):
        es_client.indices.delete(index="habr_articles")

    # Создаем новый индекс
    es_client.indices.create(index="habr_articles", body=index_settings)
    logger.info("Индекс habr_articles создан успешно")


def index_articles(es_client, jsonl_file_path):
    """Индексирует статьи из JSONL файла в Elasticsearch"""

    with open(jsonl_file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            try:
                article = json.loads(line.strip())

                # Индексируем документ
                es_client.index(
                    index="habr_articles",
                    id=i + 1,
                    document=article
                )

                if (i + 1) % 100 == 0:
                    logger.info(f"Проиндексировано {i + 1} статей")

            except json.JSONDecodeError as e:
                logger.warning(f"Ошибка парсинга строки {i}: {e}")
                continue

    # Обновляем индекс чтобы все документы стали доступны для поиска
    es_client.indices.refresh(index="habr_articles")
    logger.info("Индексация завершена")


def main():
    # Подключаемся к Elasticsearch
    es = Elasticsearch(["http://localhost:9200"])

    # Проверяем подключение
    if not es.ping():
        logger.error("Не удалось подключиться к Elasticsearch. Убедитесь, что он запущен на localhost:9200")
        return

    logger.info("Успешное подключение к Elasticsearch")

    # Создаем индекс
    create_habr_index(es)

    # Указываем правильный путь к файлу
    jsonl_path = "../habr_articles_by_id.jsonl"

    # Проверяем что файл существует
    if not os.path.exists(jsonl_path):
        logger.error(f"Файл {jsonl_path} не найден!")
        return

    logger.info(f"Найден файл с данными: {jsonl_path}")

    # Индексируем статьи
    index_articles(es, jsonl_path)

    # Выводим статистику
    stats = es.count(index="habr_articles")
    logger.info(f"Всего документов в индексе: {stats['count']}")


if __name__ == "__main__":
    main()