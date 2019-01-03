import email_scrapper
from background_task import background
from django.conf import settings
from django.utils import timezone
from email_scrapper.models import Stores

from shopville.models import Buyer, Order, Item, StoreEmailLocation, Email


@background(schedule=1)
def process_email_task(user_id: int, refresh: bool = True):
    email_processor(user_id,refresh)


def email_processor(user_id: int, refresh: bool = False):
    buyer = Buyer.objects.get(pk=user_id)
    buyer.currently_scanning = True
    buyer.last_scanned = timezone.now()
    buyer.save()
    try:
        email = Email.objects.get(email_address=buyer.email)
        credentials = (email.email_address, email.password)
    except Email.DoesNotExist:
        credentials = (settings.MASTER_EMAIL,
                       settings.MASTER_PASSWORD,)
    store_locations = list(StoreEmailLocation.objects.filter(buyer=buyer))
    locations = {Stores(int(store.store)): store.location for store in store_locations}
    search_date = (timezone.datetime.now() - timezone.timedelta(days=7))
    if buyer:
        try:
            reader = email_scrapper.Reader(*credentials, locations=locations, date_from=search_date)
            reader_data = reader.run()
            for _ in reader_data:
                order_data = dict(_)
                cart = order_data.pop("cart")
                order_data['buyer'] = buyer
                try:
                    order = Order(**order_data)
                    order.save()
                except:
                    continue
                for item in cart:
                    item['order'] = order
                    try:
                        new_item = Item(**item)
                        new_item.save()
                    except:
                        continue
            buyer.currently_scanning = False
            buyer.last_successful_scan = timezone.now()
            buyer.save()
        except Exception as e:
            print(e)
        finally:
            if refresh:
                buyer.next_scheduled_scan = timezone.now() + timezone.timedelta(days=7)
                buyer.save()
