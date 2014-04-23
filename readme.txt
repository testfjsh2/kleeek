run crons: 
python manage.py cron
python manage.py set_day_bonus
for run crons methods. 
-----------------------------------
mysql install\and settings:

to /etc/mysql/my.cnf add next rows:
to [client]
default-character-set=utf8
to [mysqld] 
character-set-server=utf8
default-storage-engine=MyISAM
transaction-isolation = READ-COMMITTED

run command:
mysql -u root -h localhost -p
insert to db:
CREATE USER kleeek@localhost IDENTIFIED BY "5UK7tK0k";
create database kleeek charset=utf8;
GRANT ALL ON kleeek.* TO kleeek@localhost;
GRANT ALL ON kleeek.* TO kleeek@'%';
-----------------------------------
change password for db-user:
mysql -u root -h localhost -p
SET PASSWORD FOR kleeek@localhost = PASSWORD('5UK7tK0k');
-----------------------------------
servers restart:
/etc/init.d/apache2 restart
-----------------------------------
debug:
 python manage.py runserver 0.0.0.0:8000


migration
Установка:

Мне хватило набрать в консоли:

sudo easy_install South
Дальше я делал такие шаги:

1. Создаем свой апликейшен, например: 

python manage.py startapp myapp

2. Добавляем 'south' и 'myapp' в INSTALLED_APPS в своем settings.py
3. Создаем свои модели в models.py
4. Запускаем:
python manage.py syncdb

- оно добавляет django и south таблицы в базу данных.
5. Запускаем:

python manage.py schemamigration myapp --initial

- оно создаст начальные файлы миграции для вашего приложения.
6. Далее запускаем саму миграцию:

python manage.py migrate app

- оно добавляет наши таблицы в базу данных.
7. Далее после изменений моделей просто пользуемся:

python manage.py schemamigration myapp --auto

и будет вам радость)).
Все описанное выше - правильно, но я столкнулся с одной проблемой, когда у меня уже была создана база данных. Миграция (python manage.py migrate app) не срабатывала и писало FATAL ERROR. Как оказалось при migrate (если миграция делается первый раз) оно пытается выполнить все миграции, начиная с initial, в таких случаях делается

python manage.py migrate myapp 0001 --fake
- для фейкового применения той первой initial миграции. А дальше
python manage.py migrate app
и будет вам счастье)).

просто вместо syncdb для нового приложения делайте schemamigration "приложение" --initial и проблем не должно быть