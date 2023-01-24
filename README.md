# Yatube - форум писателей
## Оглавление
1. [Описание проекта](https://github.com/TomatoInOil/hw05_final#описание-проекта)
2. [Технологии](https://github.com/TomatoInOil/hw05_final#технологии)
3. [Как развернуть в режиме разработчика?](https://github.com/TomatoInOil/hw05_final#как-развернуть)
4. [Об авторe](https://github.com/TomatoInOil/hw05_final#об-авторе)
## Описание проекта
***Yatube*** - форум, на котором можно опубликовать свои тексты (записи, рассказы, стихотворения и т.п.). Можно прикреплять к посту фотографию, комментировать записи других пользователей и подписываться на авторов. 
## Технологии
- `Python`
- `Django`
- `Bootstrap`
## Как развернуть в режиме разработчика?
Склонировать репозиторий
```BASH
git clone https://github.com/TomatoInOil/hw05_final.git
```
Перейти в директорию с проектом
```BASH
cd hw05_final/
```
Установить и активировать виртуальное окружение
```BASH
python -m venv venv
source venv/Scripts/activate
```
Обновить pip
```BASH
python -m pip install --upgrade pip
```
Установить зависимости
```BASH
pip install -r requirements.txt
```
Переместиться в директорию `yatube/`
```BASH
cd yatube/
```
Запустить сервер разработчика 
```BASH
python manage.py runserver
```
## Об авторe
Проект выполнен в рамках прохождения курса в Яндекс.Практикуме Даниилом Паутовым.
