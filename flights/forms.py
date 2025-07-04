from django import forms

class FlightFilterForm(forms.Form):
    source = forms.ChoiceField(
        required=False,
        label='Source (IATA Code)',
        choices=[],
    )
    destination = forms.ChoiceField(
        required=False,
        label='Destination (IATA Code)',
        choices=[],
    )
    start_date = forms.DateField(
        required=False,
        label='Start Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        label='End Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        source_choices = kwargs.pop('source_choices', [])
        destination_choices = kwargs.pop('destination_choices', [])
        super().__init__(*args, **kwargs)

        self.fields['source'].choices = [('', 'Any')] + source_choices
        self.fields['destination'].choices = [('', 'Any')] + destination_choices
