from django.shortcuts import render

from .models import *


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {}
    return render(request, 'myapp/index.html', context)