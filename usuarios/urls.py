from django.urls import path
from .views import (
    RegistroView,
    LoginCustomizado,
    dashboard_admin,
    dashboard_organizador,
    dashboard_participante,
    confirmar_cadastro
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('registrar/', RegistroView.as_view(), name='registrar'),
    path('login/', LoginCustomizado.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('confirmar/<str:codigo>/', confirmar_cadastro, name='confirmar_cadastro'),

    path('dashboard/admin/', dashboard_admin, name='dashboard_admin'),
    path('dashboard/organizador/', dashboard_organizador, name='dashboard_organizador'),
    path('dashboard/participante/', dashboard_participante, name='dashboard_participante'),
]
