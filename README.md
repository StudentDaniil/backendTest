# Построение системы для обучения
Реализовал вроде бы все пункты, которые были в тестовом задании, можно запросами получить/изменить/удалить продукты, уроки, группы, баланс, подписки если пользователь админ. Если пользователь не админ, и он не подписан на курс, 
он может просмотреть author, title, price, lessons_count у курса, после подписки ему станут доступны уроки. Баланс создаётся, когда пользователь регистрируется, изменять его может только админ(is_stuff). Группа формируется после подписки на курс первого пользователя,
не до конца понял насчёт **равномерного** распределения по группам. Как мне показалось правильным, это заполнять группу, пока она не станет полной (30 студентов), после создавать новую и заполнять её, я подумал, это логичное решиние.
У курса можно посмотреть количество студентов, заполненность групп и процент приобретения курса(продукта).
Возможно какие-то проблемы с первыми миграциями, поэтому желательно мигрировать поэтапно. 

<details><summary> GET: http://localhost:8000/api/v1/courses/ - показать список всех курсов, если пользователь админ.(is_stuff)</summary>
  200 OK:
  ```
  [
      {
          "id": 2,
          "author": "Павел Путин",
          "title": "Backend",
          "start_date": "2024-08-18T11:49:51.316932Z",
          "price": "1000.00",
          "lessons": [
              {
                  "title": "Урок один python"
              },
              {
                  "title": "Урок один python"
              }
          ],
          "lessons_count": 2,
          "students": [],
          "demand_course_percent": 0,
          "students_count": 0,
          "groups_filled_percent": 0
      },
      {
          "id": 1,
          "author": "Иван иваныч",
          "title": "Игра 2",
          "start_date": "2024-08-17T20:46:38.342000Z",
          "price": "1000.00",
          "lessons": [
              {
                  "title": "string"
              },
              {
                  "title": "string"
              },
              {
                  "title": "string"
              },
              {
                  "title": "string"
              },
              {
                  "title": "string5555"
              }
          ],
          "lessons_count": 5,
          "students": [
              {
                  "id": 11,
                  "first_name": "demo",
                  "last_name": "demo",
                  "email": "name12356@mail.ru"
              },
              {
                  "id": 10,
                  "first_name": "name555",
                  "last_name": "name555",
                  "email": "name555@mail.ru"
              }
          ],
          "demand_course_percent": 0,
          "students_count": 2,
          "groups_filled_percent": 0
      }
  ]
  ```
</details>

<details><summary> GET: http://127.0.0.1:8000/api/v1/courses/1/groups/  - показать список групп определенного курса, если пользователь админ.(is_stuff)</summary> 
  200 OK:
  ```
  [
      {
          "id": 3,
          "title": "Группа №1",
          "course": {
              "title": "Игра 2"
          },
          "students": [
              {
                  "id": 11,
                  "first_name": "demo",
                  "last_name": "demo",
                  "email": "name12356@mail.ru"
              },
              {
                  "id": 10,
                  "first_name": "name555",
                  "last_name": "name555",
                  "email": "name555@mail.ru"
              }
          ],
          "students_count": 2
      }
  ]
</details>
