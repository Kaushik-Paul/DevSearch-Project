from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('users/', views.profiles, name='profiles'),
    path('users/<str:pk>', views.profile_details, name='profile-details'),
    path('account/', views.user_account, name='user-account'),

    path('edit-account/', views.edit_account, name='edit-account'),

    path('create-skill/', views.create_skill, name="create-skill"),
    path('update-skill/<str:pk>/', views.update_skill, name="update-skill"),
    path('delete-skill/<str:pk>/', views.delete_skill, name="delete-skill"),
]
