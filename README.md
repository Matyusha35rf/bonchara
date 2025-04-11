# Бончара

# \>>Работа с функциями

## Расписание
* **Получение расписания по ID группы и недели (относительное изменение недели от текущего)** <br />

``get_schedule_by_id(group, week) ``


* **Получение расписания по названию группы (Напр. "ИСТ-341") и недели (относительное изменение недели от текущего)**

```
from schedule import get_schedule_by_name
get_schedule_by_name(name_group, week)
```
* **Получение расписание конкретного дня недели по:**
  * **ID**
  * **Названия группы**


## Соответствия групп и ID
* **Получение id группы по названию группы (Напр. "ИСТ-341")**

``find_id_by_name(name_group)``
* **Получение списка всех id групп**

``get_matched_groups()``

## Сообщения студента

* **Получение содержимого сообщения в JSON по id сообщения**

```
form lk.message import get_message_by_id
get_message_by_id(id_mes, email, password)
```
* **Получение id последнего сообщения**

```
form lk.message import get_id_last_message
get_id_last_message(email, password)
```

# Общие функции для программирования

* **Вход в аккаунт**

```
import lk.lk_func
auth(session, email,pass)
```

* **Получение номер пары**