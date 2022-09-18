from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView

from base.forms import RoomForm
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

def room(request, id):
    room = Room.objects.get(id=id)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def room_create(request):
    form = RoomForm()
    context = {'form': form}
    if request.method == 'POST':
        form_filled = RoomForm(request.POST)
        if form_filled.is_valid():
            form_filled.save()
            return redirect('rooms')
    return render(request, 'base/room_form.html', context)


class RoomsView(ListView):
    template_name = 'base/rooms.html'
    model = Room
    '''
    # pokud dědím z TemplateView
    # v template je pak použitá proměnná rooms
    rooms = Room.objects.all()
    template_name = 'base/rooms.html'
    extra_context = {'rooms': rooms}

    '''