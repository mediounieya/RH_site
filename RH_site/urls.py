from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # =========================
    # AUTH APP
    # =========================
    path('', include('auth_app.urls')),

    # =========================
    # MODULES
    # =========================
    path('employes/', include('employe.urls')),
    path('presence/', include('presence.urls')),
]