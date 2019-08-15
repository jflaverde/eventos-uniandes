from django.urls import path
from eventos_uniandes_app.views import views

urlpatterns = [
    path('evento_create/', views.create_evento, name='evento_create'),
    path('evento_delete/<int:idEvento>', views.delete_evento, name='evento_delete'),
    path('updateEvento/<int:idEvento>', views.updateEvento, name='updateEvento'),
    path('users/add/', views.postUser, name='addUser'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('eventos/<int:userid>/', views.eventos, name='eventos'),
    path('evento/<int:idEvento>', views.getEventoDetail, name='getDetalleEvento'),
    path('categorias/', views.getCategorias, name='getCategorias'),

]


