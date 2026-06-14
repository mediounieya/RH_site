from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .form import CustomUserCreationForm


# =========================
# INSCRIPTION
# =========================
def inscription(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès 👍")
            return redirect('connexion')
        else:
            messages.error(request, "Erreur dans le formulaire")

    else:
        form = CustomUserCreationForm()

    return render(request, 'inscription.html', {'form': form})


# =========================
# CONNEXION (AVEC GESTION ERREURS)
# =========================
def connexion(request):

    # =========================
    # GET → afficher page login
    # =========================
    if request.method == "GET":
        return render(request, "connexion.html")

    # =========================
    # POST → traitement login
    # =========================
    username = request.POST.get('username')
    password = request.POST.get('password')

    # champs vides
    if not username or not password:
        messages.error(request, "Veuillez remplir tous les champs")
        return render(request, "connexion.html")

    user = authenticate(request, username=username, password=password)

    # mauvais login
    if user is None:
        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
        return render(request, "connexion.html")

    # login OK
    login(request, user)

    # redirection par rôle
    if user.groups.filter(name="RH").exists():
        return redirect('acceuil_rh')

    elif user.groups.filter(name="EMPLOYE").exists():
        return redirect('acceuil_employe')

    return redirect('acceuil')
# =========================
# ACCUEIL GENERIQUE
# =========================
def acceuil(request):

    role = "RH" if request.user.groups.filter(name="RH").exists() else "EMPLOYE"

    return render(request, "acceuil.html", {
        "role": role
    })


# =========================
# DASHBOARD RH
# =========================
@login_required
def acceuil_rh(request):

    if not request.user.groups.filter(name="RH").exists():
        return redirect('acceuil')

    return render(request, 'acceuil_rh.html')


# =========================
# DASHBOARD EMPLOYE
# =========================
@login_required
def acceuil_employe(request):

    if not request.user.groups.filter(name="EMPLOYE").exists():
        return redirect('acceuil')

    return render(request, 'acceuil_employe.html')


# =========================
# DECONNEXION
# =========================
def deconnexion(request):
    logout(request)
    return redirect('connexion')