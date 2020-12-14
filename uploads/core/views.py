from django.shortcuts import render, redirect
from django.conf import settings
from django.apps import apps
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
import os
import time

from pdf2xl import *
from uploads.core.models import Document
from uploads.core.forms import DocumentForm


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })


def pdf2xl(in_file):
    fs = FileSystemStorage()
    in_file_with_path = os.path.join(fs.base_location,in_file)
    script_path = os.path.join(apps.get_app_config('pdf2xl').path,'jtoxl.py')
    cmd = 'python {} {}'.format(script_path,in_file_with_path)
    print(cmd)
    os.system(cmd)


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:

        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        down_path = os.path.join('download')
        tran_id = get_random_string(6)
        myfile.name = '{}-{}'.format(tran_id,myfile.name)
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        in_file_without_ext = os.path.splitext(os.path.basename(myfile.name))[0]
        download_file = os.path.join(down_path, '{}.xlsx'.format(in_file_without_ext))

        pdf2xl(filename)
        print(type(fs.url(download_file)))
        print(os.path.relpath(fs.url(download_file), '/media'))


        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url, 'down_filename' : os.path.relpath(fs.url(download_file), '/media')
        })
    return render(request, 'core/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
