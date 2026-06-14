from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # EMPLOYÉ
    # =========================
    path("", views.presence_view, name="presence"),

    path("entree/", views.pointer_entree, name="pointer_entree"),

    path("sortie/", views.pointer_sortie, name="pointer_sortie"),

    path("historique/", views.historique_presence, name="historique_presence"),


    # =========================
    # RH / EMPLOYÉ SPÉCIFIQUE
    # =========================
    path("historique/<int:employe_id>/", views.historique_presence, name="historique_employe"),

]