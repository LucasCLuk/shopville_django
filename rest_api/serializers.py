from rest_framework import serializers
from rest_framework.fields import CharField, DateTimeField

from shopville.models import Item, Order, Buyer


class ItemSerializer(serializers.ModelSerializer):
    purchased = CharField(source="order.purchased", read_only=True)
    store = CharField(source="order.get_store_display", read_only=True)
    discount = CharField(source="order.discount", read_only=True)

    class Meta:
        model = Item
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    store_name = CharField(source="get_store_display", read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class BuyerSerializer(serializers.ModelSerializer):
    last_scan = DateTimeField(source="last_successful_scan", format="%c", read_only=True)
    next_scan = DateTimeField(source="next_scheduled_scan", format="%c", read_only=True)
    last_successful = DateTimeField(source="last_successful_scan", format="%c", read_only=True)

    class Meta:
        model = Buyer
        fields = "__all__"
