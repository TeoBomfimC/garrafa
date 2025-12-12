from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', lambda request: redirect('login'), name='home'),

    path('usuarios/', include('usuarios.urls')),
    path('eventos/', include('eventos.urls')),
    path('api/', include('api_rest.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
