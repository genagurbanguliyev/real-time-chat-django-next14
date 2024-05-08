from django.urls import path
from chatapp import views

urlpatterns = [
    path('check-user', views.CheckUserViewSet.as_view(), name="check_user"),
    path('messages', views.MessagesViewSet.as_view(), name='messages'),
]
