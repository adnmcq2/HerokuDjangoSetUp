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

from .forms import NewUserForm


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