from django.forms import ModelForm
from .models import MenuItem, Reservation

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        
