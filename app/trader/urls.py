
from django.urls import path

from trader.views import IndexView


app_name = 'currency'

urlpatterns = [
    path('index/', IndexView.as_view()),
]
