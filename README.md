веб-гис приложения, созданное для мониторинга данных о достопримечательностях якутии



установка:
git clone https://github.com/Mxm2000777/travel_wonders/ #копирование репозитория в ваш локальный диск
python -m venv myvenv #создание виртуального окружения пайтон
myvenv/Scripts/Activate
pip install requements.txt #быстрая установка всех зависимостей для проекта
uvicorn main:app --reload #запуск ASGI сервера для fastapi+flet монстрика
