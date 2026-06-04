from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('home/', views.home_view, name='home'),
    path('pointtable/', views.point_table_view, name='pointtable'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup_view, name="signup"),
    path('rules/', views.game_rules, name="rules"),
    path('pickems/', views.pickems_view, name="pickems"),
    path('yourpicks/', views.your_pickems, name="yourpickems"),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path("matches/", views.matches_view),
    path("user/<int:user_id>/", views.user_pickems),
    path("matches/<int:match_id>/", views.match_detail),
    path("playoff/", views.bracket_view),
]