import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import re

def prepare_data(df):
    """Подготовка данных для обучения"""

    # Очистка текстовых полей
    df['title_clean'] = df['title'].fillna('').astype(str)
    df['tags_clean'] = df['tags'].fillna('').astype(str)
    df['hubs_clean'] = df['hubs'].fillna('').astype(str)

    # Создаем комбинированные признаки
    df['combined_features'] = (
            df['title_clean'] + ' ' +
            df['tags_clean'] + ' ' +
            df['hubs_clean']
    )

    # Извлекаем числовые признаки
    df['title_length'] = df['title_clean'].str.len()
    df['tags_count'] = df['tags_clean'].str.count(',') + 1

    return df


def train_logistic_regression(df):
    """Обучаем модель логистической регрессии"""

    print("🎯 ОБУЧЕНИЕ ЛОГИСТИЧЕСКОЙ РЕГРЕССИИ")
    print("=" * 50)

    # Подготовка данных
    df = prepare_data(df)

    # Разделяем на признаки и целевую переменную
    X = df['combined_features']
    y = df['relevance']

    # Разделяем на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Создаем пайплайн: векторизация + классификация
    model = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=1000,
            stop_words=['теги', 'tags', 'hubs', 'blog', 'блог'],
            min_df=2,
            ngram_range=(1, 2)  # учитываем отдельные слова и пары слов
        )),
        ('classifier', LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight='balanced'  # балансируем классы (1 и 0)
        ))
    ])

    # Обучаем модель
    print("📚 Обучаем модель на размеченных данных...")
    model.fit(X_train, y_train)

    # Оцениваем качество
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"✅ Точность модели: {accuracy:.3f}")
    print("\n📊 Отчет по классификации:")
    print(classification_report(y_test, y_pred))

    return model, X_train, X_test, y_train, y_test


def analyze_feature_importance(model, feature_names, top_n=20):
    """Анализ важности признаков"""

    print(f"\n🔍 ТОП-{top_n} ВАЖНЫХ ПРИЗНАКОВ:")
    print("=" * 50)

    # Получаем коэффициенты модели
    coefficients = model.named_steps['classifier'].coef_[0]
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': coefficients
    })

    # Сортируем по важности (по модулю)
    feature_importance['abs_importance'] = np.abs(feature_importance['importance'])
    top_features = feature_importance.sort_values('abs_importance', ascending=False).head(top_n)

    for _, row in top_features.iterrows():
        effect = "УВЕЛИЧИВАЕТ" if row['importance'] > 0 else "УМЕНЬШАЕТ"
        print(f"{row['feature']:<30} {effect} вероятность релевантности (вес: {row['importance']:.3f})")


def predict_new_articles(model, new_articles_df):
    """Предсказание для новых статей"""

    print("\n🎯 ПРЕДСКАЗАНИЕ ДЛЯ НОВЫХ СТАТЕЙ")
    print("=" * 50)

    # Подготавливаем новые данные
    new_df = prepare_data(new_articles_df)

    # Предсказываем вероятности
    probabilities = model.predict_proba(new_df['combined_features'])[:, 1]
    new_df['predicted_relevance'] = model.predict(new_df['combined_features'])
    new_df['relevance_probability'] = probabilities

    # Сортируем по вероятности релевантности
    sorted_df = new_df.sort_values('relevance_probability', ascending=False)

    print("Топ-5 самых релевантных статей:")
    for i, (idx, row) in enumerate(sorted_df.head().iterrows(), 1):
        print(f"{i}. {row['title'][:60]}... (вероятность: {row['relevance_probability']:.3f})")

    return new_df


def main():
    # Загружаем данные
    df = pd.read_excel("habr_serp_data_llm_with_relevance.xlsx")

    # Проверяем, что есть размеченные данные
    if 'relevance' not in df.columns or df['relevance'].isna().all():
        print("❌ Нет размеченных данных в колонке 'relevance'")
        return

    print(f"📊 Всего статей: {len(df)}")
    print(f"🔸 Релевантных: {len(df[df['relevance'] == 1])}")
    print(f"🔹 Нерелевантных: {len(df[df['relevance'] == 0])}")

    # Обучаем модель
    model, X_train, X_test, y_train, y_test = train_logistic_regression(df)

    # Анализируем важные признаки
    feature_names = model.named_steps['tfidf'].get_feature_names_out()
    analyze_feature_importance(model, feature_names)

    # Демонстрация предсказания на тестовых данных
    print(f"\n🎪 ДЕМОНСТРАЦИЯ РАБОТЫ МОДЕЛИ:")
    print("=" * 50)

    test_predictions = model.predict(X_test)
    test_probs = model.predict_proba(X_test)[:, 1]

    # Показываем несколько примеров
    for i in range(min(5, len(X_test))):
        actual = y_test.iloc[i]
        predicted = test_predictions[i]
        prob = test_probs[i]

        print(f"\nСтатья: {X_test.iloc[i][:80]}...")
        print(f"Фактическая релевантность: {actual}, Предсказанная: {predicted}")
        print(f"Вероятность релевантности: {prob:.3f}")
        print("✅ Верно" if actual == predicted else "❌ Ошибка")

    # Сохраняем модель для будущего использования
    import joblib
    joblib.dump(model, 'relevance_classifier.pkl')
    print(f"\n💾 Модель сохранена в 'relevance_classifier.pkl'")


if __name__ == "__main__":
    main()