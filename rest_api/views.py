import datetime

from django.db.models import Sum, QuerySet
from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from rest_api.permissions import BuyerViewPermission
from rest_api.serializers import ItemSerializer, OrderSerializer, BuyerSerializer
from rest_api.tasks import email_processor
from shopville.models import Item, Stores, Order, Buyer


# Create your views here.


class ItemListViewSet(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        buyer = self.request.query_params.get("buyer")
        purchased_from = self.request.query_params.get("purchased_from")
        purchased_to = self.request.query_params.get("purchased_to")
        if all([buyer, purchased_from, purchased_to]):
            return self.queryset.filter(order__buyer_id=buyer, order__purchased__range=(purchased_from, purchased_to))
        else:
            return self.queryset.none()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class BuyerListView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer


class BuyerItemListViewSet(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = (BuyerViewPermission,)

    def get_queryset(self):
        purchased_from = self.request.query_params.get("purchased_from")
        purchased_to = self.request.query_params.get("purchased_to")
        if all([purchased_to, purchased_from]):
            response = Item.objects.filter(order__buyer=self.kwargs['buyer'],
                                           order__purchased__range=(purchased_from, purchased_to))
        else:
            response = Item.objects.filter(order__buyer=self.kwargs['buyer'])
        return response


class OrderListViewSet(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (BuyerViewPermission,)

    def get_queryset(self):
        purchased_from = self.request.query_params.get("purchased_from")
        purchased_to = self.request.query_params.get("purchased_to")
        if all([purchased_to, purchased_from]):
            response = Order.objects.filter(buyer=self.kwargs['buyer'],
                                            purchased__range=(purchased_from, purchased_to))
        else:
            response = Order.objects.filter(buyer=self.kwargs['buyer'])
        return response


class BuyerSummaryViewSet(generics.RetrieveAPIView):
    permission_classes = (BuyerViewPermission,)

    def get_queryset(self) -> QuerySet:
        return Item.objects.filter(order__buyer=self.request.user)

    def get(self, request, *args, **kwargs):
        response = {
            "labels": [],
            "data": {store.name: [] for store in Stores},
            "total": []
        }
        now = timezone.now().date()
        for x in range(7, 0, -1):
            day = now - datetime.timedelta(days=x)
            day_midnight = datetime.datetime(now.year, now.month, day.day)
            day_end = day_midnight.replace(hour=23, minute=59, second=59)
            label = day_midnight.strftime("%x")
            response['labels'].append(label)
            total_spent = 0.00
            for store in Stores:
                store_summary = Item.objects.filter(order__buyer=self.kwargs['buyer'],
                                                    order__purchased__range=(day_midnight, day_end),
                                                    order__store=store.value).aggregate(
                    total_spent=Sum("unit_price"))
                spendings = store_summary['total_spent']
                if spendings is None:
                    spendings = 0.00
                total_spent += float(spendings)
                response['data'][store.name].append(spendings)
            response['total'].append(total_spent)

        return Response(response)


class ProcessTaskView(generics.RetrieveAPIView):
    permission_classes = (BuyerViewPermission,)

    def get(self, request, *args, **kwargs):
        email_processor(kwargs.get("buyer"))
        return Response(status=200)
