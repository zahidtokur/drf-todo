from drf_yasg.openapi import Schema
from account.serializers import UserSerializer

REGISTER_VIEW_DEFINITION = {
    'operation_description': 'User registration endpoint.',
    'request_body': UserSerializer,
    'responses': {
        '201': ''
    },
    'operation_id': 'user_create'
}

LOGIN_VIEW_DEFINITION = {
    'operation_description': 'Access token generation endpoint.',
    'request_body': Schema(
        title='User',
        type='object',
        required=['username', 'password'],
        properties={
            'username': Schema(type='string', title='Username', pattern='^[\w.@+-]+$', maxLength=150, minLength=1),
            'password': Schema(type='string', title='Password', maxLength=128, minLength=1)}
    ),
    'operation_id': 'token_create',
    'responses': {
        '201': Schema(
            title='Token',
            type='object',
            properties={
                'access': Schema(type='string', title='Access', minLength=1),
                'refresh': Schema(type='string', title='Refresh', minLength=1)
            }
        )
    }
}

LOGIN_REFRESH_DEFINITION = {
    'operation_description': 'Access token refresh endpoint.',
    'request_body': Schema(
        title='Token',
        type='object',
        required=['refresh'],
        properties={
            'refresh': Schema(type='string', title='Refresh', minLength=1)
        }
    ),
    'operation_id': 'token_update',
    'responses': {
        '201': Schema(
            title='Token',
            type='object',
            properties={
                'access': Schema(type='string', title='Access', minLength=1),
            }
        )
    }
}
