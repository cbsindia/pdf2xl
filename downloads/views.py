import os
from django.conf import settings
from django.http import HttpResponse, Http404

def download(request,in_file):
    filename = os.path.splitext(os.path.basename(in_file))[0] + '.xlsx'
    if request.method == 'GET':
        file_path = os.path.join(settings.MEDIA_ROOT,'xlsx', filename)
        print(file_path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404