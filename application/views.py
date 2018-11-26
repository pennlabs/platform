from django.shortcuts import render

def splash(request):
    return render(request, 'splash.html')