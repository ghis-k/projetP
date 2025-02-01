from django.urls import path
from .views import question_view, login_view, logout_view, register_view,score_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('question/<int:question_id>/', question_view, name='question_view'),
    path('score/', score_view, name='score'),  # Ajouter cette ligne
]