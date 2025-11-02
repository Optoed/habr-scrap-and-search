import requests
from bs4 import BeautifulSoup
import json


def debug_page(url):
    """Анализирует структуру страницы для отладки"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    print("=== ДЕБАГ СТРАНИЦЫ ===")
    print(f"URL: {url}")
    print(f"Title: {soup.find('title').text if soup.find('title') else 'No title'}")
    print()

    # Ищем все возможные элементы с классами, содержащими ключевые слова
    keywords = ['hub', 'tag', 'author', 'body', 'content', 'text', 'article']

    for keyword in keywords:
        elements = soup.find_all(class_=lambda x: x and keyword in x.lower())
        if elements:
            print(f"=== Элементы с '{keyword}': ===")
            for i, elem in enumerate(elements[:3]):  # Покажем первые 3
                print(f"{i + 1}. Class: {elem.get('class')}")
                print(f"   Text: {elem.text.strip()[:100]}...")
                print(f"   Tag: {elem.name}")
                print()

    # Сохраним HTML для ручного анализа
    with open('debug_page.html', 'w', encoding='utf-8') as f:
        f.write(response.text)

    print("HTML сохранен в debug_page.html для ручного анализа")


# Проанализируем одну статью
debug_page('https://habr.com/ru/articles/948908/')