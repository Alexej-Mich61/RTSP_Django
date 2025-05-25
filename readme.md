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

Если requirements.txt отсутствует, установи вручную:

pip install asgiref==3.8.1 Django==5.2 django-admin-autocomplete-filter==0.7.1 psycopg2==2.9.10 sqlparse==0.5.3 tzdata==2025.2

4. Настройка Nginx (для HLS)





Установи Nginx:





Windows: Скачай с официального сайта.



macOS: brew install nginx



Ubuntu: sudo apt update && sudo apt install nginx



Настрой конфигурацию Nginx для RTSP → HLS (пример конфига см. в документации Nginx или модуля nginx-rtmp-module).



Убедись, что RTSP-потоки доступны через .m3u8 файлы.

5. Настройка базы данных

SQLite (по умолчанию)

Если используешь SQLite, дополнительных настроек не требуется. Файл базы данных (db.sqlite3) создастся автоматически.

PostgreSQL (если настроено)





Установи PostgreSQL:





Windows: Скачай с официального сайта.



macOS: brew install postgresql



Ubuntu: sudo apt install postgresql postgresql-contrib



Создай базу данных:

psql -U postgres
CREATE DATABASE rtsp_django;
\q



Настрой DATABASES в stream/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rtsp_django',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

6. Применение миграций

Создай и примени миграции для настройки базы данных:

python manage.py makemigrations
python manage.py migrate

7. Создание суперпользователя

Создай суперпользователя для доступа к админ-панели:

python manage.py createsuperuser

Следуй инструкциям, чтобы задать имя, email и пароль.

8. Сбор статических файлов

Собери статические файлы (например, CSS, JS):

python manage.py collectstatic

Ответь "yes", если будет запрос на перезапись.

9. Запуск сервера

Запусти сервер разработки:

python manage.py runserver

Открой в браузере: http://127.0.0.1:8000/.

10. Доступ к админ-панели

Перейди: http://127.0.0.1:8000/admin/. Войди с логином и паролем суперпользователя.

Дополнительные шаги

Добавление данных





Через админку добавь здания (/admin/cameras/building/), камеры (/admin/cameras/camera/) и пользователей с разрешениями.



Укажи пути к .m3u8 файлам, сгенерированным Nginx, в настройках камер.

Тестирование стримов





Убедись, что RTSP-потоки настроены в Nginx и доступны через .m3u8 (проверь через VLC или браузер).



На странице здания (/cameras/buildings/<id>/) видеопотоки должны отображаться.

Устранение неполадок





Ошибка ModuleNotFoundError: No module named 'django': Убедись, что виртуальное окружение активировано, и Django установлен (pip install django).



HLS не работает: Проверь конфигурацию Nginx и доступность .m3u8 файлов.



Ошибка базы данных: Проверь настройки DATABASES в stream/settings.py.

Контакты

Если возникнут вопросы, создай issue в репозитории или свяжись с разработчиком через GitHub.