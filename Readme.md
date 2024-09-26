User 1 (John):
Username: user1
Password: password123
User 2 (Jane):
Username: user2
Password: password456

# Chat app
## Python django application for sending messages and managing threads
### Features:
* creation (if a thread with particular users exists - just return it.);
* removing a thread;
* retrieving the list of threads for any user;
* creation of a message and retrieving message list for the thread;
* marking the message as read;
* retrieving a number of unread messages for the user


## Configure envs

Create django config: .env
```
DJANGO_DEBUG_MODE=false
DJANGO_SECRET_KEY=django-insecure-i00tygfvwjav1f%5qsu9)otzd&7k*hj^57=qdvoxg^5d=ac8lw
```


## Run database migration
```
python manage.py makemigrations
python manage.py migrate
```

## Load test data

```
python manage.py loaddata test_data.json
```

### Test users (for debug):

User 1 (John):
Username: user1
Password: password123

User 2 (Jane):
Username: user2
Password: password456

## Use swagger UI to navigate RESTAPI endpoints

http://127.0.0.1:8000/api/schema/swagger-ui/
