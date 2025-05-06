from django import forms


class ShippingForm(forms.Form):
    pincode = forms.CharField(min_length=6, max_length=6, widget=forms.NumberInput(attrs={"class": "uk-input", "placeholder": "Pincode"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "uk-input", "placeholder": "City"}))
    state = forms.CharField(widget=forms.TextInput(attrs={"class": "uk-input", "placeholder": "State"}))
    fullname = forms.CharField(widget=forms.TextInput(attrs={"class": "uk-input", "placeholder": "Full Name"}))
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={"class": "uk-input", "placeholder": "House No / Building / Apartment"}))
    address_line_2 = forms.CharField(widget=forms.TextInput(attrs={"class": "uk-input", "placeholder": "Area, Sector, Street, Village"}))
    mobile = forms.CharField(min_length=10, max_length=10, widget=forms.TextInput(attrs={"class": "uk-input", "placeholder": "Mobile no"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "uk-input", "placeholder": "Email"}))