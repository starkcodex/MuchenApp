from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('create/', views.create_machen, name='create-todo'),
    path('todo/<id>', views.todo_detail, name='todo'),
    path('todo-delete/<id>', views.todo_delete, name='todo-delete'),
    path('edit-delete/<id>', views.todo_edit, name='todo-edit'),
]