from elasticsearch import Elasticsearch
import logging
from datetime import datetime
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HabrSearchEngine:
    def __init__(self):
        self.es = Elasticsearch(["http://localhost:9200"])
        if not self.es.ping():
            raise ConnectionError("Не удалось подключиться к Elasticsearch")

    def smart_spell_check(self, query):
        """Умная проверка орфографии через Yandex Speller API"""
        try:
            # Yandex Speller API
            url = "https://speller.yandex.net/services/spellservice.json/checkText"
            params = {
                'text': query,
                'lang': 'ru,en',  # Русский и английский
                'options': 518  # Игнорировать цифры, URLs и т.д.
            }

            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                corrections = response.json()

                if corrections:
                    corrected_query = query
                    corrections_list = []

                    for correction in corrections:
                        if correction.get('s'):
                            corrected_word = correction['s'][0]
                            original_word = correction['word']
                            corrected_query = corrected_query.replace(original_word, corrected_word)
                            corrections_list.append(f"'{original_word}' → '{corrected_word}'")

                    if corrected_query != query:
                        print(f"\nНайдены возможные опечатки:")
                        for correction in corrections_list:
                            print(f"   {correction}")

                        while True:
                            choice = input(f"\nИсправить на '{corrected_query}'? (y/n): ").strip().lower()
                            if choice in ['y', 'yes', 'да', 'д']:
                                return corrected_query
                            elif choice in ['n', 'no', 'нет', 'н']:
                                return query
                            else:
                                print("Пожалуйста, введите 'y' (да) или 'n' (нет)")

            return query

        except Exception as e:
            logger.warning(f"Ошибка проверки орфографии: {e}")
            return query

    def is_exact_phrase(self, query):
        """Проверяет, является ли запрос точной фразой в кавычках"""
        # Проверяем разные типы кавычек
        quote_pairs = [
            ('"', '"'),
            ('«', '»'),
            ('“', '”'),
            ("'", "'")
        ]

        for open_quote, close_quote in quote_pairs:
            if query.startswith(open_quote) and query.endswith(close_quote):
                return True

        return False

    def extract_phrase_from_quotes(self, query):
        """Извлекает фразу из кавычек"""
        if query.startswith('"') and query.endswith('"'):
            return query[1:-1]
        elif query.startswith('«') and query.endswith('»'):
            return query[1:-1]
        elif query.startswith('“') and query.endswith('”'):
            return query[1:-1]
        elif query.startswith("'") and query.endswith("'"):
            return query[1:-1]
        return query

    def should_use_spell_check(self, query):
        """Определяем, нужно ли использовать проверку орфографии"""
        # Не проверяем точные фразы в кавычках
        if self.is_exact_phrase(query):
            print("Используется поиск точной фразы (без исправлений)")
            return False

        return True

    def search_articles(self, query, size=10, search_type="simple"):
        """Поиск статей с различными типами запросов"""

        # Обрабатываем точные фразы в кавычках
        if self.is_exact_phrase(query):
            exact_phrase = self.extract_phrase_from_quotes(query)
            search_body = {
                "query": {
                    "match_phrase": {
                        "text": {
                            "query": exact_phrase,
                            "slop": 2  # Допускаем небольшое расстояние между словами
                        }
                    }
                },
                "highlight": {
                    "fields": {
                        "title": {},
                        "text": {"fragment_size": 150, "number_of_fragments": 3},
                        "hubs": {},
                        "tags": {}
                    }
                }
            }

            try:
                response = self.es.search(
                    index="habr_articles",
                    body=search_body,
                    size=size
                )
                return response
            except Exception as e:
                logger.error(f"Ошибка поиска точной фразы: {e}")
                return None

        # Умная проверка орфографии для простого поиска
        if search_type == "simple" and self.should_use_spell_check(query):
            corrected_query = self.smart_spell_check(query)
            if corrected_query != query:
                query = corrected_query

        if search_type == "exact":
            # ТОЧНЫЙ поиск без опечаток
            search_body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^3", "text^2", "hubs^2", "tags^2", "author"],
                        "operator": "and"  # Все слова должны быть
                    }
                },
                "highlight": {
                    "fields": {
                        "title": {},
                        "text": {"fragment_size": 150, "number_of_fragments": 3},
                        "hubs": {},
                        "tags": {}
                    }
                }
            }
        elif search_type == "simple":
            # Простой поиск с умной проверкой орфографии
            search_body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^3", "text^2", "hubs^2", "tags^2", "author"],
                        "operator": "or"
                    }
                },
                "highlight": {
                    "fields": {
                        "title": {},
                        "text": {"fragment_size": 150, "number_of_fragments": 3},
                        "hubs": {},
                        "tags": {}
                    }
                }
            }
        elif search_type == "advanced":
            # Расширенный поиск
            search_body = {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "title": {
                                        "query": query,
                                        "boost": 3
                                    }
                                }
                            },
                            {
                                "match": {
                                    "text": {
                                        "query": query,
                                        "boost": 2
                                    }
                                }
                            },
                            {
                                "match": {
                                    "hubs": {
                                        "query": query,
                                        "boost": 2
                                    }
                                }
                            },
                            {
                                "match": {
                                    "tags": {
                                        "query": query,
                                        "boost": 2
                                    }
                                }
                            }
                        ]
                    }
                },
                "highlight": {
                    "fields": {
                        "title": {},
                        "text": {"fragment_size": 150, "number_of_fragments": 3},
                        "hubs": {},
                        "tags": {}
                    }
                }
            }

        try:
            response = self.es.search(
                index="habr_articles",
                body=search_body,
                size=size
            )
            return response
        except Exception as e:
            logger.error(f"Ошибка поиска: {e}")
            return None

    def format_search_results(self, results):
        """Форматирует результаты поиска для красивого вывода"""

        if not results or 'hits' not in results or 'hits' not in results['hits']:
            print("Ничего не найдено")
            print("Попробуйте:")
            print("   - Изменить запрос")
            print("   - Использовать другой режим поиска")
            print("   - Проверить орфографию")
            return

        total = results['hits']['total']['value']
        hits = results['hits']['hits']

        print(f"\nНайдено результатов: {total}")
        print("=" * 80)

        for i, hit in enumerate(hits, 1):
            source = hit['_source']
            score = hit['_score']

            print(f"\n{i}. [{score:.2f}] {source['title']}")
            print(f"   Автор: {source.get('author', 'Неизвестен')}")

            if 'date' in source:
                try:
                    date = datetime.fromisoformat(source['date'].replace('Z', '+00:00'))
                    print(f"   Дата: {date.strftime('%d.%m.%Y %H:%M')}")
                except:
                    print(f"   Дата: {source['date']}")

            # Выводим хабы и теги
            if source.get('hubs'):
                print(f"   Хабы: {', '.join(source['hubs'][:3])}")
            if source.get('tags'):
                print(f"   Теги: {', '.join(source['tags'][:3])}")

            # Выводим подсветку
            if 'highlight' in hit:
                if 'title' in hit['highlight']:
                    highlighted = hit['highlight']['title'][0].replace('<em>', '**').replace('</em>', '**')
                    print(f"   Заголовок: ...{highlighted}...")
                if 'text' in hit['highlight']:
                    for fragment in hit['highlight']['text'][:2]:
                        cleaned = fragment.replace('<em>', '**').replace('</em>', '**')
                        print(f"   Текст: ...{cleaned}...")

            print(f"   URL: {source['url']}")
            print("-" * 80)


def main():
    try:
        search_engine = HabrSearchEngine()
        print("🔍 Умная поисковая система Habr")
        print("Доступные команды:")
        print("  /exact   - точный поиск (без исправлений)")
        print("  /simple  - простой поиск (с умными исправлениями)")
        print("  /advanced - расширенный поиск")
        print("  /exit    - выход")
        print("\n✨ Особенности:")
        print("  - Интерактивное исправление опечаток")
        print("  - Поиск точных фраз в кавычках")
        print("  - Умные подсказки")
        print("\nПримеры:")
        print("  /exact русы против ящеров")
        print("  /simple пайтон машинное обyчение")
        print("  /advanced база данных")
        print('  "точная фраза в кавычках"')
        print('  «русские кавычки тоже работают»')

        while True:
            try:
                user_input = input("\nВведите запрос: ").strip()

                if user_input.lower() in ['/exit', 'exit', 'quit']:
                    break
                elif user_input.startswith('/exact '):
                    query = user_input[7:]
                    search_type = "exact"
                elif user_input.startswith('/simple '):
                    query = user_input[8:]
                    search_type = "simple"
                elif user_input.startswith('/advanced '):
                    query = user_input[10:]
                    search_type = "advanced"
                else:
                    # По умолчанию используем простой поиск
                    query = user_input
                    search_type = "simple"

                if not query:
                    continue

                print(f"\nПоиск: '{query}' (режим: {search_type})")

                results = search_engine.search_articles(query, size=10, search_type=search_type)
                search_engine.format_search_results(results)

            except KeyboardInterrupt:
                print("\nВыход...")
                break
            except Exception as e:
                logger.error(f"Ошибка: {e}")

    except ConnectionError as e:
        print(f"Ошибка: {e}")
        print("Убедитесь, что Elasticsearch запущен на localhost:9200")


if __name__ == "__main__":
    main()