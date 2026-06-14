from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # EMPLOYÉS
    # =========================
    path('liste_employes/', views.liste_employes, name="liste_employes"),

    path('ajouter_employe/', views.ajouter_employe, name="ajouter_employe"),

    path('modifier_employe/<int:id>/', views.modifier_employe, name="modifier_employe"),

    path('supprimer_employe/<int:id>/', views.supprimer_employe, name="supprimer_employe"),


    # =========================
    # CONGÉS
    # =========================
    path('conges/', views.liste_conges, name='liste_conges'),

    path('conges/demander/', views.demander_conge, name='demander_conge'),

    path('conges/modifier/<int:id>/', views.modifier_conge, name='modifier_conge'),

    path('conges/supprimer/<int:id>/', views.supprimer_conge, name='supprimer_conge'),


    # =========================
    # RH ACTIONS
    # =========================
    path('conges/valider/<int:id>/', views.valider_conge, name='valider_conge'),

    path('conges/refuser/<int:id>/', views.refuser_conge, name='refuser_conge'),
]