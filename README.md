<h1 align="center">Instagram Bot</h1>

## Описание
Программа для эмуляции действий пользователя в инстаграме
 Реализованы следующие методы:
 + Метод авторизации в инстаграме
 + Метод нахождения фотографий по хэштегам и их лайканье
 + Метод для поставки лайка на пост по прямой ссылке
 + Метод для сбора ссылок на все посты пользователя
 + Метод для добавления лайков на все посты пользователя по ссылке на аккаунт пользователя
 + Метод для скачивания контента со страницы пользователя (не работает, если в посте больше одной фотографии)
 + Метод подписки на всех подписчиков переданного аккаунта
 + Метод для отправки сообщений в директ
 + Метод отписки от всех пользователей
 + Метод отписки, отписываемся от всех кто не подписан на нас

## Используемые технологии
![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=python&logoColor=python)

### Запуск проекта

1 - Разархивировать проект и запустить в IDE

2 - Понаботся указать в программе путь к chromedriver.exe

3 - В файле auth_data указать правильно свой логин и пароль от инстаграмма

4 - Для коректной работы проверить правильность функции
 (Они могут не работать, так как Инстаграм меняет свой сайт постоянно, чтобы нельзя было парсить данные)
 Нужно проверить правильнось Xpath до элементов на сайте, с которыми взаимодействуете( кнопки, ссылки и т.д.)
