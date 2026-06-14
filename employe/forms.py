from django import forms
from django.contrib.auth.models import User
from .models import Employe, Conge
from django.utils import timezone

# =========================
# FORM EMPLOYÉ
# =========================
class EmployeForm(forms.ModelForm):

    email = forms.EmailField(required=False, label="Email")

    class Meta:
        model = Employe
        fields = ['user', 'nom', 'poste', 'salaire']

        widgets = {
            'user': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nom'
            }),
            'poste': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Poste'
            }),
            'salaire': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Salaire'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # style email
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Email'
        })

        # ✅ éviter crash si user n'existe pas
        if self.instance and self.instance.pk:
            user = getattr(self.instance, "user", None)
            if user:
                self.fields['email'].initial = user.email

    def clean_user(self):
        user = self.cleaned_data.get('user')

        # ✅ sécurité : vérifier user existe
        if not user:
            raise forms.ValidationError("Utilisateur obligatoire")

        # ✅ éviter doublon OneToOne
        if Employe.objects.filter(user=user).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ce user est déjà lié à un employé")

        return user

    def save(self, commit=True):
        instance = super().save(commit=False)

        email = self.cleaned_data.get('email')

        # ✅ protection contre crash
        if instance.user:
            if email:
                instance.user.email = email
            instance.user.save()

        if commit:
            instance.save()

        return instance



# =========================
# FORM CONGÉ (SÉCURISÉ)
# =========================
class CongeForm(forms.ModelForm):

    class Meta:
        model = Conge

        # ⚠️ IMPORTANT: employe retiré pour éviter faille sécurité
        fields = ['date_debut', 'date_fin', 'motif']

        widgets = {
            'date_debut': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input input-bordered w-full'
            }),
            'date_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input input-bordered w-full'
            }),
            'motif': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'placeholder': 'Motif du congé'
            }),
        }
         # ✅ AJOUT ICI
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get("date_debut")
        date_fin = cleaned_data.get("date_fin")

        if date_debut and date_fin:

            # ❌ fin avant début
            if date_fin < date_debut:
                raise forms.ValidationError(
                    "La date de fin doit être après la date de début."
                )

            # ❌ date début dans le passé
            if date_debut < timezone.now().date():
                raise forms.ValidationError(
                    "La date de début ne peut pas être dans le passé."
                )

        return cleaned_data