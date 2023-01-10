from django.urls import path
from .views import RegisterView, LoginView, LoginRefreshView


app_name = 'account'

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('login/refresh/', LoginRefreshView.as_view()),
]