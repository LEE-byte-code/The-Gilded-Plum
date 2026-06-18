from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservations.urls')),
    path('', include('menu.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static('/images/', document_root=settings.BASE_DIR / 'images')
    urlpatterns += static('/audio/', document_root=settings.BASE_DIR / 'audio')
