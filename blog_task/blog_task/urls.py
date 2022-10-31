from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('auth/', include('account.urls')),
]

# in development django built-in server serves static and media content
if not settings.PROD:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )


admin.site.site_header = "MPM Admin"
admin.site.site_title = "MPM Administration"
admin.site.index_title = "MPM Administration"