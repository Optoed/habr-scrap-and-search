import requests
from bs4 import BeautifulSoup
import time
import random
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
]


def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
    }


def smart_find_text(soup, selectors):
    """Умный поиск текста по нескольким селекторам"""
    for selector in selectors:
        element = soup.select_one(selector)
        if element and element.text.strip():
            return element.text.strip()
    return None


def smart_find_list(soup, selectors):
    """Умный поиск списка элементов"""
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            return [elem.text.strip() for elem in elements if elem.text.strip()]
    return []


def parse_article_page(html, url):
    """Парсит страницу статьи"""
    soup = BeautifulSoup(html, 'lxml')

    # Проверяем, есть ли статья на странице (не 404)
    if soup.find('div', class_='tm-error-message'):
        return None

    title = smart_find_text(soup, ['h1', '.tm-title', '[class*="title"]'])
    author = smart_find_text(soup, ['.tm-user-info__username', '.tm-user-info__user', '[class*="author"]'])

    date = None
    time_tag = soup.find('time')
    if time_tag:
        date = time_tag.get('datetime')

    hubs = smart_find_list(soup, ['.tm-publication-hubs__hub-link', '[class*="hub"]'])
    tags = smart_find_list(soup, ['.tm-publication__label', '[class*="tag"]'])

    text = None
    text_element = soup.select_one('.article-formatted-body')
    if text_element:
        text = text_element.get_text(separator='\n', strip=True)

    # Если нет текста или заголовка, значит это не статья
    if not title or not text:
        return None

    return {
        'url': url,
        'title': title,
        'author': author,
        'date': date,
        'hubs': hubs,
        'tags': tags,
        'text': text
    }


def fetch_article(article_id, session):
    """Загружает и парсит статью по ID"""
    url = f"https://habr.com/ru/articles/{article_id}/"

    try:
        response = session.get(url, headers=get_random_headers(), timeout=10)

        # Пропускаем 404 и другие ошибки
        if response.status_code != 200:
            return None

        # Проверяем на Cloudflare
        if 'cf-challenge' in response.text.lower():
            logger.warning(f"Cloudflare защита обнаружена на {url}")
            return None

        return parse_article_page(response.text, url)

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе {url}: {e}")
        return None


def main():
    session = requests.Session()
    collected_articles = 0
    target_articles = 5000  # Цель - 5000 статей

    # Начинаем с относительно свежих статей (более высокая вероятность существования)
    start_id = 900000
    current_id = start_id

    logger.info(f"Начинаем сбор {target_articles} статей, начиная с ID {start_id}")

    with open('habr_articles_by_id.jsonl', 'w', encoding='utf-8') as f:
        while collected_articles < target_articles:
            logger.info(f"Пробуем ID {current_id}, собрано {collected_articles}/{target_articles}")

            article_data = fetch_article(current_id, session)

            if article_data:
                # Сохраняем статью
                f.write(json.dumps(article_data, ensure_ascii=False) + '\n')
                f.flush()

                collected_articles += 1
                logger.info(f"✅ Найдена статья #{collected_articles}: {article_data['title'][:50]}...")

                # Короткая пауза после успешного найденной статьи
                # time.sleep(random.uniform(0.5, 1.5))
            # else:
                # Более короткая пауза после пропуска
                # time.sleep(random.uniform(0.1, 0.3))

            # Переходим к следующему ID
            current_id += 1

            # Периодически сохраняем прогресс
            if current_id % 100 == 0:
                logger.info(f"Прогресс: проверено {current_id - start_id} ID, найдено {collected_articles} статей")

    logger.info(f"Скрапинг завершен! Собрано {collected_articles} статей.")


if __name__ == "__main__":
    main()