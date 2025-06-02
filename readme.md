RTSP_Django
Проект RTSP_Django — это веб-приложение на Django для управления RTSP-стримами камер, связанными со зданиями. Приложение использует Nginx для генерации HLS-потоков и позволяет просматривать видеопотоки, управлять зданиями, камерами, пользователями и их разрешениями через админ-панель.
Требования

Python 3.12+
Git
Nginx (для генерации HLS-потоков)
PostgreSQL (рекомендуется, если настроено в settings.py) или SQLite (по умолчанию)
ОС: Windows, macOS или Linux

Установка и развертывание
1. Клонирование репозитория
Склонируй проект с GitHub:
git clone https://github.com/<your-username>/RTSP_Django.git
cd RTSP_Django

Замени <your-username> на твой GitHub-username.
2. Создание виртуального окружения
Создай и активируй виртуальное окружение:
Windows
python -m venv .venv
.\.venv\Scripts\activate

macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

3. Установка зависимостей
Установи зависимости из requirements.txt:
pip install -r requirements.txt

На Ubuntu:
pip3 install -r requirements.txt

Если requirements.txt отсутствует, установи вручную:
pip install asgiref==3.8.1 Django==5.2 django-admin-autocomplete-filter==0.7.1 psycopg2==2.9.10 sqlparse==0.5.3 tzdata==2025.2 argon2-cffi==23.1.0 python-dotenv==1.0.1

4. Настройка переменных окружения
Переименуй файл .env.example в .env в корне проекта и добавь свои реальные значения для переменных:
# Секретный ключ Django
SECRET_KEY=your-secret-key

# Настройки базы данных
DB_NAME=rtsp_django
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
# Список разрешённых хостов (через запятую)
ALLOWED_HOSTS=localhost,127.0.0.1
# Список доверенных источников CSRF (через запятую)
CSRF_TRUSTED_ORIGINS=...(или убери это)
# Хост для HLS-потоков
HLS_HOST=http://localhost/hls

Для продакшен-среды укажи правильный HLS_HOST, 
соответствующий твоему серверу (например, http://video.ru/hls).

5. Настройка Nginx (для HLS)

Установи Nginx:
Windows: Скачай с официального сайта.
macOS: brew install nginx
Ubuntu: sudo apt update && sudo apt install nginx


Настрой конфигурацию Nginx для RTSP → HLS (пример конфига см. в документации Nginx или модуля nginx-rtmp-module).
Убедись, что RTSP-потоки доступны через .m3u8 файлы.

6. Настройка базы данных
SQLite (по умолчанию)
Если используешь SQLite, дополнительных настроек не требуется. Файл базы данных (db.sqlite3) создастся автоматически.
PostgreSQL (если настроено)

Установи PostgreSQL:
Windows: Скачай с официального сайта.
macOS: brew install postgresql
Ubuntu: sudo apt install postgresql postgresql-contrib


Создай базу данных:psql -U postgres
CREATE DATABASE rtsp_django;
\q


Укажи настройки базы данных в .env (см. шаг 4).

7. Применение миграций
Создай и примени миграции для настройки базы данных:
python manage.py makemigrations
python manage.py migrate

8. Создание суперпользователя
Создай суперпользователя для доступа к админ-панели:
python manage.py createsuperuser

Следуй инструкциям, чтобы задать имя, email и пароль.
9. Сбор статических файлов
Настройка статических файлов
Убедись, что фавикон находится по пути static/images/favicon/favicon.ico. 
Собери статические файлы для продакшена:

python manage.py collectstatic

Ответь "yes", если будет запрос на перезапись.
Собери статические файлы (например, CSS, JS):
python manage.py collectstatic

Ответь "yes", если будет запрос на перезапись.
10. Запуск сервера
Запусти сервер разработки:
python manage.py runserver

Открой в браузере: http://127.0.0.1:8000/.
11. Доступ к админ-панели
Перейди: http://127.0.0.1:8000/admin/. Войди с логином и паролем суперпользователя.
Дополнительные шаги
Добавление данных

Через админку добавь здания (/admin/cameras/building/), камеры (/admin/cameras/camera/) и пользователей с разрешениями.
Укажи пути к .m3u8 файлам, сгенерированным Nginx, в настройках камер.

Тестирование стримов

Убедись, что RTSP-потоки настроены в Nginx и доступны через .m3u8 (проверь через VLC или браузер).
На странице здания (/cameras/buildings/<id>/) видеопотоки должны отображаться.

Устранение неполадок

Ошибка ModuleNotFoundError: No module named 'django':Убедись, что виртуальное окружение активировано, и Django установлен (pip install django).
HLS не работает:Проверь конфигурацию Nginx и доступность .m3u8 файлов.
Ошибка базы данных:Проверь настройки в .env и убедись, что PostgreSQL запущен.

Контакты
Если возникнут вопросы, создай issue в репозитории или свяжись с разработчиком через GitHub.
