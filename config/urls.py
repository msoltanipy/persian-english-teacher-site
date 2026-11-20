from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

admin.site.site_header = "پنل مدیریت وب‌سایت آموزش زبان انگلیسی"
admin.site.site_title = "مدیریت سایت"
admin.site.index_title = "خوش آمدید"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("academy.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
