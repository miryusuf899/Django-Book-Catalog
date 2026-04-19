from django.urls import path
from .views import *

urlpatterns = [
    # 1. Home / Profile (Task 6)
    path('home/', home, name='home'),

    # 2. Book CRUD (Task 7, 8, 10)
    path('', book_list, name='book_list'),
    path('book/<int:pk>/', book_detail, name='book_detail'),
    path('book/create/', create_book, name='create_book'),
    path('book/update/<int:pk>/', book_update, name='book_update'),
    path('book/delete/<int:pk>/', book_delete, name='book_delete'),

    # 3. Statistics (Task 11)
    path('statistics/', aggregate_view, name='statistics'),

    # 4. Authentication (Task 12)
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # 5. Email Confirmation (Task 13)
    path('verify/<str:token>/', verify_email, name='verify_email'),

    # 6. Password Features (Task 14)
    path('password-reset/', reset_request, name='reset_request'),
    path('reset/<str:token>/', reset_confirm, name='reset_confirm'),
    path('password-change/', change_password, name='change_password'),
]