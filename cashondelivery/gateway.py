from django.db import transaction
from cashondelivery import models


@transaction.atomic
def create_transaction(order_number, total, *args, **kwargs):
    txn = models.CashOnDeliveryTransaction.objects.get_or_create(
            order_number=order_number,
            amount=total.incl_tax,
            currency=total.currency
        )
    return txn[0].reference