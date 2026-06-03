from django.db import models
from django.contrib.auth.models import User

STAGE_CHOICES = {
    ("GR","Group"),
    ("KO","Knock Out"),
    ("QF","Quatr Final"),
    ("SF","Semi Final",),
    ("TP", "Third Place"),
    ("FF","Final")
}

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=1)
    code = models.CharField(max_length=3)

class Match(models.Model):
    match_id = models.IntegerField(unique=True)

    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)

    date = models.DateTimeField()
    stage = models.CharField(max_length=20)

    status = models.CharField(max_length=20)

    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)

    winner = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"

class Pickems(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group_A = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pick_A')
    group_B = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pick_B')
    group_C = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pick_C')
    group_D = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pick_D')
    group_E = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pick_E')
    group_F = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pick_F')
    group_G = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pick_G')
    group_H = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pick_H')
    group_I = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pick_I')
    group_J = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pick_J')
    group_K = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pick_K')
    group_L = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pick_L')

class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.FloatField(default=0)

class Comment(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
