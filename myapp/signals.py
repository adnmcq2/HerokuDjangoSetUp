from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from django.core.signals import request_finished
from django.dispatch import receiver

import logging

from .models import *

# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

logger = logging.getLogger(__name__)

from django.conf import settings

#https://docs.djangoproject.com/en/3.1/topics/signals/

@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.
        try:
            my_pk = ipn_obj.invoice
            mytransaction = MyTransaction.objects.get(pk=my_pk)
            assert ipn_obj.mc_gross == mytransaction.amount and ipn_obj.mc_currency == 'EUR'
        except Exception:
            logger.exception('Paypal ipn_obj data not valid!')
        else:
            mytransaction.paid = True
            mytransaction.save()
    else:
        logger.debug('Paypal payment status not completed: %s' % ipn_obj.payment_status)