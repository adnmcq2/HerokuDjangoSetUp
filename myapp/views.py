from django.shortcuts import render, redirect


from django.contrib.auth import logout, login

from .models import *
from django.conf import settings


# import os, csv, json, re
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# import urllib3
# import textwrap

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from .forms import *

from django.views.generic import FormView
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from django.views.generic import TemplateView

import logging, os

# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

logger = logging.getLogger(__name__)

from django.views.decorators.csrf import csrf_exempt


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {}
    return render(request, 'myapp/index.html', context)

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # messages.success(request, "Registration successful." )
            return redirect("myapp:index")
        # messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="registration/register.html", context={"register_form":form})




class OrderListJson(BaseDatatableView):
    #address, data_deletes, data_opt_outs, delete_instructions, email, id, name, opt_out, opt_out_instructions, other_instructions, site

    order_columns = ['name', 'site', 'email','opt_out_instructions','delete_instructions',
                     'other_instructions', 'address']

    def get_initial_queryset(self):
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        return DataBroker.objects.all()#filter(something=self.kwargs['something'])

    def filter_queryset(self, qs):
        # use request parameters to filter queryset

        # simple example:
        # search = self.request.GET.get('search[value]', None)
        # if search:
        #     qs = qs.filter(name__istartswith=search)
        #
        # # more advanced example
        # filter_customer = self.request.GET.get('customer', None)
        #
        # if filter_customer:
        #     customer_parts = filter_customer.split(' ')
        #     qs_params = None
        #     for part in customer_parts:
        #         q = Q(customer_firstname__istartswith=part)|Q(customer_lastname__istartswith=part)
        #         qs_params = qs_params | q if qs_params else q
        #     qs = qs.filter(qs_params)
        return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append([
                # escape(item.number),  # escape HTML for security reasons
                # escape("{0} {1}".format(item.customer_firstname, item.customer_lastname)),  # escape HTML for security reasons
                # item.get_state_display(),
                # item.created.strftime("%Y-%m-%d %H:%M:%S"),
                # item.modified.strftime("%Y-%m-%d %H:%M:%S")
                escape(item.name),
                '<a href ="%s" >%s</a>'%(item.site, item.site),
                escape(item.email),
                escape(item.opt_out_instructions),
                escape(item.delete_instructions),
                escape(item.other_instructions),
                escape(item.address)
            ])
        return json_data


def profile(request):


    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    context={'user':request.user}
    return render(request, 'myapp/profile.html', context)

def logout_view(request):
    logout(request)
    # Redirect to a success page.



#https://www.guguweb.com/2021/01/12/how-to-accept-paypal-payments-on-your-django-application/
#https://django-paypal.readthedocs.io/en/stable/standard/ipn.html


# class PaypalFormView(FormView):
#     template_name = 'paypal/paypal_form.html'
#     form_class = PayPalPaymentsForm
#
#     def get_initial(self):
#         return {
#             "business": settings.PAYPAL_RECEIVER_EMAIL,
#             "amount": 0.01,
#             "currency_code": "USD",
#             "item_name": 'Example item',
#             "invoice": 1234,
#             "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
#             "return_url": self.request.build_absolute_uri(reverse('paypal-return')),
#             "cancel_return": self.request.build_absolute_uri(reverse('paypal-cancel')),
#             "lc": 'EN',
#             "no_shipping": '1',
#         }

def order_create(request):
    form = OrderCreateForm()

    if request.method == 'POST':

        return redirect(reverse('myapp:process'))

    return render(request, 'myapp/order_create.html', {'form': form})  #this really should be different from myapp/process


def payment_process(request):
    host = request.get_host()

    paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": 0.01,
            "currency_code": "USD",
            "item_name": 'Example item',
            "invoice": 1234,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),#'https://%s/%s'%(host, reverse('paypal-ipn')),
            "return_url": request.build_absolute_uri(reverse('myapp:done')),
            "cancel_return": request.build_absolute_uri(reverse('myapp:canceled')),#'https://%s/%s'%(host, reverse('paypal-cancel')), #self.request.build_absolute_uri(reverse('paypal-cancel')),
            "lc": 'EN',
            "no_shipping": '1',
        }

    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'myapp/process.html', {'form':form})


@csrf_exempt
def payment_done(request):
    return render(request, 'myapp/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'myapp/payment_canceled.html')


# @csrf_exempt
# class PaypalCancelView(TemplateView):
#     template_name = 'paypal/paypal_cancel.html'


