from django.shortcuts import render


def index(request):
    return render(request, 'evaluation/index.html', {'name': 'Dolokelen'})