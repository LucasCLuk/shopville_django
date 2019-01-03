from django.http import HttpRequest
from django.urls import reverse


class NavigationItem:

    def __init__(self, request: HttpRequest, display_name: str, url_name: str = None, name_space: str = "shopville",
                 admin: bool = False):
        self.name = display_name  # The name displayed on the navbar
        self.href = reverse(f"{name_space}:{url_name or display_name.lower()}")  # the django url
        self.active = request.path == self.href  # if it should have the active class
        self.admin = admin  # requires is_staff permissions


def dashboard_navigation_processor(request: HttpRequest) -> dict:
    return {
        "navbar": [
            # NavigationItem(request, "Dashboard"),
            # NavigationItem(request, "Accounting"),
            # NavigationItem(request, "Control Panel", "control-panel", admin=True),
            NavigationItem(request, "Manager", "task-manager", admin=True)
        ]
    }
