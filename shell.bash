from banter.models import Team

groups = {
    "A": ["Mexico", "South Africa", "South Korea", "Czechia"],
    "B": ["Canada", "Bosnia-Herzegovina", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["United States", "Paraguay", "Australia", "Türkiye"],
    "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "Congo DR", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

TEAM_CODES = {
    "Mexico": "MEX",
    "South Africa": "RSA",
    "South Korea": "KOR",
    "Czechia": "CZE",
    "Canada": "CAN",
    "Bosnia-Herzegovina": "BIH",
    "Qatar": "QAT",
    "Switzerland": "SUI",
    "Brazil": "BRA",
    "Morocco": "MAR",
    "Haiti": "HAI",
    "Scotland": "SCO",
    "United States": "USA",
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
    "Iran": "IRN",
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
}

for group, teams in groups.items():
    for team in teams:
        Team.objects.create(
            name=team,
            group=group,
            code=TEAM_CODES.get(team, "UNK")
        )

import json
from datetime import datetime
from banter.models import Match

with open("fifa.json") as f:
    data = json.load(f)
    for match in data:
        stage = match.get("stage")
        for t in match.get("tournaments", []):
            match_id = t.get("id")
            date = t.get("date")
            date_obj = datetime.fromisoformat(date) if date else None
            Match.objects.update_or_create(
                match_id=match_id,
                defaults={
                    "home_team": t.get("homeSquadName"),
                    "away_team": t.get("awaySquadName"),
                    "date": date_obj,

                    "stage": stage,
                    "status": t.get("status"),

                    "home_score": t.get("homeScore"),
                    "away_score": t.get("awayScore"),

                    "winner": t.get("winner"),
                }
            )

Match.objects.count()