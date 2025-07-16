from django.urls import path
from . import views

urlpatterns = [
    # главная — список привычек
    path('', views.habit_list,    name='habit_list'),

    # отметка «выполнено»
    path('complete/<int:habit_id>/', views.complete_habit, name='complete_habit'),

    # отбой привычки
    path('uncomplete/<int:habit_id>/', views.uncomplete_habit, name='uncomplete_habit'),  # ← вот тут

    # удаление привычки
    path('delete/<int:habit_id>/',   views.delete_habit,   name='delete_habit'),

    # регистрация
    path('register/',    views.register,      name='register'),

    path('profile/', views.profile, name='profile'),

]
