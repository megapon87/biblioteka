from django.urls import path
from .views import (
    home, book_detail, toggle_save,
    register, user_login, user_logout, profile,
)

urlpatterns = [
    path('', home, name='home'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('book/<int:book_id>/save/', toggle_save, name='toggle_save'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
]
