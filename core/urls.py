from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('lost-found/', views.lost_and_found, name='lost_found'),
    path('lost-found/post/', views.post_item, name='post_item'),
    path('ai-chat/', views.ai_chat_page, name='ai_chat'),
    path('api/chat/', views.ai_chat_api, name='ai_chat_api'),
    path('complaint/', views.complaint_page, name='complaint'),
]