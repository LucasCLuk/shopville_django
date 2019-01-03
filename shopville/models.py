# Create your models here.
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from email_scrapper.models import Stores


class Buyer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    purchased_date = models.DateField(name="purchased")
    store = models.CharField(max_length=2, choices=[(store.value, store.name) for store in Stores])
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    tracking = models.URLField(null=True)
    shipped = models.BooleanField(default=False, null=True)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True)

    def get_store_display(self):
        store = self.store
        return Stores(int(store)).name


class Item(models.Model):
    name = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(default=1)
    item_page = models.URLField(null=True)

    class Meta:
        unique_together = ("name", "order")


class StoreEmailLocation(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    store = models.CharField(max_length=2, choices=[(str(store.value), store.name) for store in Stores])
    location = models.CharField(max_length=120)

    class Meta:
        unique_together = ("buyer", "store")

    def __str__(self):
        return f"<{self.buyer}> - <{self.store}> - <{self.location}>"


class Email(models.Model):
    email_address = models.EmailField(primary_key=True)
    password = models.CharField(max_length=120)


class BuyerSchedule(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    last_scanned = models.DateTimeField(null=True, blank=True)
    currently_scanning = models.BooleanField(default=False)
    last_successful_scan = models.DateTimeField(null=True, blank=True)
    next_scheduled_scan = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.buyer.name

    @property
    def last_scan(self):
        return self.last_successful_scan.strftime("%c")

    @property
    def next_scan(self):
        return self.next_scheduled_scan.strftime("%c")

    @property
    def last_successful(self):
        return self.last_successful_scan.strftime("%c")
