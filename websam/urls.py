from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.carga_imagen, name='carga_imagen'),
    path('segmentar_imagen/', views.segmentar_imagen, name='segmentar_imagen'),
    path('segmentar_binario/', views.segmentar_binario, name='segmentar_binario'),
    path('segmentar_json/', views.segmentar_json, name='segmentar_json'),
    path('ver_imagen_segmentada/', views.ver_imagen_segmentada, name='ver_imagen_segmentada'),
    path('csv-view/', views.csv_view, name='csv-view'),
    path('vista_json/', views.json_view, name='vista_json'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)