from django.contrib import admin
from django.urls import include, re_path

urlpatterns = [
    re_path(r"^admin/", admin.site.urls, name="admin"),
    re_path(r"^", include('blog.urls')),
    re_path(r"^", include('portfolio.urls')),
]
