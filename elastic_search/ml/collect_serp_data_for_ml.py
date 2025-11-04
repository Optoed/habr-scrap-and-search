from elastic_search.collect_serp_data import SERPCollector

programming_queries = [
    "python разработка", "python для начинающих", "python машинное обучение", "python веб разработка",
    "python асинхронное программирование", "python django tutorial", "python flask fastapi",
    "python pandas анализ данных", "python numpy массивы", "python matplotlib визуализация",
    "python scikit-learn ml", "python парсинг данных", "python телеграм бот", "python selenium автоматизация",
    "python оптимизация кода", "python декораторы", "python генераторы", "python многопоточность",
    "python asyncio примеры", "python тестирование pytest", "python базы данных", "python sqlalchemy",
    "python docker контейнеризация", "python микросервисы", "python rest api",

    "javascript программирование", "javascript для начинающих", "javascript es6 features",
    "javascript асинхронность", "javascript promises", "javascript async await",
    "javascript dom manipulation", "javascript фронтенд", "javascript react vue",
    "javascript node.js сервер", "javascript typescript", "javascript фреймворки 2024",
    "javascript оптимизация", "javascript webpack", "javascript npm пакеты",

    "java разработка", "java spring framework", "java микросервисы", "java maven gradle",
    "java многопоточность", "java коллекции", "java stream api", "java junit тестирование",
    "java hibernate orm", "java docker", "java performance", "java best practices",

    "golang программирование", "golang для начинающих", "golang goroutines", "golang web сервер",
    "golang микросервисы", "golang производительность", "golang тестирование", "golang gin framework",

    "rust системное программирование", "rust ownership", "rust безопасность", "rust webassembly",
    "rust производительность", "rust для начинающих",

    "c++ разработка", "c++ stl", "c++ многопоточность", "c++ оптимизация", "c++ qt",
    "c++ game development", "c++ templates", "c++ modern features",

    "c# .net разработка", "c# asp.net core", "c# entity framework", "c# wpf", "c# unity",
    "c# многопоточность", "c# linq",

    "php программирование", "php laravel", "php symfony", "php wordpress", "php performance",

    "kotlin android разработка", "kotlin coroutines", "kotlin multiplatform",

    "swift ios разработка", "swiftui tutorial", "swift async await",

    "typescript angular", "typescript react", "typescript best practices",

    "scala functional programming", "scala akka",

    "haskell функциональное программирование", "haskell для начинающих",

    "elixir phoenix framework", "elixir otp",

    "dart flutter", "dart mobile development",

    "r язык для анализа данных", "r статистика", "r визуализация",

    "sql запросы", "sql оптимизация", "sql индексы", "sql joins", "sql window functions",
    "postgresql настройка", "mysql производительность", "mongodb агрегации",
    "redis кэширование", "elasticsearch поиск", "clickhouse аналитика"
]

frameworks_queries = [
    "react разработка", "react hooks", "react state management", "react next.js",
    "react typescript", "react testing library", "react performance", "react native",
    "react router", "react context api", "react redux", "react mobx",

    "vue.js разработка", "vue composition api", "vue pinia", "vue nuxt.js",
    "vue router", "vue тестирование", "vue 3 features",

    "angular разработка", "angular components", "angular rxjs", "angular forms",
    "angular routing", "angular testing", "angular performance",

    "django framework", "django rest framework", "django orm", "django deployment",
    "django celery", "django channels", "django testing",

    "flask python", "flask rest api", "flask sqlalchemy", "flask deployment",

    "fastapi python", "fastapi async", "fastapi pydantic", "fastapi документация",

    "spring boot java", "spring security", "spring data jpa", "spring cloud",
    "spring mvc", "spring testing",

    "laravel php", "laravel eloquent", "laravel artisan", "laravel deployment",

    "express node.js", "express middleware", "express mongodb", "express authentication",

    "nestjs typescript", "nestjs microservices", "nestjs swagger",

    "next.js react", "next.js ssr", "next.js api routes", "next.js deployment",

    "nuxt.js vue", "nuxt.js ssr", "nuxt.js modules",

    "svelte разработка", "svelte kit", "svelte stores",

    "flutter dart", "flutter widgets", "flutter state management", "flutter animation",
    "flutter firebase", "flutter testing",

    "tensorflow machine learning", "tensorflow keras", "tensorflow neural networks",
    "tensorflow deployment", "tensorflow lite",

    "pytorch deep learning", "pytorch transformers", "pytorch computer vision",
    "pytorch nlp", "pytorch gpu",

    "keras neural networks", "keras tutorial", "keras cnn", "keras rnn",

    "pandas анализ данных", "pandas dataframe", "pandas группировка", "pandas временные ряды",

    "numpy массивы", "numpy операции", "numpy линейная алгебра", "numpy производительность",

    "apache spark big data", "spark streaming", "spark ml", "spark performance",

    "apache kafka messaging", "kafka streams", "kafka connect", "kafka deployment",

    "grafana мониторинг", "grafana дашборды", "grafana alerts", "grafana prometheus",

    "prometheus метрики", "prometheus queries", "prometheus alertmanager",

    "jenkins ci/cd", "jenkins pipeline", "jenkins docker", "jenkins groovy",

    "gitlab ci/cd", "gitlab runners", "gitlab docker", "gitlab automation",

    "github actions", "github workflows", "github deployment", "github automation"
]

devops_queries = [
    "docker контейнеризация", "docker compose", "docker swarm", "docker kubernetes",
    "docker best practices", "docker security", "docker multi-stage build",
    "docker volumes", "docker networking", "docker monitoring",

    "kubernetes orchestration", "kubernetes pods", "kubernetes services",
    "kubernetes deployment", "kubernetes helm", "kubernetes monitoring",
    "kubernetes security", "kubernetes autoscaling", "kubernetes operators",

    "aws облачные сервисы", "aws ec2", "aws s3", "aws lambda", "aws rds",
    "aws vpc", "aws iam", "aws cloudformation", "aws eks", "aws cost optimization",

    "azure cloud", "azure vm", "azure functions", "azure kubernetes",
    "azure devops", "azure monitoring", "azure security",

    "gcp google cloud", "gcp compute engine", "gcp cloud functions", "gcp gke",
    "gcp bigquery", "gcp monitoring", "gcp security",

    "terraform infrastructure", "terraform modules", "terraform state",
    "terraform aws", "terraform best practices", "terraform automation",

    "ansible automation", "ansible playbooks", "ansible roles", "ansible docker",
    "ansible best practices", "ansible troubleshooting",

    "ci/cd pipeline", "ci/cd best practices", "ci/cd testing", "ci/cd security",
    "ci/cd deployment strategies", "ci/cd monitoring",

    "мониторинг приложений", "мониторинг производительности", "лог анализ",
    "apm инструменты", "метрики приложений", "alerting система",

    "безопасность приложений", "owasp top 10", "web security", "api security",
    "контейнерная безопасность", "kubernetes security", "devsecops",

    "highload архитектура", "масштабирование приложений", "load balancing",
    "caching стратегии", "cdn настройка", "database scaling",

    "микросервисы архитектура", "microservices patterns", "service discovery",
    "api gateway", "event driven architecture", "message brokers",

    "serverless архитектура", "aws lambda", "azure functions", "google cloud functions",
    "serverless limitations", "serverless best practices",

    "базы данных производительность", "sql оптимизация", "nosql выбор",
    "database indexing", "query optimization", "database replication",

    "nginx настройка", "nginx reverse proxy", "nginx load balancing",
    "nginx caching", "nginx security", "nginx performance",

    "apache настройка", "apache virtual hosts", "apache mod_rewrite",
    "apache performance", "apache security"
]

datascience_queries = [
    "машинное обучение", "ml алгоритмы", "обучение с учителем", "обучение без учителя",
    "классификация ml", "регрессия модели", "кластеризация данных", "аномалия detection",

    "нейросети глубокое обучение", "cnn сверточные сети", "rnn рекуррентные сети",
    "transformer архитектура", "attention механизм", "gan генеративные сети",

    "обработка естественного языка", "nlp тексты", "токенизация текст", "word embeddings",
    "sentiment анализ", "named entity recognition", "text classification",

    "компьютерное зрение", "cv opencv", "объекты detection", "image segmentation",
    "facial recognition", "image processing", "computer vision tensorflow",

    "рекомендательные системы", "collaborative filtering", "content based filtering",
    "recommendation algorithms", "matrix factorization",

    "анализ данных", "data preprocessing", "feature engineering", "data cleaning",
    "exploratory data analysis", "data visualization",

    "big data обработка", "hadoop ecosystem", "spark analytics", "data lakes",
    "data warehouse", "etl процессы",

    "data mining", "pattern recognition", "association rules", "frequent itemsets",

    "статистика анализ", "вероятность распределения", "гипотезы testing",
    "a/b testing", "statistical significance",

    "временные ряды", "time series analysis", "forecasting модели", "arima модели",
    "seasonal decomposition",

    "feature selection", "dimensionality reduction", "pca анализ", "feature importance",

    "mlops практики", "model deployment", "model monitoring", "model retraining",
    "ml pipelines", "experiment tracking",

    "automl автоматическое ml", "hyperparameter tuning", "neural architecture search",

    "transfer learning", "pre-trained models", "fine-tuning моделей",

    "reinforcement learning", "q-learning", "deep q networks", "policy gradients",

    "graph neural networks", "graph analysis", "social network analysis",

    "anomaly detection", "fraud detection", "outlier detection",

    "time series forecasting", "demand prediction", "sales forecasting",

    "computer vision applications", "object detection yolo", "image classification resnet",

    "nlp applications", "text generation gpt", "chatbots nlp", "machine translation",

    "data visualization", "plotly dash", "tableau альтернативы", "interactive dashboards",

    "feature stores", "data versioning", "model registry"
]

web_mobile_queries = [
    "веб разработка", "frontend development", "backend development", "fullstack разработка",
    "responsive design", "mobile first", "cross browser compatibility",

    "html5 features", "css3 анимации", "flexbox layout", "css grid", "sass scss",
    "bootstrap framework", "tailwind css", "css methodologies",

    "javascript frameworks", "single page applications", "progressive web apps",
    "web components", "shadow dom", "custom elements",

    "web performance", "page speed optimization", "core web vitals", "lazy loading",
    "code splitting", "bundle optimization",

    "web security", "xss protection", "csrf tokens", "content security policy",
    "https настройка", "ssl certificates",

    "api design", "rest api best practices", "graphql api", "api versioning",
    "api documentation", "openapi specification",

    "authentication authorization", "jwt tokens", "oauth2 flow", "openid connect",
    "session management", "password security",

    "web sockets", "real-time applications", "socket.io", "websocket security",

    "pwa progressive web apps", "service workers", "web app manifest", "offline functionality",

    "seo оптимизация", "meta tags", "structured data", "page ranking",
    "google search console", "technical seo",

    "accessibility веб", "wcag guidelines", "screen readers", "aria attributes",

    "mobile разработка", "android development", "ios development", "cross platform",
    "react native", "flutter mobile", "xamarin forms",

    "android studio", "kotlin android", "java android", "android jetpack",
    "material design", "android architecture",

    "xcode разработка", "swift ios", "objective-c", "swiftui", "uikit",
    "ios architecture", "app store submission",

    "mobile ui/ux", "mobile patterns", "navigation patterns", "mobile gestures",

    "mobile performance", "battery optimization", "memory management", "mobile testing",

    "mobile security", "data encryption", "secure storage", "biometric authentication",

    "push notifications", "firebase cloud messaging", "apple push notifications",

    "mobile analytics", "user behavior tracking", "crash reporting", "performance monitoring",

    "app distribution", "testflight", "google play console", "enterprise distribution",

    "mobile ci/cd", "fastlane automation", "mobile deployment", "app signing"
]

career_queries = [
    "карьера в it", "it профессии", "программист карьера", "developer roadmap",
    "junior developer", "middle developer", "senior developer", "tech lead",
    "software architect", "team lead", "engineering manager",

    "техническое собеседование", "coding interview", "algorithm questions",
    "system design interview", "behavioral interview", "interview preparation",

    "резюме программиста", "it резюме", "github portfolio", "linkedin профиль",
    "projects for portfolio", "technical skills",

    "удаленная работа", "remote teams", "work from home", "distributed teams",
    "remote collaboration", "time management remote",

    "agile методологии", "scrum framework", "kanban метод", "sprint planning",
    "daily standups", "retrospective meetings",

    "project management", "product management", "technical product manager",
    "requirements gathering", "user stories", "acceptance criteria",

    "team management", "people management", "performance reviews", "one on one meetings",
    "team motivation", "conflict resolution",

    "software development lifecycle", "sdlc phases", "waterfall model", "iterative development",
    "continuous delivery", "release management",

    "code quality", "code review practices", "coding standards", "clean code",
    "refactoring techniques", "technical debt",

    "тестирование программного обеспечения", "unit testing", "integration testing",
    "end-to-end testing", "test automation", "test driven development",

    "документация проектов", "technical documentation", "api documentation",
    "code documentation", "architecture documentation",

    "soft skills разработчика", "коммуникация в it", "presentation skills",
    "technical writing", "mentoring junior developers",

    "it образование", "online courses", "programming bootcamps", "self study",
    "computer science fundamentals", "continuous learning",

    "open source contribution", "github projects", "oss community", "first contribution",

    "технические конференции", "it meetups", "tech talks", "knowledge sharing",

    "work life balance", "burnout prevention", "stress management", "developer health",

    "salary negotiation", "it зарплаты", "compensation packages", "career growth",

    "freelance programming", "contract work", "independent consulting",

    "startup culture", "tech startups", "venture capital", "product development",

    "corporate it", "enterprise development", "legacy systems", "digital transformation"
]

# Объединяем все запросы в один список
all_queries = (programming_queries + frameworks_queries + devops_queries +
               datascience_queries + web_mobile_queries + career_queries)

all_queries_config = [{'query': query, 'type': 'simple'} for query in all_queries]

def main():
    """Основная функция для запуска сбора SERP данных"""
    try:
        print("🔍 Сбор SERP данных для 1000 тестовых запросов")
        print("=" * 60)
        print("Конфигурация запросов:")
        print("  1000 запросов с SIMPLE поиском (минимум 67% слов)")
        print("=" * 60)
        print("Всего будет собрано: 1000 запросов × 10 статей = 10000 статей")
        print("=" * 60)

        # Создаем коллектор
        collector = SERPCollector(False)

        # Собираем данные
        all_serp_data_for_ml = collector.collect_serp_data(
            queries_config=all_queries_config,
            output_json="all_serp_data_for_ml.json",
            output_xlsx="all_serp_data_for_ml.xlsx"
        )

        print("\n🎉 Сбор данных завершен успешно!")
        print("\n📁 Созданные файлы:")
        print("  - all_serp_data_for_ml.json - структурированные данные SERP")
        print("  - all_serp_data_for_ml.xlsx - табличные данные для анализа (Excel)")

        # Дополнительная информация о собранных данных
        if all_serp_data_for_ml:
            total_queries = len(all_serp_data_for_ml)
            total_articles = sum(len(data['results']) for data in all_serp_data_for_ml.values())

            print(f"\n📊 Итоговая статистика:")
            print(f"  Успешно обработано запросов: {total_queries}")
            print(f"  Всего собрано статей: {total_articles}")

    except Exception as e:
        print(f"\n❌ Произошла ошибка при сборе данных: {e}")
        print("Проверьте:")
        print("  - Запущен ли Elasticsearch на localhost:9200")
        print("  - Корректность импорта класса HabrSearchEngine")
        print("  - Наличие индекса 'habr_articles' в Elasticsearch")
        print("  - Установлены ли библиотеки: pandas, openpyxl")


if __name__ == "__main__":
    main()
