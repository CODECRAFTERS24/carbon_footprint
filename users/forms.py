from django import forms
from .models import TransportTicket

class TransportTicketForm(forms.ModelForm):
    """Form for users to upload transport tickets"""
    class Meta:
        model = TransportTicket
        fields = ['transport_type', 'distance_traveled', 'ticket_image']
        widgets = {
            'transport_type': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'distance_traveled': forms.NumberInput(attrs={
                'class': 'w-full p-2 border rounded', 
                'step': '0.1', 
                'placeholder': 'Distance in kilometers'
            }),
            'ticket_image': forms.FileInput(attrs={'class': 'w-full p-2 border rounded'})
        }

    def clean_distance_traveled(self):
        """Validate distance is positive"""
        distance = self.cleaned_data.get('distance_traveled')
        if distance <= 0:
            raise forms.ValidationError("Distance must be greater than zero")
        return distance

    def calculate_co2_saved(self):
        """
        Estimate CO2 saved based on transport type and distance
        These are rough estimates and should be refined with actual data
        """
        co2_factors = {
            'bus': 0.1,      # kg CO2 per km
            'metro': 0.05,   # kg CO2 per km
            'train': 0.04,   # kg CO2 per km
            'tram': 0.03,    # kg CO2 per km
            'bicycle': 0.0   # No emissions
        }
        transport_type = self.cleaned_data.get('transport_type')
        distance = self.cleaned_data.get('distance_traveled')
        
        return distance * co2_factors.get(transport_type, 0.1)