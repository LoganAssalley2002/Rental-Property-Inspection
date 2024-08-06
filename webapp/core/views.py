from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


from core.forms import CreateAccountForm
from core.forms import PropertyForm
# from core.forms import InspectionForm
from core.forms import AreaForm
from core.forms import AreaImageForm
from core.forms import CustomAuthenticationForm
from core.forms import InspectionForm
from core.forms import AddPropertyToInspectionForm

from core.models import Profile
from core.models import Property
from core.models import Inspection
from core.models import Area
from core.models import AreaImage

def is_inspector(user):
    return user.groups.filter(name='Inspector').exists()




def home(request):
    context = {}
    return render(request, 'core/home.html', context)



def login_view(request):
    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.add_message(request, messages.SUCCESS, 'You are successfully logged in!')
            return redirect('account')
    else:
        # If request method is not POST, display an empty login form (authentication form is just the form)
        form = CustomAuthenticationForm()

    context = {
        'form': form
    }
    return render(request, 'core/login.html', context) 


def create_account(request):
    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        # check if user form is valid
        if form.is_valid():
            # This will handle saving the user
            user = form.save()
            # login user to the account they just created
            auth_login(request, user)

            messages.add_message(request, messages.SUCCESS, 'Your account is created!')
            return redirect('account')
    else:
        form = CreateAccountForm

    context = {
        'form': form
    }

    return render(request, 'core/create_account.html', context)


def logout_view(request):
    '''
    When user clicks "logout" button, logout and redirect to homepage
    '''
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'You are logged out.')
    return redirect('home')


@login_required
def account(request):
    context = {}
    return render(request, 'core/account.html', context)




@login_required
def inspections(request):
    if is_inspector(request.user):
        inspections = Inspection.objects.filter(inspector=request.user)
    else:
        inspections = Inspection.objects.filter(inspected_user=request.user)\
                                        .exclude(inspected_property=None)\
                                        .exclude(areas=None)

    
    context = {
        'inspections': inspections
    }
    return render(request, 'core/inspections.html', context)


@login_required
def properties(request):
    properties = Property.objects.filter(owner=request.user)
    context = {
        'properties': properties
    }
    return render(request, 'core/properties.html', context)



@login_required
def create_property(request):
    inspection_id = request.GET.get('inspection_id', None)

    if is_inspector(request.user) and inspection_id:
        owner = get_object_or_404(User, pk=int(request.GET.get('owner')))
    else:
        owner = request.user

    if request.method == 'POST':
        form = PropertyForm(owner, request.POST)
        if form.is_valid():
            property_ = form.save()
            messages.add_message(request, messages.SUCCESS, f'Successfully created new property: {property_.name}!')
            if inspection_id:
                return redirect('create_inspection_property', int(inspection_id))
            else:
                return redirect('properties')
                

    else:
        form = PropertyForm(owner)
    
    context = {
        'form': form
    }
    return render(request, 'core/create_property.html', context)


@login_required
def property_detail(request, property_id):
    property_ = get_object_or_404(Property, pk=property_id)
    
    if property_.owner != request.user:
        return redirect('account')
    
    context = {
        'property': property_
    }
    return render(request, 'core/property_detail.html', context)


@user_passes_test(is_inspector)
def create_inspection(request):
    inspection_id = request.GET.get('inspection_id', None)
    if inspection_id:
        instance = get_object_or_404(Inspection, pk=int(inspection_id))
        button_text = 'Save'
    else:
        instance = None
        button_text = 'Next'

    if request.method == 'POST':
        form = InspectionForm(request.POST, instance=instance)
        if form.is_valid():
            inspection = form.save()
            if inspection_id:
                return redirect('inspection_detail', instance.id)
            else:
                return redirect('create_inspection_property', inspection.id)
    else:
        form = InspectionForm(instance=instance)

    context = {
        'form': form,
        'button_text': button_text
    }
    return render(request, 'core/create_inspection.html', context)


@user_passes_test(is_inspector)
def create_inspection_property(request, inspection_id):
    edit = request.GET.get('edit', None)
    inspection = get_object_or_404(Inspection, pk=inspection_id)

    if edit:
        button_text = 'Save'
    else:
        button_text = 'Next'

    # Uncomment below if a request.user must be the inspector of this particular inspection to edit.
    # if inspection.inspector != request.user:
    #     return redirect('inspections')

    if request.method == 'POST':
        form = AddPropertyToInspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            form.save()
            if edit:
                return redirect('inspections')
            else:
                return redirect('create_inspection_area', inspection.id)
    else:
        form = AddPropertyToInspectionForm(instance=inspection)

    context = {
        'form': form,
        'button_text': button_text
    }
    return render(request, 'core/create_inspection_property.html', context)


@login_required
def inspection_detail(request, inspection_id):
    inspection = get_object_or_404(Inspection, pk=inspection_id)
    
    context = {
        'inspection': inspection
    }
    return render(request, 'core/inspection_detail.html', context)


@user_passes_test(is_inspector)
def create_inspection_area(request, inspection_id):
    inspection = get_object_or_404(Inspection, pk=inspection_id)

    # Uncomment below if a request.user must be the inspector of this particular inspection to edit.
    # if inspection.inspector != request.user:
    #     return redirect('inspections')

    if request.method == 'POST':
        form = AreaForm(inspection, request.POST)
        area_pictures = request.FILES.getlist('area-picture')

        if form.is_valid():
            area = form.save()
            for picture in area_pictures:
                AreaImage.objects.create(area=area, picture=picture)
            if 'add-another' in request.POST:
                return redirect('create_inspection_area', inspection.pk)
            elif 'finish' in request.POST:
                messages.add_message(request, messages.SUCCESS, 'Your inspection is now completed!')
                return redirect('inspections')
            else:
                # TODO: Handle this case
                pass
    else:
        form = AreaForm(inspection=inspection)

    context = {
        'form': form
    }
    return render(request, 'core/create_inspection_area.html', context)



@user_passes_test(is_inspector)
def area_detail(request, inspection_id, area_id):
    inspection = get_object_or_404(Inspection, pk=inspection_id)
    area = get_object_or_404(Area, pk=area_id)
    area_images = AreaImage.objects.filter(area=area)

    context = {
        'area': area,
        'area_images': area_images
    }
    return render(request, 'core/area_detail.html', context)
































