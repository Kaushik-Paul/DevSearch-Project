from django.urls import path

from projects import views

urlpatterns = [
    path('project/', views.projects_list, name='project-list'),
    path('project/<str:pk>/', views.project_detail, name='project-detail'),
    path('project-create/', views.project_create, name='project-create'),
    path('project-update/<str:pk>', views.project_update, name='project-update'),
    path('project-delete/<str:pk>', views.project_delete, name='project-delete'),
]
