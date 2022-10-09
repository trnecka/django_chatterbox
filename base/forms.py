from logging import getLogger

from django.core.exceptions import ValidationError
from django.forms import ModelForm

from base.models import Room

LOGGER = getLogger()

class RoomForm(ModelForm):

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            validation_error = ValidationError("Name must contain minimal 2 characters.")
            LOGGER.warning(f'Validation error: {validation_error}: {name}')
            raise validation_error
        if Room.objects.filter(name__iexact=name).exists():
            validation_error = ValidationError("Name already exists.")
            LOGGER.warning(f'Validation error: {validation_error}: {name}')
            raise validation_error

        return name

    class Meta:
        model = Room
        # zobrazi všechny pole které nejsou automatizované  (nedají se změnit)
        fields = '__all__'
        # tyto sloupečky se nezobrazí
        exclude = ['participants']