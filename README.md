## What is it?

This is a simple ToDo CRUD API built with Django REST Framework.

Any authenticated user can:

- List their Todos
- Retrieve a Todo by id
- Retrieve a random Todo
- Create a Todo
- Update a Todo by id
- Delete a Todo by id
  
## Requirements

Having Python3.7+ installed.

## Installation

**After cloning the repository, create a virtual environment:**

```
python3 -m venv <env-name>
```

**Activate virtual enviroment:**

On Linux/macOS
```
source <env-name>/bin/activate
```

On Windows
```
<env-name>/Scripts/activate
```

**Install requirements:**

```
pip install -r requirements.txt
```

**Migrate:**
```
python manage.py migrate
```

**Load initial data:**
```
python manage.py loaddata users
python manage.py loaddata todos
```

**NOTE:** It is important that users data is loaded before todos data since todos have a foreignkey relationship with users.

Passwords for the initially loaded user objects are the same as their usernames, meaning if username is `test1`, then the password is also `test1`.

## Documentation

Documentation is on the home page.