from django.conf.urls import url
from django.conf.urls.static import static
from findface import settings

from app.views import index, base64_image


urlpatterns = [
    url(r'^base64/$', base64_image, name='base64_image'),
    url(r'^$', index, name='index'),    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
