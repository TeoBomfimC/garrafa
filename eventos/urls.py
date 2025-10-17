from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('novo/', views.criar_evento, name='criar_evento'),
    path('<int:evento_id>/', views.detalhe_evento, name='detalhe_evento'),
    
    path('<int:evento_id>/inscrever/', 
         views.inscrever_evento, 
         name='inscrever_evento'),
    
    path('<int:evento_id>/emitir/<int:usuario_id>/', 
         views.emitir_certificado, 
         name='emitir_certificado'),
         
    path('certificado/<int:certificado_id>/', 
         views.visualizar_certificado, 
         name='visualizar_certificado'),
]