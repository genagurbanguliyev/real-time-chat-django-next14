from django.urls import path
from chatapp import views

urlpatterns = [
    path('check-user', views.CheckUserViewSet.as_view(), name="check_user"),
    path('messages', views.MessagesViewSet.as_view(), name='messages'),
    path('messages/long-polling', views.MessagesLongPollingViewSet.as_view(), name='messages_long_polling'),
]
