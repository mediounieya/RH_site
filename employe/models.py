from django.contrib.auth.models import User
from django.db import models


class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nom = models.CharField(max_length=100)
    poste = models.CharField(max_length=100)
    salaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom
    
# =========================
# CONGÉ
# =========================
class Conge(models.Model):

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]

    employe = models.ForeignKey(
        Employe,
        on_delete=models.CASCADE,
        related_name="conges"
    )

    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.TextField()

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employe.nom} ({self.date_debut} → {self.date_fin}) - {self.statut}"

    class Meta:
        ordering = ['-created_at']