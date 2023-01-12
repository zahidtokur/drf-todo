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

Documentation is on the home page. All the Todo endpoints require you to be authenticated. Follow these steps before using the endpoints:

1. Login using the `auth/login/` endpoint with initially provided user data (ex: `test1` - `test1` username - password pair).
2. Copy the access token that will be returned in the response body under the key `access`.
3. Click `Authorize` button on the top-right of the page.
4. You will be prompted to enter an api key. Enter the value `Bearer <access-token-you-copied>` and click `Authorize`.

You can now use the endpoints. 

**NOTE:** Access tokens expire in 15 minutes. If it expires, you can use your refresh token and generate a new access token using the `auth/login/refresh/` endpoint or repeat the previous steps. 
