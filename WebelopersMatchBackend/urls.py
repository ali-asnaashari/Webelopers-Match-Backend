
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home.views import home, contact_us, contact_us_done

urlpatterns = [
    path('', home, name='home' ),
    path('contact_us/', contact_us, name='contact_us'),
    path('contact_us_done/', contact_us_done, name='contact_us_done'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
