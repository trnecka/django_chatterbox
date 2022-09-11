from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse

from base.models import Room


# Create your views here.
def hello(request):
    s = request.GET.get('s', '')
    return HttpResponse(f'Hello, {s} world!')

def search(request):
    q = request.GET.get('q', '')
    if q == '':
        return HttpResponse("Prosím zadejte hledaný výraz.")

    # vyhledava jak v popisku tak v description
    rooms = Room.objects.filter(
        Q(description__contains=q) |
        Q(name__contains=q)
    )

    context = {'q': q, 'rooms': rooms}
    return render(request, 'base/search.html', context)