from django.contrib import admin

# Register your models here.
from shopville.models import *

admin.site.register(Buyer)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(StoreEmailLocation)
admin.site.register(Email)
