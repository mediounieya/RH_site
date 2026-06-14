from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, date

from employe.models import Employe
from .models import PresenceLog


# =========================
# HELPERS
# =========================
def get_employe(user):
    return Employe.objects.filter(user=user).first()


# =========================
# DASHBOARD PRESENCE
# =========================
@login_required
def presence_view(request):

    employe = get_object_or_404(Employe, user=request.user)

    logs = PresenceLog.objects.filter(
        employe=employe,
        date=date.today()
    ).order_by("heure")

    last = logs.last()

    can_enter = (last is None) or (last.type == "OUT")
    can_exit = (last is not None and last.type == "IN")

    return render(request, "presence/presence.html", {
        "logs": logs,
        "employe": employe,
        "can_enter": can_enter,
        "can_exit": can_exit
    })


# =========================
# ENTREE
# =========================
@login_required
def pointer_entree(request):

    employe = get_object_or_404(Employe, user=request.user)

    logs = PresenceLog.objects.filter(
        employe=employe,
        date=date.today()
    ).order_by("heure")

    last = logs.last()

    # ❌ déjà ouvert
    if last and last.type == "IN":
        return redirect("presence")

    PresenceLog.objects.create(
        employe=employe,
        date=date.today(),
        type="IN",
        heure=datetime.now().time(),
        est_modifie_manuellement=False
    )

    return redirect("presence")


# =========================
# SORTIE
# =========================
@login_required
def pointer_sortie(request):

    employe = get_object_or_404(Employe, user=request.user)

    logs = PresenceLog.objects.filter(
        employe=employe,
        date=date.today()
    ).order_by("heure")

    last_in = None

    for l in reversed(logs):
        if l.type == "IN":
            last_in = l
            break
        if l.type == "OUT":
            break

    if not last_in:
        return redirect("presence")

    PresenceLog.objects.create(
        employe=employe,
        date=date.today(),
        type="OUT",
        heure=datetime.now().time(),
        est_modifie_manuellement=False
    )

    return redirect("presence")


# =========================
# HISTORIQUE EMPLOYÉ
# =========================
@login_required
def historique_presence(request, employe_id=None):

    is_rh_view = False

    # =========================
    # RH → voir un employé précis
    # =========================
    if employe_id:

        if not request.user.groups.filter(name="RH").exists():
            return redirect("presence")

        employe = get_object_or_404(Employe, id=employe_id)
        is_rh_view = True

    # =========================
    # EMPLOYÉ → son propre historique
    # =========================
    else:
        employe = get_object_or_404(Employe, user=request.user)

    logs = PresenceLog.objects.filter(
        employe=employe
    ).order_by("-date", "heure")

    grouped = {}

    for log in logs:
        grouped.setdefault(log.date, []).append(log)

    historique = []

    for d, logs_jour in grouped.items():

        logs_jour = sorted(logs_jour, key=lambda x: x.heure)

        cycles = []
        current_in = None

        for log in logs_jour:

            if log.type == "IN":
                current_in = log.heure

            elif log.type == "OUT":
                if current_in:
                    cycles.append({
                        "entree": current_in,
                        "sortie": log.heure
                    })
                current_in = None

        historique.append({
            "date": d,
            "cycles": cycles
        })

    return render(request, "presence/historique.html", {
        "historique": historique,
        "employe": employe,
        "is_rh_view": is_rh_view
    })

# =========================
# AJOUT MANUEL RH
# =========================
@login_required
def ajouter_presence(request):

    employe = get_object_or_404(Employe, user=request.user)

    selected_date = request.GET.get("date")

    try:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except:
        selected_date = date.today()

    logs = PresenceLog.objects.filter(
        employe=employe,
        date=selected_date
    ).order_by("heure")

    help_message = None

    if request.method == "POST":

        form = PresenceLogForm(request.POST)

        if form.is_valid():

            obj = form.save(commit=False)
            obj.employe = employe
            obj.est_modifie_manuellement = True

            day_logs = PresenceLog.objects.filter(
                employe=employe,
                date=obj.date
            ).order_by("heure")

            last = day_logs.last()

            # ❌ IN consécutif interdit
            if obj.type == "IN" and last and last.type == "IN":
                help_message = "⚠ Entrée déjà ouverte."
                return render(request, "presence/form.html", {
                    "form": form,
                    "logs": logs,
                    "selected_date": selected_date,
                    "help_message": help_message
                })

            # ❌ OUT sans IN
            if obj.type == "OUT" and (not last or last.type == "OUT"):
                help_message = "⚠ Sortie invalide."
                return render(request, "presence/form.html", {
                    "form": form,
                    "logs": logs,
                    "selected_date": selected_date,
                    "help_message": help_message
                })

            obj.save()
            return redirect(f"/presence/ajouter/?date={selected_date}")

    else:
        form = PresenceLogForm(initial={"date": selected_date})

    return render(request, "presence/form.html", {
        "form": form,
        "logs": logs,
        "selected_date": selected_date,
        "help_message": help_message
    })