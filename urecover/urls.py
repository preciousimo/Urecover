from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Custom URLs
    path("user/", include("userauths.urls")),
    path('', include('base.urls')),
    
    # CKEditor
    path("ckeditor5/", include("django_ckeditor_5.urls"), name="ck_editor_5_upload_file")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)