from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.models import User
from collections import defaultdict
from django.shortcuts import render, redirect
from .models import Team, Pickems, Score, Match, Comment
import pandas as pd
import os
from datetime import datetime, timedelta

# Globals
TEAM_CODES = {
    "Mexico": "MEX",
    "South Africa": "RSA",
    "Czechia": "CZE",
    "Canada": "CAN",
    "Bosnia-Herzegovina": "BIH",
    "Qatar": "QAT",
    "Switzerland": "SUI",
    "Brazil": "BRA",
    "Morocco": "MAR",
    "Haiti": "HAI",
    "Scotland": "SCO",
    "USA": "USA",
    "Paraguay": "PAR",
    "Australia": "AUS",
    "Türkiye": "TUR",
    "Germany": "GER",
    "Curacao": "CUW",
    "Ivory Coast": "CIV",
    "Ecuador": "ECU",
    "Netherlands": "NED",
    "Japan": "JPN",
    "Sweden": "SWE",
    "Tunisia": "TUN",
    "Belgium": "BEL",
    "Egypt": "EGY",
    "IR Iran": "IRN",
    "New Zealand": "NZL",
    "Spain": "ESP",
    "Cape Verde": "CPV",
    "Saudi Arabia": "KSA",
    "Uruguay": "URU",
    "France": "FRA",
    "Senegal": "SEN",
    "Iraq": "IRQ",
    "Norway": "NOR",
    "Argentina": "ARG",
    "Algeria": "ALG",
    "Austria": "AUT",
    "Jordan": "JOR",
    "Portugal": "POR",
    "Congo DR": "COD",
    "Uzbekistan": "UZB",
    "Colombia": "COL",
    "England": "ENG",
    "Croatia": "CRO",
    "Ghana": "GHA",
    "Panama": "PAN",
    "Korea Republic":"KOR"
}

def calculate_points(user):
    matches = Match.objects.all()
    picks = Pickems.objects.get(user=user)

    user_teams = [
        picks.group_A, picks.group_B, picks.group_C, picks.group_D,
        picks.group_E, picks.group_F, picks.group_G, picks.group_H,
        picks.group_I, picks.group_J, picks.group_K, picks.group_L,
    ]

    total = 0

    for m in matches:
        if m.home_score is None or m.away_score is None:
            continue

        for team in user_teams:
            if team.name not in [m.home_team, m.away_team]:
                continue

            # ✅ GROUP scoring
            if m.stage == "GROUP":
                if m.home_score == m.away_score:
                    total += 1.5
                else:
                    winner = m.home_team if m.home_score > m.away_score else m.away_team
                    if winner == team.name:
                        total += 3

            # ✅ KO scoring
            elif m.stage == "KO":
                if (m.home_score > m.away_score and m.home_team == team.name) or \
                   (m.away_score > m.home_score and m.away_team == team.name):
                    total += 5

            # ✅ FINAL
            elif m.stage == "FINAL":
                if (m.home_score > m.away_score and m.home_team == team.name) or \
                   (m.away_score > m.home_score and m.away_team == team.name):
                    total += 17.5

    return total

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                email=request.POST["email"],
                password=request.POST["password1"]
            )

            login(request, user)
            return redirect("/rules")

    return render(request, "signup.html")


@login_required
def pickems_view(request):
    if not request.user.profile.rules_seen:
        return redirect("/rules")

    # normal logic here
    return render(request, "pickems.html")

@login_required
def game_rules(request):
    if request.method == "POST":
        return redirect("/pickems")

    return render(request, "rules.html")

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def pickems_view(request):
    teams = Team.objects.all().order_by("group")

    grouped = defaultdict(list)
    for t in teams:
        grouped[t.group].append(t)

    if request.method == "POST":
        data = request.POST

        Pickems.objects.update_or_create(
            user=request.user,
            defaults={
                "group_A": Team.objects.get(id=data.get("A")),
                "group_B": Team.objects.get(id=data.get("B")),
                "group_C": Team.objects.get(id=data.get("C")),
                "group_D": Team.objects.get(id=data.get("D")),
                "group_E": Team.objects.get(id=data.get("E")),
                "group_F": Team.objects.get(id=data.get("F")),
                "group_G": Team.objects.get(id=data.get("G")),
                "group_H": Team.objects.get(id=data.get("H")),
                "group_I": Team.objects.get(id=data.get("I")),
                "group_J": Team.objects.get(id=data.get("J")),
                "group_K": Team.objects.get(id=data.get("K")),
                "group_L": Team.objects.get(id=data.get("L")),
            }
        )

        return redirect("/home")

    return render(request, "pickems.html", {"groups": dict(grouped)})

@login_required
def leaderboard_view(request):
    users = User.objects.all()

    data = []
    for u in users:
        try:
            score = calculate_points(u)
            data.append({
                "id": u.id,
                "user": u.username,
                "points": score
            })
        except:
            continue

    data.sort(key=lambda x: x["points"], reverse=True)
    return render(request, "leaderboard.html", {"data": data})


@login_required
def home_view(request):
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    
    matches = Match.objects.filter(
        date__date__in=[yesterday, today, tomorrow]
    ).order_by("date")

    return render(request, "home.html", {
        "matches": matches
    })

@login_required
def point_table_view(request):

    groups = {g: list(Team.objects.filter(group=g)) for g in "ABCDEFGHIJKL"}
    group_stats = {}

    for g, teams in groups.items():
        stats = []

        for team in teams:
            stats.append({
                "team": team,
                "played": 0,
                "won": 0,
                "lost": 0,
                "draw": 0,
                "points": 0
            })

        group_stats[g] = stats

    matches = Match.objects.filter(stage="GROUP")

    for g, stats in group_stats.items():
        for team_stat in stats:
            name = team_stat["team"].name

            for m in matches:
                t1 = m.home_team
                t2 = m.away_team
                s1 = m.home_score
                s2 = m.away_score

                if s1 is None or s2 is None:
                    continue

                if name not in [t1, t2]:
                    continue

                team_stat["played"] += 1

                if s1 == s2:
                    team_stat["draw"] += 1
                    team_stat["points"] += 1
                else:
                    winner = t1 if s1 > s2 else t2

                    if winner == name:
                        team_stat["won"] += 1
                        team_stat["points"] += 2
                    else:
                        team_stat["lost"] += 1

        stats.sort(key=lambda x: x["points"], reverse=True)

    return render(request, "pointtable.html", {
        "groups": group_stats
    })

@login_required
def your_pickems(request):
    try:
        picks = Pickems.objects.get(user=request.user)
    except Pickems.DoesNotExist:
        picks = None

    total = 0
    if picks:
        total = calculate_points(request.user)

    return render(request, "yourpicks.html", {
        "picks": picks,
        "total": total
    })


def matches_view(request):
    matches = Match.objects.all().order_by("id")
    for m in matches:
        m.home_code = TEAM_CODES.get(m.home_team, "UNK")
        m.away_code = TEAM_CODES.get(m.away_team, "UNK")

    return render(request, "matches.html", {
        "matches": matches
    })

@login_required
def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if request.method == "POST":
        Comment.objects.create(
            match=match,
            user=request.user,
            text=request.POST.get("text")
        )
        return redirect(f"/matches/{match_id}/")

    comments = Comment.objects.filter(match=match).order_by("-created_at")

    # ✅ HTMX request → return ONLY comments
    if request.headers.get("HX-Request"):
        return render(request, "_comments.html", {
            "comments": comments
        })

    # ✅ collect user picks relevant to this match
    picks_data = []

    users = User.objects.all()

    for u in users:
        try:
            p = Pickems.objects.get(user=u)
        except Pickems.DoesNotExist:
            continue

        picked_team = None

        # ✅ check if user picked one of the teams in THIS match
        for team in [
            p.group_A, p.group_B, p.group_C, p.group_D,
            p.group_E, p.group_F, p.group_G, p.group_H,
            p.group_I, p.group_J, p.group_K, p.group_L,
        ]:
            if team.name in [match.home_team, match.away_team]:
                picked_team = team.name
                break

        if picked_team:
            picks_data.append({
                "user": u.username,
                "team": picked_team
            })

    return render(request, "match_detail.html", {
        "match": match,
        "comments": comments,
        "picks_data": picks_data
    })


@login_required
def user_pickems(request, user_id):
    user = User.objects.get(id=user_id)

    try:
        picks = Pickems.objects.get(user=user)
    except Pickems.DoesNotExist:
        picks = None

    total = 0
    if picks:
        total = calculate_points(user)

    return render(request, "yourpicks.html", {
        "picks": picks,
        "total": total,
        "view_user": user.username   # ✅ who we are viewing
    })

def bracket_view(request):
    matches = Match.objects.all()

    bracket = {
        "R32": matches.filter(stage="KNOCKOUT-R32"),
        "R16": matches.filter(stage="KNOCKOUT-R16"),
        "QF": matches.filter(stage="Quater-Final"),
        "SF": matches.filter(stage="Semi-Final"),
        "BF" : matches.filter(stage="Bronze-Final"),
        "FF": matches.filter(stage="Final"),
    }

    return render(request, "bracket.html", {
        "bracket": bracket
    })
