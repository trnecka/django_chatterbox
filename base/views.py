from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView

from base.forms import RoomForm
from base.models import Room, Message


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

    # na instanci mistnosti chci zobrazit zpravy (je to v podstate druhy select
    messages = room.message_set.all()

    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            body=request.POST.get('body'),
            room=room
        )
        room.participants.add(request.user)
        return redirect('room', id=room.id)
    context = {'room': room, 'messages': messages}
    return render(request, 'base/room.html', context)

class RoomCreateView(CreateView):
    template_name = 'base/room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('rooms')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add new room'
        return context

    # def form_valid(self, form):
    #     result = super().form_valid(form) # vrati vysledky formulare zvalidovane
    #     cleaned_data = form.cleaned_data
    #     Room.objects.create(
    #         name=cleaned_data['name'],
    #         description=cleaned_data['description'],
    #     )
    #     return result

    def form_invalid(self, form):
        return super().form_invalid(form)

class RoomUpdateView(UpdateView):
    template_name = 'base/room_form.html'
    model = Room
    form_class = RoomForm
    success_url = reverse_lazy('rooms')

    def form_invalid(self, form):
        return super().form_invalid(form)

# def room_create(request):
#     form = RoomForm()
#     context = {'form': form}
#     if request.method == 'POST':
#         form_filled = RoomForm(request.POST)
#         if form_filled.is_valid():
#             form_filled.save()
#             return redirect('rooms')
#     return render(request, 'base/room_form.html', context)

class RoomDeleteView(DeleteView):
    template_name = 'base/room_confirm_delete.html'
    model = Room
    success_url = reverse_lazy('rooms')

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