from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Employe, Conge
from .forms import EmployeForm, CongeForm


# =========================
# ROLE RH CHECK
# =========================
def is_rh(user):
    return user.groups.filter(name="RH").exists()


# =========================
# LISTE EMPLOYÉS
# =========================
@login_required
def liste_employes(request):

    if is_rh(request.user):
        employes = Employe.objects.all()
    else:
        employes = Employe.objects.filter(user=request.user)

    return render(request, 'employe/list.html', {
        'employes': employes
    })


# =========================
# AJOUT EMPLOYÉ (RH)
# =========================
@login_required
def ajouter_employe(request):

    if not is_rh(request.user):
        return redirect("liste_employes")

    form = EmployeForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('liste_employes')

    return render(request, 'employe/formulaire.html', {'form': form})
# =========================
# MODIFIER EMPLOYÉ (RH)
# =========================
@login_required
def modifier_employe(request, id):

    if not is_rh(request.user):
        return redirect("liste_employes")

    employe = get_object_or_404(Employe, id=id)

    form = EmployeForm(request.POST or None, instance=employe)

    if form.is_valid():
        form.save()
        return redirect('liste_employes')

    return render(request, 'employe/formulaire.html', {'form': form})


# =========================
# SUPPRIMER EMPLOYÉ (RH)
# =========================
@login_required
def supprimer_employe(request, id):

    if not is_rh(request.user):
        return redirect("liste_employes")

    employe = get_object_or_404(Employe, id=id)

    if request.method == "POST":
        employe.delete()
        return redirect('liste_employes')

    return render(request, 'employe/confirmer_suppression.html', {
        'employe': employe
    })
# =========================
# LISTE CONGÉS (RH + EMPLOYÉ)
# =========================
@login_required
def liste_conges(request):

    if is_rh(request.user):
        conges = Conge.objects.all().order_by('-created_at')
    else:
        employe = get_object_or_404(Employe, user=request.user)
        conges = Conge.objects.filter(employe=employe).order_by('-created_at')

    return render(request, 'employe/liste_conges.html', {
        'conges': conges
    })


# =========================
# DEMANDER CONGÉ (EMPLOYÉ)
# =========================
@login_required
def demander_conge(request):

    employe = get_object_or_404(Employe, user=request.user)

    form = CongeForm(request.POST or None)

    if form.is_valid():
        conge = form.save(commit=False)
        conge.employe = employe
        conge.statut = "en_attente"
        conge.save()
        return redirect('liste_conges')

    return render(request, 'employe/demander_conge.html', {
        'form': form
    })


# =========================
# MODIFIER CONGÉ (EMPLOYÉ)
# =========================
@login_required
def modifier_conge(request, id):

    employe = get_object_or_404(Employe, user=request.user)

    conge = get_object_or_404(Conge, id=id, employe=employe)

    if conge.statut != "en_attente":
        return redirect('liste_conges')

    form = CongeForm(request.POST or None, instance=conge)

    if form.is_valid():
        form.save()
        return redirect('liste_conges')

    return render(request, 'employe/formulaire_conge.html', {
        'form': form
    })


# =========================
# SUPPRIMER CONGÉ (EMPLOYÉ)
# =========================
@login_required
def supprimer_conge(request, id):

    employe = get_object_or_404(Employe, user=request.user)

    conge = get_object_or_404(Conge, id=id, employe=employe)

    if conge.statut != "en_attente":
        return redirect('liste_conges')

    if request.method == "POST":
        conge.delete()
        return redirect('liste_conges')

    return render(request, 'employe/confirmer_suppression_conge.html', {
        'conge': conge
    })


# =========================
# VALIDER CONGÉ (RH)
# =========================
@login_required
def valider_conge(request, id):

    if not is_rh(request.user):
        return redirect("liste_conges")

    conge = get_object_or_404(Conge, id=id)

    if conge.statut == "en_attente":
        conge.statut = "accepte"
        conge.save()

    return redirect('liste_conges')


# =========================
# REFUSER CONGÉ (RH)
# =========================
@login_required
def refuser_conge(request, id):

    if not is_rh(request.user):
        return redirect("liste_conges")

    conge = get_object_or_404(Conge, id=id)

    if conge.statut == "en_attente":
        conge.statut = "refuse"
        conge.save()

    return redirect('liste_conges')