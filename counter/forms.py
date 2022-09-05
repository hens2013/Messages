from django import forms


class CountryDetails(forms.Form):
    country_name = forms.CharField(label='Country Name', max_length=100, required=True)


class LocationDetails(forms.Form):
    latitude_number = forms.FloatField(required=True)
    longitude_number = forms.FloatField(required=True)
    radios_number = forms.FloatField(required=True)
