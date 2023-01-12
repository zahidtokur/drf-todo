from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from todo.models import Todo


class TodoViewsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.password = 'test_password'
        self.user = self.__createUser(password=self.password)

    def __createUser(self, password, username=None):
        username = username or 'test_username'
        user = User.objects.create_user(
            username=username, password=password)
        return user

    def __getAccessToken(self):
        data = {
            'username': self.user.username,
            'password': self.password
        }
        response = self.client.post('/api/auth/login/', data=data)
        return response.json().get('access')

    def __authenticateUser(self):
        access_token = self.__getAccessToken()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_create_view(self):
        todo_title = 'Test ToDo'
        data = {'title': todo_title}

        # Unauthorized request
        create_response = self.client.post('/api/todos/', data=data)
        self.assertEqual(create_response.status_code, 401)

        # Authorized request
        todos = Todo.objects.all()
        self.assertEqual(todos.count(), 0)

        self.__authenticateUser()
        create_response = self.client.post('/api/todos/', data=data)
        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(todos.count(), 1)
        todo = todos.first()
        self.assertEqual(todo.title, todo_title)
        self.assertEqual(todo.creator.id, self.user.id)

    def test_retrieve_view(self):
        todo_obj_1 = Todo.objects.create(creator=self.user, title='ToDo 1')

        # Unauthorized request
        retrieve_response = self.client.get(f'/api/todos/{todo_obj_1.id}/')
        self.assertEqual(retrieve_response.status_code, 401)

        # Authorized request
        self.__authenticateUser()
        retrieve_response = self.client.get(f'/api/todos/{todo_obj_1.id}/')
        self.assertEqual(retrieve_response.status_code, 200)
        retrieve_response_data = retrieve_response.json()
        self.assertEqual(retrieve_response_data.get('id'), todo_obj_1.id)

        # Accessing a different user's object
        different_user = self.__createUser(username='user_2', password='test_pw')
        todo_obj_2 = Todo.objects.create(creator=different_user, title='ToDo 2')
        retrieve_response = self.client.get(f'/api/todos/{todo_obj_2.id}/')
        self.assertEqual(retrieve_response.status_code, 403)

    def test_list_view(self):
        # Create ToDo objects for two users
        different_user = self.__createUser(username='user_2', password='test_pw')
        for i in range(3):
            Todo.objects.create(creator=self.user, title=f'ToDo {i+1}')
            Todo.objects.create(creator=different_user, title=f'ToDo {i+1}')

        # Unauthorized request
        retrieve_response = self.client.get('/api/todos/')
        self.assertEqual(retrieve_response.status_code, 401)

        # Authorized request
        self.__authenticateUser()
        retrieve_response = self.client.get('/api/todos/')
        self.assertEqual(retrieve_response.status_code, 200)
        retrieve_response_data = retrieve_response.json()
        result_ids = [obj['id'] for obj in retrieve_response_data.get('results')]
        # Doesn't return objects of different users
        self.assertEqual(
            Todo.objects.filter(id__in=result_ids, creator_id=self.user.id).count(), 3)

    def test_retrieve_random_view(self):
        pass

    def test_update_view(self):
        todo_obj_1 = Todo.objects.create(creator=self.user, title='ToDo 1')
        data = {
            'title': 'New Title',
            'completed': True
        }

        # Unauthorized request
        update_response = self.client.put(f'/api/todos/{todo_obj_1.id}/', data=data)
        self.assertEqual(update_response.status_code, 401)

        # Authorized request
        self.__authenticateUser()
        update_response = self.client.put(f'/api/todos/{todo_obj_1.id}/', data=data)
        self.assertEqual(update_response.status_code, 200)
        todo_obj_1 = Todo.objects.get(id=todo_obj_1.id)
        self.assertEqual(todo_obj_1.title, 'New Title')
        self.assertEqual(todo_obj_1.completed, True)

        # Accessing a different user's object
        different_user = self.__createUser(username='user_2', password='test_pw')
        todo_obj_2 = Todo.objects.create(creator=different_user, title='ToDo 2')
        update_response = self.client.put(f'/api/todos/{todo_obj_2.id}/', data=data)
        self.assertEqual(update_response.status_code, 403)        

    def test_partial_update_view(self):
        todo_obj_1 = Todo.objects.create(creator=self.user, title='ToDo 1')
        data = {'completed': True}

        # Unauthorized request
        update_response = self.client.patch(f'/api/todos/{todo_obj_1.id}/', data=data)
        self.assertEqual(update_response.status_code, 401)

        # Authorized request
        self.__authenticateUser()
        update_response = self.client.patch(f'/api/todos/{todo_obj_1.id}/', data=data)
        self.assertEqual(update_response.status_code, 200)
        todo_obj_1 = Todo.objects.get(id=todo_obj_1.id)
        self.assertEqual(todo_obj_1.completed, True)

        # Accessing a different user's object
        different_user = self.__createUser(username='user_2', password='test_pw')
        todo_obj_2 = Todo.objects.create(creator=different_user, title='ToDo 2')
        update_response = self.client.patch(f'/api/todos/{todo_obj_2.id}/', data=data)
        self.assertEqual(update_response.status_code, 403)

    def test_destroy_view(self):
        todo_obj_1 = Todo.objects.create(creator=self.user, title='ToDo 1')

        # Unauthorized request
        delete_response = self.client.delete(f'/api/todos/{todo_obj_1.id}/')
        self.assertEqual(delete_response.status_code, 401)

        # Authorized request
        self.__authenticateUser()
        delete_response = self.client.delete(f'/api/todos/{todo_obj_1.id}/')
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Todo.objects.filter(id=todo_obj_1.id).exists())

        # Accessing a different user's object
        different_user = self.__createUser(username='user_2', password='test_pw')
        todo_obj_2 = Todo.objects.create(creator=different_user, title='ToDo 2')
        delete_response = self.client.delete(f'/api/todos/{todo_obj_2.id}/')
        self.assertEqual(delete_response.status_code, 403)
