# Dementev's foodgram

![Main workflow](https://github.com/Hangman91/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Foodgram - проект сайта, аккумулирующего рецепты, позволяющий искать по ключевым словам, тэгам, вкусам и так далее. 
У Вас будет возможность выбрать понравившиеся рецепты, отложить их в "избранное", а также создать и скачать список покупок. 

Можно затестить по ссылке:
http://51.250.27.161/

### При разработке использованы технологии:
Python 3.7
Django 2.2.19
Django REST framework 3.12.4
Nginx
Docker
Postgres
~~Джин в ночи~~

**Для локальной развертки необходимо будет:**

Скопировать себе на устройство:
```
git clone git@github.com:Hangman91/foodgram-project-react.git
```

Установите Docker. Запустите docker compose:
```
docker-compose up -d --build
```
Создадутся 4 контейнера. 
На данном этапе нас интересует создание контейнера с базой данных и контейнера с фронтэндом для просмотра спецификации.
Спецификация:
```
http://localhost/api/docs/redoc.html#tag/Spisok-pokupok
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r ./backend/foodgram/requirements.txt
```

Выполнить миграции:

```
python ./backend/foodgram/manage.py migrate
```

Создаём супеюзверя
```
python ./backend/foodgram/manage.py createsuperuser
```

Запустить проект:

```
python ./backend/foodgram/manage.py runserver
```



Админка:
```
http://127.0.0.1:8000/admin
```

**Для развертки через докер на сервере:**

1. Готовим сервер:
Останавливаем службу nginx:
```
sudo systemctl stop nginx
```

2. Устанавливаем docker:
```
sudo apt install docker.io 
```

3. Устанавливаем docker-compose:
```
https://docs.docker.com/compose/install/
```

4. Копируем файлы docker-compose.yaml и nginx/default.conf на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/default.conf соответственно.

5. Клонируем проект:
```
git@github.com:Hangman91/foodgram-project-react.git
```

6. Разворачиваем проект: 
```
docker-compose up -d
```

7. Накатываем миграции
```
docker-compose exec web python manage.py migrate
```

7. Создаём суперюзера
```
docker-compose exec web python manage.py createsuperuser
```

8. Собираем статику
```
docker-compose exec web python manage.py collectstatic --no-input 
```

9. Импортируем базу данных
```
docker-compose exec web python manage.py loaddata дамп_бд.json
```


## Немного об авторе:
Александр, 30 лет, Санкт-Петербург.

Защитил  кандидатскую, работаю в Горном университете. 
Занимаюсь приёмом абитуриентов, профориентацией, проведением олимпиад. 
По совместительству преподаватель кафедры Метрологии.

