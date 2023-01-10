from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='DRF To-do App',
        default_version='1.0',
        description='API Documentation for To-do App'
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('todos/', include('todo.urls'), name='todos'),
        path('auth/', include('account.urls'), name='auth'),
        path('docs/', schema_view.with_ui('swagger')),
    ])),
]
