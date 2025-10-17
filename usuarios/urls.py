from django.urls import path
from .views import RegistroView, LoginCustomizado 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('registrar/', RegistroView.as_view(), name='registrar'), 
    
    path('login/', LoginCustomizado.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]