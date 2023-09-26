from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from .forms import RegisterUserForm,EditUserForm,TransactionConcretingForm,ProjectForm,SiteForm,ImageUploadForm,StructuralElementForm,ChangePasswordForm
from .models import Schedule_Curing,Transaction_Concreting,Site_Master,Project_Master,Structural_Element,CustomUser
from datetime import datetime
from datetime import timedelta
from logfile import logdata
from django.http import JsonResponse

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        if user is not None and user.is_active:
            login(request,user)
            messages.info(request,'Login Successful...!')
            return redirect('home')
        else:
            messages.warning(request,'Something went wrong..! please check input ')
            return redirect('loginuser')
        
    else:
        return render(request,'curingapp/login.html')
    
def logout_user(request):
    logout(request)
    return redirect("loginuser") 
    
def home(request):
    if request.user.is_authenticated:
        print('Logged')
    else:
        print('not')
    
    variables = { 'page_title': 'Ashoka Buildcon Limited',
                  'username': request.user.get_full_name(), 
                  'isActive' : request.user.is_authenticated,
                  'isSuperUser' : request.user.is_superuser,
                  'app_title':'Document Inbox',
                  'isForm' : True,
                  'isHomePage' : True,
                  'customer_name' : 'Ashoka Buildcon Limited',
                }
    return render(request, 'curingapp/home.html', variables)

def register_user(request):
    custom_users=CustomUser.objects.all()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            variable = form.save(commit=False)
            variable.save()
            messages.info(request,'Your Account has been Successfully Register...! Please Login')
            return redirect('loginuser')
        else:
            messages.warning(request,'Something went wrong..! Please check form input ')
            return redirect('register_user')

    else:
        form = RegisterUserForm()

    variables = { 'page_title': 'Ashoka Buildcon Limited',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'app_title':'Document Inbox',
                'isForm' : True,
                'isHomePage' : True,
                'form':form,
                'custom_users':custom_users,
            }
    return render(request,'curingapp/register_user.html',variables)

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, User_ID=user_id)
    Projects= Project_Master.objects.all()
    Sites= Site_Master.objects.all()

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            logdata('asd')
            form.save()
            return redirect('home')  # Redirect to the user list view after editing
    else:
        form = EditUserForm(instance=user)
    variables = { 'page_title': 'Ashoka Buildcon Limited',
                'username': request.user.get_full_name(), 
                'isActive' : request.user.is_authenticated,
                'isSuperUser' : request.user.is_superuser,
                'app_title':'Document Inbox',
                'isForm' : True,
                'isHomePage' : True,
                'form':form,
                'user': user,
                'Projects':Projects,
                'Sites':Sites,
            }
    return render(request, 'curingapp/edit_user.html', variables)

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
       
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            msg = "Your password is changed"
            variables = { 'page_title': 'Ashoka Buildcon Limited',
                          'username': request.user.get_full_name(),
                          'isActive' : request.user.is_authenticated,
                          'isSuperUser' : request.user.is_superuser,
                          'isForm' : True,
                          'isHomePage' : True,
                          'customer_name' : 'Ashoka Buildcon Limited',
                          'successalert' : msg
                        }            
            return render(request, 'curingapp/home.html', variables)
        else:
            form = ChangePasswordForm(request.user)
            msg = 'Password do not match or incorrect passwords. Please try again'
            variables = { 'page_title': 'Ashoka Buildcon Limited',
                          'username': request.user.get_full_name(),
                          'isActive' : request.user.is_authenticated,
                          'isSuperUser' : request.user.is_superuser,
                          'isForm' : True,
                          'isHomePage' : True,
                          'customer_name' : 'Ashoka Buildcon Limited',
                          'successalert' : msg,
                          'form' : form,
                        }            
            return render(request, 'curingapp/change_password.html', variables)
    else:
        form = ChangePasswordForm(request.user)
        variables = { 'page_title': 'Ashoka Buildcon Limited',
                      'username': request.user.get_full_name(),
                      'isActive' : request.user.is_authenticated,
                      'isSuperUser' : request.user.is_superuser,
                      'app_title':'Document Inbox',
                      'isForm' : True,
                      'isHomePage' : True,
                      'customer_name' : 'Ashoka Buildcon Limited',
                      'form' : form,                     
                    }        
        return render(request, 'curingapp/change_password.html', variables)
    

def create_project(request):
    projects = Project_Master.objects.all()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, you can add a success message here
            return redirect('home')  # Redirect to the home page after successful project creation
    else:
        form = ProjectForm()
        variables = { 'page_title': 'Ashoka Buildcon Limited',
                  'username': request.user.get_full_name(), 
                  'isActive' : request.user.is_authenticated,
                  'isSuperUser' : request.user.is_superuser,
                  'app_title':'Document Inbox',
                  'isForm' : True,
                  'isHomePage' : True,
                  'customer_name' : 'Ashoka Buildcon Limited',
                  'form': form,
                  'projects':projects,
                }
    return render(request, 'curingapp/create_project.html',variables)

def edit_project(request, project_id):
    # Get the project object based on the project_id or return a 404 error if not found
    project = get_object_or_404(Project_Master, Project_ID=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()

            messages.success(request, 'Project updated successfully.') 
            # Optionally, you can add a success message here
            return redirect('home')  # Redirect to the home page after successful project edit
    else:
        # Create a form instance with the project data
        form = ProjectForm(instance=project)
    
    variables = {
        'page_title': 'Edit Project',
        'username': request.user.get_full_name(),
        'isActive': request.user.is_authenticated,
        'isSuperUser': request.user.is_superuser,
        'app_title': 'Document Inbox',
        'isForm': True,
        'isHomePage': False,  # Set to False because this is not the home page
        'customer_name': 'Ashoka Buildcon Limited',
        'form': form,
        'project_id': project_id,  # Pass the project_id to the template
        
    }

    return render(request, 'curingapp/edit_project.html', variables)

def create_site(request):
    sites=Site_Master.objects.all()
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, you can add a success message here
            return redirect('home')  # Redirect to the home page after successful site creation
    else:
        form = SiteForm()
        variables = { 'page_title': 'Ashoka Buildcon Limited',
                  'username': request.user.get_full_name(), 
                  'isActive' : request.user.is_authenticated,
                  'isSuperUser' : request.user.is_superuser,
                  'app_title':'Document Inbox',
                  'isForm' : True,
                  'isHomePage' : True,
                  'customer_name' : 'Ashoka Buildcon Limited',
                  'form': form,
                  'sites':sites,
                }
    return render(request, 'curingapp/create_site.html',variables)

def edit_site(request, site_id):
    # Get the site object based on the site_id or return a 404 error if not found
    site = get_object_or_404(Site_Master, Site_ID=site_id)

    if request.method == 'POST':
        form = SiteForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site updated successfully.')

            # Optionally, you can add a success message here
            # messages.success(request, 'Site updated successfully.')
            
            return redirect('home')  # Redirect to the home page after successful site edit
    else:
        # Create a form instance with the site data
        form = SiteForm(instance=site)

    variables = {
        'page_title': 'Edit Site',
        'username': request.user.get_full_name(),
        'isActive': request.user.is_authenticated,
        'isSuperUser': request.user.is_superuser,
        'app_title': 'Document Inbox',
        'isForm': True,
        'isHomePage': False,
        'customer_name': 'Ashoka Buildcon Limited',
        'form': form,
        'site_id': site_id,  # Pass the site_id to the template
    }

    return render(request, 'curingapp/edit_site.html', variables)

def create_structural_element(request):
    structural_elements=Structural_Element.objects.all()
    if request.method == 'POST':
        form = StructuralElementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to a success page or another appropriate URL
    else:
        form = StructuralElementForm()
        variables = { 'page_title': 'Ashoka Buildcon Limited',
                  'username': request.user.get_full_name(), 
                  'isActive' : request.user.is_authenticated,
                  'isSuperUser' : request.user.is_superuser,
                  'app_title':'Document Inbox',
                  'isForm' : True,
                  'isHomePage' : True,
                  'customer_name' : 'Ashoka Buildcon Limited',
                  'form': form,
                  'structural_elements':structural_elements,
                }
    return render(request, 'curingapp/create_structural_element.html', variables)

def edit_structural_element(request, element_id):
    element = get_object_or_404(Structural_Element, Structural_Element_ID=element_id)

    if request.method == 'POST':
        form = StructuralElementForm(request.POST, instance=element)
        if form.is_valid():
            form.save()
            messages.success(request, 'Structural Element updated successfully.')
            # Optionally, you can add a success message here
            # messages.success(request, 'Structural Element updated successfully.')
            return redirect('home')  # Redirect to the home page after successful edit
    else:
        form = StructuralElementForm(instance=element)

    variables = {
        'page_title': 'Edit Structural Element',
        'username': request.user.get_full_name(),
        'isActive': request.user.is_authenticated,
        'isSuperUser': request.user.is_superuser,
        'app_title': 'Document Inbox',
        'isForm': True,
        'isHomePage': False,
        'customer_name': 'Ashoka Buildcon Limited',
        'form': form,
        'element_id': element_id,
    }

    return render(request, 'curingapp/edit_element.html', variables)

def create_schedule_curing(request):
    if request.method == 'POST':
        form = TransactionConcretingForm(request.POST)
        if form.is_valid():
            project_id = form.cleaned_data['Project']
            site_id = form.cleaned_data['Site']
            try:
                # Get the corresponding project and site objects
                project = Project_Master.objects.get(Project_Name=project_id)
                site = Site_Master.objects.get(Site_Name=site_id)
                # Process the form data and save the instance if needed
                transaction_concreting = form.save(commit=False)
                form.instance.User = request.user

                transaction_concreting.Project = project
                transaction_concreting.Site = site

                transaction_concreting.save()
                transaction_concreting_id = transaction_concreting.pk  # pk passing for url for see specific schedules for transaction
                # logdata(transaction_concreting)
                
                #selected_structural_element access their data table
                selected_structural_element = transaction_concreting.Structural_Element
                no_of_days = selected_structural_element.No_Of_Days
                frequency=selected_structural_element.Frequency
                time_Bet_TwoCuring=selected_structural_element.Time_Bet_TwoCuring
                # Calculate the initial datetime based on the form submission time
                initial_datetime = datetime.now()
                form.fields['Schedule_Date_and_Time'].initial = initial_datetime
                # Create 10 sets of 2 entries in Schedule_Curing
                
                for i in range(no_of_days):
                    for j in range(frequency):
                        schedule_curing = Schedule_Curing(
                            Transaction_Concreting=transaction_concreting,
                            Project=transaction_concreting.Project,
                            Site=transaction_concreting.Site,
                            Structural_Element=transaction_concreting.Structural_Element,
                            Schedule_Date_and_Time=initial_datetime + timedelta(hours=i * (time_Bet_TwoCuring*2) + j * time_Bet_TwoCuring)
                        )
                        schedule_curing.save()
                return redirect('schedule_curing_table',transaction_concreting_id=transaction_concreting_id)
            except Exception as e: 
                 print(f"Error: {e}")
        else:
            print(form.errors)

    else:
        initial_datetime = datetime.now()
        form = TransactionConcretingForm(initial={'Schedule_Date_and_Time': initial_datetime})
    Projects = Project_Master.objects.all()
    Sites = Site_Master.objects.all()
    
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
        'Projects': Projects,
        'Sites': Sites,
    }
    return render(request, 'curingapp/start_schedule.html', variables)

def get_sites_for_project(request, project_id):
    # Retrieve the sites for the selected project
    sites = Site_Master.objects.filter(Project_id=project_id)
    # Convert the sites to JSON format
    site_data = [{'id': site.Site_ID, 'name': site.Site_Name} for site in sites]
    
    return JsonResponse({'sites': site_data})

def schedule_curing_table(request, transaction_concreting_id):
    schedules = Schedule_Curing.objects.filter(Transaction_Concreting_id=transaction_concreting_id)
    transaction = get_object_or_404(Transaction_Concreting, pk=transaction_concreting_id)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            schedule_entry_id = form.cleaned_data['schedule_entry_id']
            schedule_entry = get_object_or_404(Schedule_Curing, pk=schedule_entry_id)

            # Save the uploaded image to the Image_Of_Curing field of the schedule entry
            schedule_entry.Image_Of_Curing = form.cleaned_data['image']
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

    return render(request, 'curingapp/schedule_curing_table.html', variables)

def transaction_concreting_list(request):
    transactions = Transaction_Concreting.objects.filter(User=request.user)

    variables = { 'page_title': 'Ashoka Buildcon Limited',
                  'username': request.user.get_full_name(), 
                  'isActive' : request.user.is_authenticated,
                  'isSuperUser' : request.user.is_superuser,
                  'app_title':'Document Inbox',
                  'isForm' : True,
                  'isHomePage' : True,
                  'customer_name' : 'Ashoka Buildcon Limited',
                  'transactions': transactions
                }
    return render(request, 'curingapp/transaction_concreting_list.html', variables)

def transaction_detail(request, transaction_pk):
    transaction = get_object_or_404(Transaction_Concreting, pk=transaction_pk)
    return render(request, 'curingapp/transaction_detail.html', {'transaction': transaction})

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