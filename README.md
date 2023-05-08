<img src="https://github.com/milmax75/foodgram-project-react/actions/workflows/main.yml/badge.svg" height="90"/>

# praktikum_new_diplom

Дипломный работой является написание бэк-энда ресурса, позполяющего созавать рецепты, добавлять их в избранное, подписываться на авторов рецептов, добавлять картинки и нгредиенты, добавлять рецепты в корзину и на ее основании формировать список покупок, агрегирующий все ингредиенты из рецептов.

# автор
Миленин Максим

### Установка.
##### Как развернуть проект на локальной машине

**Клонировать репозиторий и перейти в него в командной строке:**
Скопируйте SSH Code
> git clone * *вставьте SSH Code* *
> cd api_yamdb

Cоздать и активировать виртуальное окружение:
> python -m venv venv
> source venv/Scripts/activate

Установить зависимости из файла requirements.txt:
> python -m pip install --upgrade pip
> pip install -r requirements.txt

Выполнить миграции:
> python manage.py migrate

Запустить проект:
> python manage.py runserver

Если есть необходимость, заполнить базу тестовыми данными:
>python manage.py dataimport

### Вход в панель админинстрирования.
##### Адрес.
http://62.84.118.104/admin/

### Примеры.
##### Некоторые примеры запросов к API.

GET /api/users/
список всех пользователей

POST /api/users/
создание пользователя

GET /api/users/{id}/
данные о пользователе

GET /api/users/me/
текущий пользователь

POST /api/users/set_password/
установить пароль
 
POST /api/auth/token/login/
Получить токен авторизации

POST /api/auth/token/logout/
Удаление токена

POST /api/tags/
Cписок тегов

POST /api/tags/{id}/
Получение тега

GET /api/recipes/
Список рецептов

POST /api/recipes/
Создание рецепта

GET /api/recipes/{id}/
Получение рецепта

POST /api/recipes/{id}/
Обновление рецепта

DEL /api/recipes/{id}/
Удаление рецепта

GET /api/recipes/download_shopping_cart/
Скачать список покупок

POST /api/recipes/{id}/shopping_cart/
Добавить рецепт в список покупок

DEL /api/recipes/{id}/shopping_cart/
Удалить рецепт из списка покупок

POST /api/recipes/{id}/favorite/
Добавить рецепт в избранное

DEL /api/recipes/{id}/favorite/
Удалить рецепт из избранного

GET /api/users/subscriptions/
Мои подписки

POST /api/users/{id}/subscribe/
Подписаться на пользователя

DEL /api/users/{id}/subscribe/
Отписаться от пользователя

GET /api/ingredients/
Список ингредиентов

GET /api/ingredients/{id}/
Получение ингредиента




