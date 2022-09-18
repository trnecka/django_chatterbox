from django.forms import ModelForm

from base.models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        # zobrazi všechny pole které nejsou automatizované  (nedají se změnit)
        fields = '__all__'
        # tyto sloupečky se nezobrazí
        exclude = ['participants']