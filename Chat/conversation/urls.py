from django.urls import path
from . import views
from django.views.generic.base import TemplateView
app_name="conversation"
urlpatterns = [
    path('username/<str:username>' , views.room , name="chat" ),
    path("period-message/<str:to_user>",views.send_periodic_messages, name="periodic_task"),
    path("messages/<str:username>" ,views.RetrieveMessages.as_view() ,name="messages" )
]
