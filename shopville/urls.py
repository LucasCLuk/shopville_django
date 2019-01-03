from django.urls import path

from shopville import views as ice_views

app_name = "shopville"

urlpatterns = [
    # path("", ice_views.Dashboard.as_view(), name="dashboard"),
    path("", ice_views.Accounting.as_view(), name="accounting"),
    path("tasks",ice_views.TaskManager.as_view(),name="task-manager")
]
