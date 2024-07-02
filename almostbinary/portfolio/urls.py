from django.urls import re_path
from . import views

app_name = "portfolio"

urlpatterns = [
    re_path(r"^cv/$", views.cv, name='cv'),
    re_path(r"^about/$", views.about, name='about'),
]