from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('compose/', views.compose_message, name='compose_message'),
    path('compose/<str:recipient_username>/', views.compose_message, name='compose_to_user'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),
    path('conversation/<int:user_id_other>/', views.conversation, name='conversation'),
]