from django.urls import path
from eventos_uniandes_app.views import eventosBehavior

urlpatterns = [
    path('buscarEvento/', eventosBehavior.buscar_evento, name='eventos'),
    path('evento_create/', eventosBehavior.create_evento, name='evento_create'),
    path('evento_delete/', eventosBehavior.delete_evento, name='evento_delete'),
    path('evento_update/', eventosBehavior.update_evento, name='evento_update'),
    path('eventos/', eventosBehavior.buscar_evento, name='eventos'),
]


