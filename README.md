# Flask_BootStrap_Blog

A Blog made by using flask + Bootstrap

to using it,you can run

- cd to the project dir

- oepn virtual venv 
  > source venv/bin/activate
  
- install lib
  > pip install -r requirements.txt
  
- create database 
  > python3 manage.py db migrate
  
  > python3 manage.py db upgrete
  
- add a user
  > python3 manage.py shell
  
      u = Admin(username="yourname",password="yourpsd")
      db.session.add(u)
      db.session.commit()
      
  > EOF
- running
  > python manage.py runserver

after do this, you can open `127.0.0.1:5000`, by it is empty

to add message,you should open the manage site(`127.0.0.1:5000/auth/login`)
