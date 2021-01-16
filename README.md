# fabrique-poll-api
Тестовове задание для Fabrique
API на базе django и django-rest-framework для проведения опросов
## Запуск сервиса 
Клонировать проект:  
```git clone https://github.com/Dukastlik/fabrique-poll-api```  
Перейти в директорию fabrique-poll-api:  
```cd fabrique-poll-api```
Собрать образ с помощью:
```docker-compose build```
Применить миграции:
```docker-compose run apiserver /app/manage.py migrate```
Создать суперюзера:
```docker-compose run apiserver /app/manage.py createsuperuser --username admin --email admin@example.com```
Запустить сервис:
```docker-compose up```

## Интерфейс
Методы сервиса доступны по http://localhost:8080/api/

Интерфейс администратора:
1.Просмотр всех опросы по `GET` на http://localhost:8080/api/polls
2.Добавление нового опроса по `POST` на http://localhost:8080/api/polls/ с json вида:
```
{"poll":
        {
        "title":"<poll_title>",
        "pub_date":"<publication_date>",
        "expire_date":"<expire_date>"
        }
}
```
3.Редактирование опроса по `POST` на http://localhost:8080/api/polls с указанием названия опроса, который необходимо обновить (json схема как у `GET`).
4. Просмотр вопросов конкретного опроса по `GET` на http://localhost:8080/api/polls/{poll_id}/questions/
4. Добавление нового вопроса к опросу по `POST` на http://localhost:8080/api/polls/{poll_id}/questions/ c json вида:
```
{"question":
        {
        "question_type":<question_type>,
        "question_text":<question_text>
        }
}
```
5.Редактирование вопроса по `POST` на http://localhost:8080/api/polls/{poll_id}/questions/ с указанием названия вопроса, который необходимо обновить (json схема как у `GET`).

Для аутентификации администратор отправляет username ('admin') password (тот который был задан при createsuperuser) с каждым запросом (для этого, как и для отправки други запросов можно использовать Postman или curl).

Интерфейс пользователя:
1. Просмотр актуальных опросов по `GET` на http://localhost:8080/api/polls
2. Прохождение опроса по `POST` на http://localhost:8080/api/polls/{poll_id}/questions/ с json вида:
```
{"answers":
    [
        {
        "question_id":<question_id>,
        "user_id":"<user_id>",
        "choice_text":"<choice_text>"
        },
        {
        "question_id":<question_id>,
        "user_id":"<user_id>",
        "choice_text":"<choice_text>"
        }
    ]
}
```
Пользователь анонимно проходит опросы, чтобы получить user_id отправьте `GET` на http://localhost:8080/api/keygen/

3. Просмотр результатов пройденных пользователем  опросов по `GET` на http://localhost:8080/api/answers/?uid=<user_id>
(user_id передается в качестве параметра таким, каким был указан при прохождении опроса).

