# PrivateNotes

Тестовое задание для интенсива Backend/WEB Simbirsoft

Инструкция по развертыванию окружения

Необходимо выполнить в терминале следующие 2 команды

<code>docker-compose up -d --build</code>

<code>docker-compose exec web python manage.py migrate --noinput</code>

В отдельном окне терминала поднимаем нашу БД

<code>docker-compose up db</code>

В другом окне поднимаем приложение

<code>docker-compose up web</code>

Приложение должно запуститься на localhost:8000

После просмотра приложения не забудьте прописать

<code>docker-compose down</code>

для удаления изображения Docker

P.S.

Может так случится, что некоторые команды не срабатывают с первого раза (из-за асинхронности Docker, БД может подниматься позже самого приложения). Просто нужно их повторить без изменений еще раз или два.
