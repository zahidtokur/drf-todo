from drf_yasg.openapi import Schema
from account.serializers import UserSerializer

REGISTER_VIEW = {
    'operation_description': 'User registration endpoint.',
    'operation_summary': 'register user',
    'request_body': UserSerializer,
    'responses': {
        '201': ''
    },
    'operation_id': 'user_create'
}

LOGIN_VIEW = {
    'operation_description': 'Access token generation endpoint. Provide your username and password to receive a token that will be used to access other endpoints. Access tokens are valid for 15 minutes. This endpoint is rate limited to 10 requests an hour.',
    'operation_summary': 'generate access token',
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

LOGIN_REFRESH_VIEW = {
    'operation_description': 'Access token refresh endpoint. Using your refresh token, generate a new access token after it expires. Refresh tokens are valid for 4 hours. This endpoint is rate limited to 12 requests a day.',
    'operation_summary': 'refresh access token',
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
