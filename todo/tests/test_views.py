from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from todo.models import Todo


class TodoViewsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def __createUser(self, username, password):
        user = User.objects.create_user(
            username=username, password=password)
        return user

    def __getAccessToken(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        response = self.client.post('/api/auth/login/', data=data)
        return response.json().get('access')

    def __authenticateUser(self, username, password):
        access_token = self.__getAccessToken(username, password)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_views_unauthenticated(self):
        data = {'title': 'Test ToDo', 'completed': True}
        post_response = self.client.post('/api/todos/', data=data)
        self.assertEqual(post_response.status_code, 401)

        put_response = self.client.put(f'/api/todos/1/', data=data)
        self.assertEqual(put_response.status_code, 401)

        patch_response = self.client.patch(f'/api/todos/1/', data=data)
        self.assertEqual(patch_response.status_code, 401)

        delete_response = self.client.delete(f'/api/todos/1/')
        self.assertEqual(delete_response.status_code, 401)

        get_response = self.client.get(f'/api/todos/1/')
        self.assertEqual(get_response.status_code, 401)

        get_list_response = self.client.get('/api/todos/')
        self.assertEqual(get_list_response.status_code, 401)

        get_random_response = self.client.get('/api/todos/random/')
        self.assertEqual(get_random_response.status_code, 401)

    def test_create_authenticated(self):
        user = self.__createUser('test_username', 'password')
        self.__authenticateUser(user.username, 'password')

        todos = Todo.objects.all()
        self.assertEqual(todos.count(), 0)

        todo_title = 'Test ToDo'
        data = {'title': todo_title}
        create_response = self.client.post('/api/todos/', data=data)
        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(todos.count(), 1)
        todo = todos.first()
        self.assertEqual(todo.title, todo_title)
        self.assertEqual(todo.creator.id, user.id)

    def test_retrieve_authenticated(self):
        user = self.__createUser('test_username', 'password')
        self.__authenticateUser(user.username, 'password')

        todo_obj_1 = Todo.objects.create(creator=user, title='ToDo 1')
        retrieve_response = self.client.get(f'/api/todos/{todo_obj_1.id}/')
        self.assertEqual(retrieve_response.status_code, 200)
        retrieve_response_data = retrieve_response.json()
        self.assertEqual(retrieve_response_data.get('id'), todo_obj_1.id)

        # Accessing a different user's object
        user_2 = self.__createUser(username='user_2', password='test_pw')
        todo_obj_2 = Todo.objects.create(creator=user_2, title='ToDo 2')
        retrieve_response = self.client.get(f'/api/todos/{todo_obj_2.id}/')
        self.assertEqual(retrieve_response.status_code, 403)

    def test_list_authenticated(self):
        # Create ToDo objects for two users
        user = self.__createUser('test_username', 'password')
        user_2 = self.__createUser('user_2', 'password')
        for i in range(3):
            Todo.objects.create(creator=user, title=f'ToDo {i+1}')
            Todo.objects.create(creator=user_2, title=f'ToDo {i+1}')

        self.__authenticateUser(user.username, 'password')
        retrieve_response = self.client.get('/api/todos/')
        self.assertEqual(retrieve_response.status_code, 200)
        retrieve_response_data = retrieve_response.json()
        result_ids = [obj['id']
                      for obj in retrieve_response_data.get('results')]
        # Doesn't return objects of different users
        self.assertEqual(
            Todo.objects.filter(id__in=result_ids, creator_id=user.id).count(), 3)

    def test_retrieve_random_authenticated(self):
        # Create ToDo objects for two users
        user = self.__createUser('test_username', 'password')
        user_2 = self.__createUser('user_2', 'password')
        for i in range(3):
            Todo.objects.create(creator=user, title=f'ToDo {i+1}')
            Todo.objects.create(creator=user_2, title=f'ToDo {i+1}')

        self.__authenticateUser(user.username, 'password')
        retrieve_response = self.client.get('/api/todos/random/')
        self.assertEqual(retrieve_response.status_code, 200)
        retrieve_response_data = retrieve_response.json()
        todo_obj_id = retrieve_response_data.get('id')
        self.assertEqual(Todo.objects.get(
            id=todo_obj_id).creator_id, user.id)

    def test_update_authenticated(self):
        user = self.__createUser('test_username', 'password')
        todo_obj_1 = Todo.objects.create(creator=user, title='ToDo 1')
        data = {
            'title': 'New Title',
            'completed': True
        }

        self.__authenticateUser(user.username, 'password')
        update_response = self.client.put(
            f'/api/todos/{todo_obj_1.id}/', data=data)
        self.assertEqual(update_response.status_code, 200)
        todo_obj_1 = Todo.objects.get(id=todo_obj_1.id)
        self.assertEqual(todo_obj_1.title, 'New Title')
        self.assertEqual(todo_obj_1.completed, True)

        # Accessing a different user's object
        user_2 = self.__createUser('user_2', 'password')
        todo_obj_2 = Todo.objects.create(creator=user_2, title='ToDo 2')
        update_response = self.client.put(
            f'/api/todos/{todo_obj_2.id}/', data=data)
        self.assertEqual(update_response.status_code, 403)

    def test_partial_update_authenticated(self):
        user = self.__createUser('test_username', 'password')
        todo_obj_1 = Todo.objects.create(creator=user, title='ToDo 1')
        data = {'completed': True}

        self.__authenticateUser(user.username, 'password')
        update_response = self.client.patch(
            f'/api/todos/{todo_obj_1.id}/', data=data)
        self.assertEqual(update_response.status_code, 200)
        todo_obj_1 = Todo.objects.get(id=todo_obj_1.id)
        self.assertEqual(todo_obj_1.completed, True)

        # Accessing a different user's object
        user_2 = self.__createUser('user_2', 'password')
        todo_obj_2 = Todo.objects.create(creator=user_2, title='ToDo 2')
        update_response = self.client.patch(
            f'/api/todos/{todo_obj_2.id}/', data=data)
        self.assertEqual(update_response.status_code, 403)

    def test_destroy_authenticated(self):
        user = self.__createUser('test_username', 'password')
        todo_obj_1 = Todo.objects.create(creator=user, title='ToDo 1')

        self.__authenticateUser(user.username, 'password')
        delete_response = self.client.delete(f'/api/todos/{todo_obj_1.id}/')
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Todo.objects.filter(id=todo_obj_1.id).exists())

        # Accessing a different user's object
        user_2 = self.__createUser('user_2', 'password')
        todo_obj_2 = Todo.objects.create(creator=user_2, title='ToDo 2')
        delete_response = self.client.delete(f'/api/todos/{todo_obj_2.id}/')
        self.assertEqual(delete_response.status_code, 403)
