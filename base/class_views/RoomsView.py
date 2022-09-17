from django.views.generic import ListView

from base.models import Room


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
