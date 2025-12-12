from django.urls import path
from .views import (
    CustomObtainAuthToken,
    EventoListAPI,
    EventoDetailAPI,
    InscreverEventoAPI
)

urlpatterns = [
    path('token/', CustomObtainAuthToken.as_view(), name='api_token_auth'),

    path('eventos/', EventoListAPI.as_view(), name='api_evento_list'),

    path('eventos/<int:evento_id>/', EventoDetailAPI.as_view(), name='api_evento_detail'),

    path('eventos/<int:evento_id>/inscrever/', InscreverEventoAPI.as_view(), name='api_inscrever_evento'),
]
