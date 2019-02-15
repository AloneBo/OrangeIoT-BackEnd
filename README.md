### Orange Internet of things back-end implement. Write with Flask.

### Run
First, Run https://github.com/AloneBo/OrangeIoT-FrontEnd.
Install MySQL or sqlite3(default) & Redis in your PC.

> If error, see https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost,
create `db_iotweb` database in your MySQL.


Then, ctrl+t, type:
```
pip3 install -r packages.txt
python3 manger.py db init 
python manger.py db migrate
python manger.py db upgrade
mv user.db iotweb
sh runserver.py
curl localhost:8080/api/v1.0/add_user
```

