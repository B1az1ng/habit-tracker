from django.urls import path
from . import views

urlpatterns = [
    # главная — список привычек
    path('', views.habit_list,    name='habit_list'),

    # отметка «выполнено»
    path('complete/<int:habit_id>/', views.complete_habit, name='complete_habit'),

    # удаление привычки
    path('delete/<int:habit_id>/',   views.delete_habit,   name='delete_habit'),

    # регистрация
    path('register/',    views.register,      name='register'),
]
