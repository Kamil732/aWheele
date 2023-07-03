from django.shortcuts import render

def handler404(request, *args, **kwargs):
    template_name = 'errors/404.html'
    return render(request, template_name, status=404)

def handler500(request, *args, **kwargs):
    template_name = 'errors/500.html'
    return render(request, template_name, status=500)