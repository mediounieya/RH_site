from django.db import models
from employe.models import Employe


class PresenceLog(models.Model):

    TYPE_CHOICES = [
        ("IN", "Entrée"),
        ("OUT", "Sortie"),
    ]

    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    heure = models.TimeField()
    est_modifie_manuellement = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employe.nom} - {self.type} - {self.date}"