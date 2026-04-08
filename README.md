# NeoStore

# 1. Клонировать репозиторий
git clone https://github.com/w0nkest/neostore.git
cd neostore

# 2. Создать виртуальное окружение
python -m venv .venv

# 3. Активировать виртуальное окружение
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Установить зависимости
pip install -r requirements.txt

# 5. Создать миграции и базу данных
python neostore/manage.py migrate

# 6. Создать суперпользователя (опционально)
python neostore/manage.py createsuperuser

# 7. Запустить сервер
python neostore/manage.py runserver
