from django.shortcuts import render

from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.http import JsonResponse

#from PIL import Image
import cv2
import numpy as np

# Create your views here.

def carga_imagen(request):
    if request.method == 'POST' and request.FILES['imagen']:

        # Elimina la imagen anterior
        #ruta_imagen_anterior = os.path.join(settings.MEDIA_ROOT, 'imagen01.jpg')
        ruta_imagen_anterior = os.path.join(settings.STATIC_ROOT,'images','imagenes','imagen01.jpg')
        if os.path.exists(ruta_imagen_anterior):
            os.remove(ruta_imagen_anterior)

        # Guarda la nueva imagen
        imagen = request.FILES['imagen']
        imagen_bytes = imagen.read()

        # Transforma la imagen a formato RGB
        imagen_numpy = cv2.imdecode(np.frombuffer(imagen_bytes, np.uint8), cv2.IMREAD_UNCHANGED)
        imagen_rgb = cv2.cvtColor(imagen_numpy, cv2.COLOR_BGR2RGB)

        #Guardar la imagen RGB
        #ruta_imagen_nueva = os.path.join(settings.MEDIA_ROOT, 'imagen_rgb.jpg')
        ruta_imagen_nueva = os.path.join(settings.IMG_ROOT,'imagen_rgb.jpg')
        with open(ruta_imagen_nueva, 'wb+') as archivo:
            archivo.write(cv2.imencode('.jpg', imagen_rgb)[1])

        #Guardar la imagen BGR
        #ruta_imagen_nueva = os.path.join(settings.MEDIA_ROOT, 'imagen_bgr.jpg')
        ruta_imagen_nueva = os.path.join(settings.IMG_ROOT, 'imagen_bgr.jpg')
        with open(ruta_imagen_nueva, 'wb+') as archivo:
            for chunk in imagen.chunks():
                archivo.write(chunk)

        # Devuelve la respuesta en formato JSON
        return JsonResponse({'status': 'success'})

    return render(request, 'carga_imagen.html')


from django.http import HttpResponse
import subprocess
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def segmentar_imagen(request):
    if request.method == 'POST':
        # Carga el cuaderno en memoria
        ruta_notebook = os.path.join(settings.NOTE_ROOT, 'samtest.ipynb')
        #with open('websam/notebooks/samtest.ipynb', 'r') as f:
        with open(ruta_notebook, 'r') as f:
            nb = nbformat.read(f, as_version=4)

        #Uso en AWS
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

        # Se crea un preprocesador de ejecución Local
        #ep = ExecutePreprocessor(timeout=600, kernel_name='PythonDjango')

        # Se ejecuta el cuaderno
        try:
            ep.preprocess(nb, {'metadata': {'path': './'}})
        except Exception as e:
            # Maneja cualquier excepción que ocurra durante la ejecución
            return HttpResponse('Error durante la ejecución del cuaderno: {}'.format(str(e)))
        
        # Devuelve una respuesta satisfactoria
        return HttpResponse('Cuaderno ejecutado con éxito')
    else:
        return render(request, 'carga_imagen.html')
    
from django.shortcuts import redirect    
from django.http import HttpResponseRedirect
from django.urls import reverse

def segmentar_binario(request):

    if request.method == 'POST':
        # Carga el cuaderno en memoria
        ruta_notebook = os.path.join(settings.NOTE_ROOT, 'sambinario.ipynb')
        #with open('websam/notebooks/samtest.ipynb', 'r') as f:
        with open(ruta_notebook, 'r') as f:
            nb = nbformat.read(f, as_version=4)

        #Uso en AWS
        #ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

        #Se crea un preprocesador de ejecución Local
        ep = ExecutePreprocessor(timeout=600, kernel_name='PythonDjango')

        # Se ejecuta el cuaderno
        try:
            ep.preprocess(nb, {'metadata': {'path': './'}})
            mensaje_exito = 'Cuaderno binario ejecutado con éxito'
            return HttpResponseRedirect(reverse('output_csv') + '?mensaje=' + mensaje_exito)         
        except Exception as e:
            # Maneja cualquier excepción que ocurra durante la ejecución
            return HttpResponse('Error durante la ejecución del cuaderno: {}'.format(str(e)))
        
        # Devuelve una respuesta satisfactoria
        # return HttpResponse('Cuaderno binario ejecutado con éxito')
    else:
        return render(request, 'carga_imagen.html')

def segmentar_json(request):  

    if request.method == 'POST':
        # Carga el cuaderno en memoria
        ruta_notebook = os.path.join(settings.NOTE_ROOT, 'samjson.ipynb')
        #with open('websam/notebooks/samtest.ipynb', 'r') as f:
        with open(ruta_notebook, 'r') as f:
            nb = nbformat.read(f, as_version=4)

        #Uso en AWS
        #ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

        #Se crea un preprocesador de ejecución Local
        ep = ExecutePreprocessor(timeout=600, kernel_name='PythonDjango')

        # Se ejecuta el cuaderno
        try:
            ep.preprocess(nb, {'metadata': {'path': './'}})
            mensaje_exito = 'Cuaderno JSON ejecutado con éxito'
            return HttpResponseRedirect(reverse('output_json') + '?mensaje=' + mensaje_exito)                
        except Exception as e:
            # Maneja cualquier excepción que ocurra durante la ejecución
            return HttpResponse('Error durante la ejecución del cuaderno: {}'.format(str(e)))
        
        # Devuelve una respuesta satisfactoria
        #return HttpResponse('Cuaderno JSON ejecutado con éxito')
    else:
        return render(request, 'carga_imagen.html')

def ver_imagen_segmentada(request):

    if request.method == 'POST':
    
        img_segmentada = os.path.join(settings.STATIC_ROOT,'images' ,'img-segmentada','imagen_segmentada.png')
        #img_segmentada = "C:/Users/piped/OneDrive/Escritorio/Pruebas3/websitesam/websam/img-segmentada/imagen_segmentada.png"
        img_original = os.path.join(settings.STATIC_ROOT,'images' ,'imagenes','imagen_bgr.jpg')

        return render(request, 'carga_imagen.html',{'img_original':img_original,'img_segmentada':img_segmentada })

    #return HttpResponse(imagen_segmentada, content_type='image/png')
    return render(request, 'carga_imagen.html')

from django.contrib.staticfiles.views import serve as serve_static
#from django.http import FileResponse

def csv_view(request):

    csv_path = os.path.join(settings.CSV_ROOT, 'metadata.csv')

    # Abre el archivo CSV en modo binario
    with open(csv_path, 'rb') as csv_file:
        response = HttpResponse(csv_file, content_type='text/csv')
        response['Content-Disposition'] = 'inline; filename="data.csv"'

    # Devuelve una respuesta HTTP con el contenido del archivo CSV
    return response

import json

def json_view(request):
    # Ruta al archivo JSON
    json_path = os.path.join(settings.JSON_ROOT, 'segmentacion_json.json')

    # contenido del archivo JSON
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)
        

    # # Pasa los datos JSON a la plantilla para mostrarlos
    return render(request, 'vista_json.html', {'json_data': json_data})


def output_csv(request):
    mensaje = request.GET.get('mensaje', '')
    return render(request, 'output_csv.html', {'mensaje': mensaje})

def output_json(request):
    mensaje = request.GET.get('mensaje', '')
    return render(request, 'output_json.html', {'mensaje': mensaje})