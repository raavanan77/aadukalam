from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import Pickems

class PickLockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path == "/pickems/" and request.method == "POST":
                if Pickems.objects.filter(user=request.user).exists():
                    return redirect("/pickems/")

        return self.get_response(request)

class AuthSafetyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        public_paths = ["/login", "/signup", "/admin"]

        if any(request.path.startswith(p) for p in public_paths):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect("/login")

        try:
            response = self.get_response(request)
            return response

        except Exception:
            logout(request)
            return redirect("/login")
