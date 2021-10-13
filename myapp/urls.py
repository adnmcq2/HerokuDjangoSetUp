
from django.urls import path

from . import views

from django.conf.urls import url

app_name = 'myapp'
urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:question_id>/', views.detail, name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path("register", views.register_request, name="register"),
    url(r'^my/datatable/data/$', views.OrderListJson.as_view(), name='order_list_json'),
    path("profile", views.profile, name="profile"),

]