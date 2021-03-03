from django.contrib.auth.views import LoginView
from django.urls import path

from accounts.views import signup, logout_user

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_user, name='logout')

]
