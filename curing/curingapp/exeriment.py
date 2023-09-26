from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout
from .forms import TransactionConcretingForm,ProjectForm,SiteForm,ImageUploadForm,StructuralElementForm
from .models import Schedule_Curing,Transaction_Concreting,Site_Master,Project_Master
from datetime import datetime
from datetime import timedelta
from logfile import logdata
from django.http import JsonResponse
from django.core import serializers
from django.utils import timezone

def camera_view(request):
    return render(request,'curingapp/camera.html')

def schedule_curing_table(request, transaction_concreting_id):
    schedules = Schedule_Curing.objects.filter(Transaction_Concreting_id=transaction_concreting_id)
    transaction = get_object_or_404(Transaction_Concreting, pk=transaction_concreting_id)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            schedule_entry_id = form.cleaned_data['schedule_entry_id']
            schedule_entry = get_object_or_404(Schedule_Curing, pk=schedule_entry_id)

            # Save the uploaded image to the Image_Of_Curing field of the schedule entry
            schedule_entry.Image_Of_Curing = request.FILES['image']  # Use request.FILES to get the uploaded image
            schedule_entry.save()

            # Redirect back to the same page to prevent resubmission issues
            return redirect('schedule_curing_table', transaction_concreting_id=transaction_concreting_id)
    else:
        form = ImageUploadForm()

    variables = {
        'page_title': 'Ashoka Buildcon Limited',
        'username': request.user.get_full_name(),
        'isActive': request.user.is_authenticated,
        'isSuperUser': request.user.is_superuser,
        'app_title': 'Document Inbox',
        'isForm': True,
        'isHomePage': True,
        'customer_name': 'Ashoka Buildcon Limited',
        'form': form,
        'transaction': transaction,
        'schedules': schedules,
        'transaction_concreting_id': transaction_concreting_id
    }

    return render(request, 'curingapp/experiment.html', variables)
    
def upload_image_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            schedule_entry_id = form.cleaned_data['schedule_entry_id']
            schedule_entry = get_object_or_404(Schedule_Curing, pk=schedule_entry_id)

            # Save the uploaded image to the Image_Of_Curing field of the schedule entry
            schedule_entry.Image_Of_Curing = form.cleaned_data['image']
            schedule_entry.save()

            # Replace the following with the actual image URL if needed
            image_url = schedule_entry.Image_Of_Curing.url

            return JsonResponse({'success': True, 'image_url': image_url})
        else:
            # Print form validation errors to help with debugging
            print(form.errors)
            return JsonResponse({'success': False, 'error': 'Form validation failed'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})