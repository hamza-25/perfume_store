python -m venv venv
source venv/bin/activate
    flask
    flask_sqlalchemy
    pumysql
if these packages above are install it dont make it
make sure mysql running
create db perfume_db
cd project dir
run python3
>> from app import app, db
>> with app.app_context():
...     db.create_all()
...
>>
this step to create table on db 

