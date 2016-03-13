from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'json', views.restaurant_list),
    #url(r'push', views.sendPushMessage),
]