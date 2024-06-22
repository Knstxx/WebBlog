# WebBlog
О проекте:
1. WebBlog - социальная сеть.
2. Над проектом работали:
<a href="https://github.com/Knstxx" target="_blank">Konstantin Khotnog</a>

Сайт-блог для публикации собственных постов с медиа и возможностью комментирования чужих работ. Реализован на Django. Настроена регистрация пользователей, есть система восстановления через e-mail. Полностью прописан бэкенд для HTML, CSS и JavaScript шаблонов.

Tech.Stack: Python, Django, HTML, CSS
# Как запустить проект:

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
