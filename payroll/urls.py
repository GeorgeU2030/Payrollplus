

from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", TemplateView.as_view(template_name="initscreen.html"), name="initscreen"),
    path('admin/', admin.site.urls),
    path("authentication/", include("authentication.urls")),
    path("authentication/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)