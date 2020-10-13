from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .forms import ImageForm
from .image_processing import process_image, process_base64


def index(request):
    if request.method == 'GET':
        form = ImageForm()
        ctx = {'form': form}
        return render(request, 'index.html', ctx)
    elif request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = process_image(form.files['img'])
            return render(request, 'result.html', {'image': image})
    
    return HttpResponse(status=400)


@require_POST
def base64_image(request):
    b64 = request.POST['imgBase64'].split(',', maxsplit=1)[-1]
    image = process_base64(b64)
    return render(request, 'result.html', {'image': image})
