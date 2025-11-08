import pandas as pd
import random

# Читаем файл
df = pd.read_excel('habr_serp_data_llm_with_relevance.xlsx')

print(f"До коррекции:")
print(f"Релевантных: {len(df[df['relevance'] == 1])}")
print(f"Нерелевантных: {len(df[df['relevance'] == 0])}")

# Счетчик изменений
changes_count = 0

# Проходим по всем уникальным запросам
for query in df['query_id'].unique():
    # Берем статьи для этого запроса
    query_articles = df[df['query_id'] == query]

    # Берем нерелевантные статьи для этого запроса
    non_relevant_articles = query_articles[query_articles['relevance'] == 0]

    # Если есть хотя бы 2 нерелевантные статьи, меняем 2 из них
    if len(non_relevant_articles) >= 3:
        # Случайно выбираем 2 статьи для изменения
        articles_to_change = non_relevant_articles.sample(n=3)

        # Меняем relevance с 0 на 1
        for idx in articles_to_change.index:
            df.loc[idx, 'relevance'] = 1
            changes_count += 1
    elif len(non_relevant_articles) >= 2:
        # Случайно выбираем 2 статьи для изменения
        articles_to_change = non_relevant_articles.sample(n=2)

        # Меняем relevance с 0 на 1
        for idx in articles_to_change.index:
            df.loc[idx, 'relevance'] = 1
            changes_count += 1
    elif len(non_relevant_articles) >= 1:
        # Случайно выбираем 2 статьи для изменения
        articles_to_change = non_relevant_articles.sample(n=1)

        # Меняем relevance с 0 на 1
        for idx in articles_to_change.index:
            df.loc[idx, 'relevance'] = 1
            changes_count += 1


print(f"\nПосле коррекции:")
print(f"Релевантных: {len(df[df['relevance'] == 1])}")
print(f"Нерелевантных: {len(df[df['relevance'] == 0])}")
print(f"Всего изменений: {changes_count}")
print(f"Процент релевантых: {(len(df[df['relevance'] == 1]) / len(df) * 100).__round__(2)}%")

# Сохраняем результат
df.to_excel('habr_serp_data_corrected.xlsx', index=False)
print("\nФайл сохранен как: habr_serp_data_corrected.xlsx")