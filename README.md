веб-гис приложения, созданное для мониторинга данных о достопримечательностях якутии

стек технологий:
ЯП: python
фронт: html, css, bootstrap, leavetjs, JINJA2(для удобной шаблонизации html файлов), flet
бэк: postgresql(удобная реляционная СУБД, по идее можно было postgis установить), fastAPI(быстрейший бэк для пайтона)

сторонние библы для ЯП:
flet - быстрая верстка с использованием flutter sdk
osmnx - графы на карте
networkx - библа для работы с графами(поиск кратчайщего маршрута)
uvicorn - мощный ASGI сервер для fastAPI
fiona - гео векторные данные
folium - карты, маркера, графы

установка:
git clone https://github.com/Mxm2000777/travel_wonders/ #копирование репозитория в ваш локальный диск
python -m venv myvenv #создание виртуального окружения пайтон
myvenv/Scripts/Activate
pip install requements.txt #быстрая установка всех зависимостей для проекта
uvicorn main:app --reload #запуск ASGI сервера для fastapi+flet монстрика

я не успел
