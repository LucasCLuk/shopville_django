from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from rest_api.views import *

app_name = "rest_api"

router = routers.DefaultRouter()
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include((router.urls, "rest_api"))),
    path("buyers/", BuyerListView.as_view(), name="get-buyers"),
    path("buyers/<int:buyer>/performance", BuyerSummaryViewSet.as_view(), name="buyer-week-graph"),
    path("buyers/<int:buyer>/items", BuyerItemListViewSet.as_view(), name="buyer-items"),
    path("buyers/<int:buyer>/orders", OrderListViewSet.as_view(), name="buyer-orders"),
    path("buyers/<int:buyer>/process", ProcessTaskView.as_view(), name="processs-buyer-email"),
    path("items/", ItemListViewSet.as_view(), name="items"),
    path("auth-token/", views.obtain_auth_token),
]
