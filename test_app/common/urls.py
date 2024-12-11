from django.urls import path

from test_app.common import views
from test_app.common.views import HomeView

urlpatterns = [
    path('', HomeView, name='home'),
]