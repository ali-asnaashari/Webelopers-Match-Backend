from django.urls import path

from home.views import home, contact_us, contact_us_done

app_name = 'home'
urlpatterns = [
    path('', home, name='index'),



]
