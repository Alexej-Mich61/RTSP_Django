RTSP_Django Project
Это Django-проект для управления потоками RTSP-камер с использованием HLS для воспроизведения видео. Включает аутентификацию пользователей, управление зданиями и камерами, а также базовые функции для создания отчётов.
Структура проекта

cameras/: Приложение для управления зданиями и камерами.
users/: Приложение для аутентификации и управления пользователями.
reports/: Приложение для создания отчётов (в разработке).
stream/: Основные настройки проекта и URL-адреса.
templates/: Базовые шаблоны и шаблоны приложений.
static/: Статические файлы (CSS, JS, изображения).
logs/: Папка для файлов логов (не отслеживается Git).

Требования

Python 3.12 установлен.
PostgreSQL установлен и запущен.
Git установлен.
FFmpeg установлен (для трансляции RTSP в HLS).
Nginx установлен (для предоставления HLS-потоков).
PyCharm (опционально, для Ubuntu).

Инструкции по установке
На Windows

Клонирование репозиторияОткрой терминал (PowerShell или Командная строка) и выполни:
git clone <url-репозитория>
cd RTSP_Django


Создание необходимых файлов и папок

Создай папку logs в корне проекта:mkdir logs


Переименуй .env.example в .env:ren .env.example .env


Открой .env в текстовом редакторе и заполни требуемые значения:SECRET_KEY=ваш-секретный-ключ
DB_NAME=имя-вашей-базы-данных
DB_USER=имя-пользователя-базы
DB_PASSWORD=пароль-пользователя-базы
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000
HLS_HOST=http://127.0.0.1/hls

Сгенерируй SECRET_KEY с помощью безопасного генератора (например, Python-скрипт: python -c "import secrets; print(secrets.token_hex(32))").


Настройка виртуального окружения

Создай виртуальное окружение:python -m venv .venv


Активируй виртуальное окружение:.venv\Scripts\activate




Установка зависимостейУстанови необходимые Python-пакеты:
pip install -r requirements.txt


Настройка базы данных

Убедись, что PostgreSQL запущен и создана база данных с именем, указанным в .env.
Примени миграции:python manage.py migrate




Сбор статических файловСобери статические файлы для продакшена (опционально для разработки):
python manage.py collectstatic --noinput


Запуск локального сервераЗапусти сервер разработки Django:
python manage.py runserver

Открой приложение по адресу http://127.0.0.1:8000.

Настройка FFmpeg и Nginx для HLS-трансляции

Убедись, что FFmpeg и Nginx установлены.
Создай папку для HLS-потоков:mkdir C:\nginx\www\hls


Настрой Nginx для предоставления HLS-потоков (пример nginx.conf):http {
    server {
        listen 80;
        server_name localhost;

        location /hls {
            root C:/nginx/www;
            types {
                application/vnd.apple.mpegurl m3u8;
                video/mp2t ts;
            }
            add_header Cache-Control no-cache;
        }
    }
}


Запусти Nginx:nginx


Запусти FFmpeg для каждой камеры (пример для camera_1):ffmpeg -i rtsp://ваш-rtsp-url -c:v copy -c:a aac -f hls -hls_time 10 -hls_list_size 5 C:\nginx\www\hls\camera_1\stream.m3u8

Замени rtsp://ваш-rtsp-url на реальный RTSP-URL вашей камеры.



На Ubuntu

Клонирование репозиторияОткрой терминал и выполни:
git clone <url-репозитория>
cd RTSP_Django


Создание необходимых файлов и папок

Создай папку logs в корне проекта:mkdir logs


Переименуй .env.example в .env:mv .env.example .env


Открой .env в текстовом редакторе (например, nano .env) и заполни требуемые значения:SECRET_KEY=ваш-секретный-ключ
DB_NAME=имя-вашей-базы-данных
DB_USER=имя-пользователя-базы
DB_PASSWORD=пароль-пользователя-базы
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000
HLS_HOST=http://127.0.0.1/hls

Сгенерируй SECRET_KEY с помощью безопасного генератора (например, Python-скрипт: python3 -c "import secrets; print(secrets.token_hex(32))").


Настройка виртуального окружения

Создай виртуальное окружение:python3 -m venv .venv


Активируй виртуальное окружение:source .venv/bin/activate




Установка зависимостейУстанови необходимые Python-пакеты:
pip install -r requirements.txt


Настройка базы данных

Установи и запусти PostgreSQL:sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start


Создай базу данных с именем, указанным в .env:sudo -u postgres createdb имя-вашей-базы-данных


Примени миграции:python manage.py migrate




Сбор статических файловСобери статические файлы для продакшена (опционально для разработки):
python manage.py collectstatic --noinput


Запуск локального сервераЗапусти сервер разработки Django:
python manage.py runserver

Открой приложение по адресу http://127.0.0.1:8000.

Настройка FFmpeg и Nginx для HLS-трансляции

Установи FFmpeg и Nginx:sudo apt update
sudo apt install ffmpeg nginx


Создай папку для HLS-потоков:sudo mkdir -p /usr/share/nginx/www/hls
sudo chown -R $(whoami):$(whoami) /usr/share/nginx/www


Настрой Nginx для предоставления HLS-потоков (редактируй /etc/nginx/sites-available/default):server {
    listen 80;
    server_name localhost;

    location /hls {
        root /usr/share/nginx/www;
        types {
            application/vnd.apple.mpegurl m3u8;
            video/mp2t ts;
        }
        add_header Cache-Control no-cache;
    }
}


Перезапусти Nginx:sudo systemctl restart nginx


Запусти FFmpeg для каждой камеры (пример для camera_1):ffmpeg -i rtsp://ваш-rtsp-url -c:v copy -c:a aac -f hls -hls_time 10 -hls_list_size 5 /usr/share/nginx/www/hls/camera_1/stream.m3u8

Замени rtsp://ваш-rtsp-url на реальный RTSP-URL вашей камеры.



Обновление проекта
На Windows

Перейди в директорию проекта:
cd C:\PYTHON PROJECT\RTSP_Django


Выполни git pull для получения последних изменений:
git pull origin main


Активируй виртуальное окружение:
.venv\Scripts\activate


Обнови зависимости, если requirements.txt изменился:
pip install -r requirements.txt


Примени новые миграции базы данных:
python manage.py migrate


Собери статические файлы, если они изменились:
python manage.py collectstatic --noinput


Перезапусти сервер разработки:
python manage.py runserver



На Ubuntu (с PyCharm)

Открой проект в PyCharm:

Запусти PyCharm и открой директорию RTSP_Django.


Выполни git pull через PyCharm:

Перейди в VCS > Git > Pull в меню.
Выбери ветку main и нажми Pull.

Или используй терминал в PyCharm:

Открой терминал (в нижней панели PyCharm) и выполни:git pull origin main




Активируй виртуальное окружение в терминале PyCharm:
source .venv/bin/activate


Обнови зависимости, если requirements.txt изменился:
pip install -r requirements.txt


Примени новые миграции базы данных:
python manage.py migrate


Собери статические файлы, если они изменились:
python manage.py collectstatic --noinput


Запусти сервер разработки через PyCharm:

Создай конфигурацию для сервера Django (если ещё не настроена):
Перейди в Run > Edit Configurations.
Добавь новую конфигурацию Django server.
Укажи путь к manage.py и оставь хост/порт по умолчанию (127.0.0.1:8000).


Нажми кнопку Run для запуска сервера.



Дополнительные заметки

Убедись, что FFmpeg и Nginx запущены для работы HLS-трансляции.
Создай администратора для доступа к админ-панели:python manage.py createsuperuser


Проект использует django-admin-autocomplete-filter, который требует правильной конфигурации INSTALLED_APPS (уже настроено в settings.py).

Дата последнего обновления: 03.06.2025, 17:56 (CEST).
