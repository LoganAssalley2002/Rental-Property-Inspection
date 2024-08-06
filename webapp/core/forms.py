import datetime
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from core.models import Profile
from core.models import Property
from core.models import Area
from core.models import AreaImage
from core.models import Inspection


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {
                'placeholder': 'Username',
                'icon': 'envelope',
                'class': 'owl-input',
                'autocomplete': 'off'
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'placeholder': 'Password',
                'icon': 'shield-lock',
                'class': 'owl-input',
                'autocomplete': 'off'
            }
        )


class CreateAccountForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter Username',
                'autocomplete': 'off',
                'class': 'owl-input',
                'icon': 'person-square'
            }
        )
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Password',
                'autocomplete': 'off',
                'class': 'owl-input',
                'icon': 'shield-lock'
            }
        )
    )
    password2 = forms.CharField(
        label='Password Again',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Password Again',
                'autocomplete': 'off',
                'class': 'owl-input',
                'icon': 'shield-check'
            }
        )
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter Email',
                'autocomplete': 'off',
                'class': 'owl-input',
                'icon': 'envelope'
            }
        )
    )
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter First Name',
                'autocomplete': 'off',
                'class': 'owl-input',
                'icon': 'person'
            }
        )
    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter Last Name',
                'autocomplete': 'off',
                'class': 'owl-input',
                'icon': 'person-check'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile = Profile.objects.create(user=user)

        return user


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address']

    def __init__(self, owner, *args, **kwargs):
        self.owner = owner
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

    def clean_name(self):
        name = self.cleaned_data['name']
        if Property.objects.filter(name=name, owner=self.owner).exists():
            self.add_error('name', 'You already have a property with this name')

        return name

    def clean_address(self):
        address = self.cleaned_data['address']
        if Property.objects.filter(address=address, owner=self.owner).exists():
            self.add_error('address', 'You already have a property with this address')

        return address

    def save(self):
        property_ = super().save(commit=False)
        property_.owner = self.owner
        property_.save()
        return property_



class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['inspector', 'inspected_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['inspector'].queryset = User.objects.filter(groups__name='Inspector')

    def clean_inspected_user(self):
        inspected_user = self.cleaned_data['inspected_user']
        # Check if user is editing an existing inspection
        if self.instance.pk and self.instance.inspected_property:
            # If user already chose/created a property for this inspection, that property
            # is related to the inspection.owner. Later on if they attempt to change the
            # inspected_user, you should handle that case.
            # Either change the inspection.inspected_property.owner to this new selected user
            # or delete the inspected property and areas.
            if self.instance.inspected_property.owner != inspected_user:
                # If you dont want to allow this, add an error to form and return that error
                # message insted of the below line
                self.instance.inspected_property.owner = inspected_user
                self.instance.inspected_property.save(update_fields=['owner'])
        return inspected_user





class AddPropertyToInspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['inspected_property']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['inspected_property'].required = True
        self.fields['inspected_property'].label = 'Choose Property'
        self.fields['inspected_property'].help_text = 'Choose Property from the dropdown or create new one.'
        self.fields['inspected_property'].queryset = Property.objects.filter(owner=self.instance.inspected_user)





class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['name', 'notes']

    def __init__(self, inspection, *args, **kwargs):
        self.inspection = inspection
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

    def save(self):
        area = super().save(commit=False)
        area.inspection = self.inspection
        area.save()
        return area


class AreaImageForm(forms.ModelForm):
    class Meta:
        model = AreaImage
        fields = ['picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})


























