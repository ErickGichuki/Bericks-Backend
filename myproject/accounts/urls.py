from django.urls import path
from .views import SignupView, LoginView, UserListView, AddUserView, DeleteUserView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user_list'), 
    path('users/add/', AddUserView.as_view(), name='add_user'),
    path('users/delete/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
]
