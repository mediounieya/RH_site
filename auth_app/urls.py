from django.urls import path
from . import views

urlpatterns = [

    # AUTH
    path('', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    # ACCUEIL
    path('acceuil/', views.acceuil, name='acceuil'),
    path('acceuil/rh/', views.acceuil_rh, name='acceuil_rh'),
    path('acceuil/employe/', views.acceuil_employe, name='acceuil_employe'),
]