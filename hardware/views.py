from audioop import mul
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mass_mail, send_mail
from django.template.loader import render_to_string

from .decorators import unauthenticated_user, allowed_users
from .models import *
from .forms import *
from .filters import EmployeeFilter, ExitEmployeeFilter, LaptopFilter

from datetime import date
from environs import Env

env = Env()
env.read_env()

#Helpers
def employee_add_email(emp_id, emp_name, lk_emp_id, dept_id, desig_id, loc_id, request):
    URL = request.build_absolute_uri(reverse('onbrd_hw_assign', args=(emp_id,)))
    SUBJECT = f"[miniERP] New Employee Added: {emp_name}"
    context = {
        'emp_name': emp_name,
        'url': URL,
        'lk_emp_id': lk_emp_id,
        'dept_id': dept_id,
        'desig_id': desig_id,
        'loc_id': loc_id
    }
    MESSAGE = render_to_string('hardware/employee_add_email.html', context)
    FROM = 'notifications.miniERP@gmail.com'
    send_mail(SUBJECT, MESSAGE, FROM, env.list("EMAIL_RECIPIENTS"), fail_silently=True, html_message=MESSAGE)

def load_designations(request):
    dept_id = request.GET.get('dept_id')
    designations = Designation.objects.filter(dept_id=dept_id).order_by('designation')
    context = {'designations': designations}
    return render(request, 'partials/designation_dropdown_list.html', context)

def load_buildings(request):
    laptop_branch = request.GET.get('laptop_branch')
    print(laptop_branch)
    buildings = Building.objects.filter(location=laptop_branch).order_by('building')
    context = {'buildings': buildings}
    return render(request, 'partials/building_dropdown_list.html', context)

#Views
@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "username OR password is Incorrect.")

    context = {}
    return render(request, 'login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee_list_view(request):

    myFilter = EmployeeFilter(request.GET, queryset=Employee.objects.all())
    employees = myFilter.qs
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'employees': employees, 'myFilter':myFilter, 'page_obj': page_obj}
    return render(request, 'employees/employees.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee(request, pk):

    employee_info = Employee.objects.get(emp_id=pk)
    hardware_type = Hardware._meta.get_field('hardware_id').remote_field.model.__name__
    laptop_assigned = None
    number_of_laptops = ''
    try:
        del request.session['assign_new']
    except KeyError:
        pass

    try:
        laptop_assigned = Laptop.objects.get(emp_id=pk)
        number_of_laptops = '1'
    except Laptop.MultipleObjectsReturned:
        number_of_laptops = '>1'
        laptop_assigned = Laptop.objects.filter(emp_id=pk)
    except Laptop.DoesNotExist:
        number_of_laptops = '0'
    except Exception as e:
        return HttpResponse(e)

    qry = employee_info.history.all()
    def historical_changes(qry):
        changes = []
        if qry is not None and id:
            last = qry.first()
            for all_changes in range(qry.count()):
                new_record, old_record = last, last.prev_record
                if old_record is not None:
                    delta = new_record.diff_against(old_record)
                    changes.append(delta)
                last = old_record
        return changes
    changes = historical_changes(qry)

    context = {'employee_info': employee_info, 'number_of_laptops': number_of_laptops,
    'laptop_assigned': laptop_assigned, 'hardware_type':hardware_type, 'changes':changes,}
    return render(request, 'employees/employee.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee_add_view(request):

    form = EmployeeForm()
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            instance = form.save()
            employee_add_email(instance.emp_id, instance.emp_name, lk_emp_id=instance.lk_emp_id,
            dept_id=instance.dept_id, desig_id=instance.desig_id, loc_id=instance.loc_id, request=request)
            messages.success(request, "Successfully Added New Employee")
            return redirect(employee_list_view)
        else:
            print(form.errors)
            
    cancel_url_name = reverse('dash_employees')

    context = {'form':form, 'cancel_url_name': cancel_url_name}
    return render(request, 'employees/add_new_employee.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee_edit_view(request, pk):
    employee = Employee.objects.get(emp_id=pk)
    form = EmployeeForm(instance=employee)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f"Succesfully Edited {employee.emp_name}'s Profile")
            return redirect('employee', employee.emp_id)        

    cancel_url_name = reverse('employee', args=(employee.emp_id,))

    context = {'form':form, 'employee':employee, 'cancel_url_name': cancel_url_name}
    return render(request, 'employees/add_new_employee.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee_delete_view(request, pk):
    employee = Employee.objects.get(emp_id=pk)

    if request.method == "POST":
        employee.delete()
        messages.success(request, f'Successfully Deleted {employee}')
        return redirect(employee_list_view)

    context = {'employee':employee}
    return render(request, 'employees/employee_delete_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def laptops_list_view(request):

    myFilter = LaptopFilter(request.GET, queryset=Laptop.objects.all())
    laptops = myFilter.qs
    paginator = Paginator(laptops, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'myFilter':myFilter, 'page_obj': page_obj}
    return render(request, 'laptops/laptops.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def laptop(request, pk):
    laptop_info = Laptop.objects.get(id=pk)
    qry = laptop_info.history.all()

    def historical_changes(qry):
        changes = []
        if qry is not None and id:
            last = qry.first()
            for all_changes in range(qry.count()):
                new_record, old_record = last, last.prev_record
                if old_record is not None:
                    delta = new_record.diff_against(old_record)
                    changes.append(delta)
                last = old_record
        return changes
    
    changes = historical_changes(qry)

    context = {'laptop_info': laptop_info, 'changes':changes}
    return render(request, 'laptops/laptop.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def laptop_add_view(request):
    form = LaptopForm()

    if request.method == 'POST':
        form = LaptopForm(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request, f"Successfully added {instance} to database.")
            return redirect(laptops_list_view)
    
    cancel_url = reverse('dash_laptops')

    context = {'form' : form, 'cancel_url': cancel_url}
    return render(request, 'laptops/add_new_laptop.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def laptop_edit_view(request, pk):
    laptop = Laptop.objects.get(id=pk)
    form = LaptopForm(instance=laptop)

    if request.method == 'POST':
        form = LaptopForm(request.POST, instance=laptop)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully Edited {laptop}')
            return redirect('laptop', laptop.id)

    cancel_url = reverse('laptop', args=(laptop.id,))

    context = {'form':form, 'laptop':laptop, 'cancel_url': cancel_url}
    return render(request, 'laptops/add_new_laptop.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def laptop_delete_view(request, pk):
    laptop = Laptop.objects.get(id=pk)
    if request.method == 'POST':
        messages.success(request, f"Succesfully deleted {laptop}")
        laptop.delete()
        return redirect(laptops_list_view)
    
    context = {'laptop':laptop}
    return render(request, 'laptops/laptop_delete_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def onboarding_add_employee_view(request):
    """
    View for Step 1/3 of 'Onboarding', adding the new employee details & saving it.
    After saving it, it passes over the emp_id to Step 2 for Laptop selection.
    """
    form = EmployeeForm()
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            instance = form.save()
            # request.session['onboard_employee'] = instance.emp_id
            messages.success(request, f"Added New Employee {instance.emp_name}")
            return redirect(onboarding_assign_hardware_view, instance.emp_id)

    context = {'form':form}
    return render(request, 'onboard/onboarding_add_employee.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def onboarding_assign_hardware_view(request, pk):
    """
    View for Step 2/3 of 'Onboarding', selecting a laptop for the newly added employee
    from the previous step. Available laptops are based of the employees Location.
    """
    onboarded_emp = Employee.objects.get(emp_id=pk)
    request.session['onboard_employee'] = onboarded_emp.emp_id
    free_laptops = Laptop.objects.filter(laptop_branch=onboarded_emp.loc_id, laptop_status='Working', emp_id=None)
    
    context = {'onboarded_emp':onboarded_emp, 'free_laptops':free_laptops}
    return render(request, 'onboard/onboarding_assign_hardware.html', context)

def onboarding_complete_view(request, pk):
    """
    View for Step 3/3 of 'Onboarding', assigining the selected laptop from previous
    step to the onboarded employee.
    """
    selected_laptop = Laptop.objects.get(id=pk)
    employee_to_assign = Employee.objects.get(emp_id=request.session['onboard_employee'])

    selected_laptop.emp_id = employee_to_assign
    selected_laptop.save()

    employee_to_assign.is_assigned = True
    employee_to_assign.save()

    messages.success(request, f"Succesfully assigned the laptop: {selected_laptop} to {employee_to_assign}")
    return redirect(employee, employee_to_assign.emp_id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def laptop_return(request, pk):

    today = date.today()
    employee_info = Employee.objects.get(emp_id=pk)
    hardware_type = Hardware._meta.get_field('hardware_id').remote_field.model.__name__
    assign_new = request.session['assign_new']

    try:
        laptop_assigned = Laptop.objects.get(emp_id=pk)
        number_of_laptops = "1"
    except Laptop.MultipleObjectsReturned:
        number_of_laptops = ">1"
        laptop_assigned = Laptop.objects.filter(emp_id=pk)
    except Exception as e:
        return HttpResponse(e)
    
    form = LaptopReturnForm(
        initial={
            'laptop_date_returned': today.strftime("%b %d, %Y")
        }
    )

    if request.method == "POST":
        
        form = LaptopReturnForm(
            request.POST,
            initial={
                'laptop_date_returned': today.strftime("%b %d, %Y")
            },
            instance=laptop_assigned
        )

        if form.is_valid():

            form.save(returning=True)
            messages.info(request, f"Laptop Return for {employee_info.emp_name} Complete.")

            if assign_new == 'true':
                return redirect('onbrd_hw_assign', employee_info.emp_id)
            elif assign_new == 'false':
                return redirect('employee', employee_info.emp_id )
            else:
                return HttpResponse("'Assign New' condition not found")
    
    context = {'employee_info':employee_info, 'hardware_type':hardware_type,
    'laptop_assigned':laptop_assigned, 'number_of_laptops':number_of_laptops, 
    'return_form': form}
    return render(request, 'replace/replace_confirm.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def emp_exit(request):
    employees = Employee.objects.filter(emp_status='Active')
    myExitFilter = ExitEmployeeFilter(request.GET, queryset=employees)
    employees = myExitFilter.qs

    context = {'myExitFilter':myExitFilter, 'employees':employees}
    return render(request, 'exit/emp_exit.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def emp_exit_confirm(request, pk):

    employee_info = Employee.objects.get(emp_id=pk)
    employee_info.emp_status = 'InActive'
    employee_info.save()
    request.session['assign_new'] = 'false'

    messages.success(request, f"{employee_info.emp_name}'s Exit Complete")

    return redirect(laptop_return, employee_info.emp_id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def emp_exit_complete(request, pk):
    employee = Employee.objects.get(emp_id=pk)
    laptop_assigned = Laptop.objects.get(emp_id=pk)
    employee.emp_status = 'InActive'
    employee.save()
    laptop_assigned.emp_id = None
    laptop_assigned.save()
    messages.success(request, f"{employee.emp_name}'s Exit succesfully processed.")
    return redirect('employee', employee.emp_id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def employee_profile_view(request):
    '''
    An 'employee self service' page where the employee can view all the hardware
    that have been assigned to him/her.
    '''
    laptop_assigned = Laptop.objects.get(emp_id=request.user.employee)
    hardwareType = Hardware._meta.get_field('hardware_id').remote_field.model.__name__
    context = {'laptop_assigned':laptop_assigned, 'hardwareType':hardwareType}
    return render(request, 'employees/employee_profile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee',])
def employee_profile_edit_view(request):
    employee = request.user.employee
    form = EmployeeForm(instance=employee)

    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'employees/empSettingsPage.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def search_results_for_laptop_assignment(request):

    lk_emp_id = request.POST.get('lk_emp_id')

    try:
        employee = Employee.objects.get(lk_emp_id=lk_emp_id)
        laptop = Laptop.objects.filter(emp_id=employee)
        num_of_laptops = laptop.count()
    except Employee.DoesNotExist:
        return HttpResponse("<div><br><p style='color: red;'>Invalid Employee ID, Please enter a valid employee ID</p></div>")
    except Exception as e:
        return HttpResponse(e)
        
    context = {'employee': employee, 'laptop': laptop, 'num_of_laptops':num_of_laptops}
    return render(request, 'partials/search-result-assign.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def search_results_for_laptop_replacement(request):

    lk_emp_id = request.POST.get('lk_emp_id')
    request.session['assign_new'] = request.POST.get('assign_new')

    try:
        employee = Employee.objects.get(lk_emp_id=lk_emp_id)
        laptop = Laptop.objects.filter(emp_id=employee)
        num_of_laptops = laptop.count()       
    except Employee.DoesNotExist:
        return HttpResponse("<div><br><p style='color: red;'>Invalid Employee ID! Please enter a valid employee ID</p></div>")
    except Exception as e:
        return HttpResponse(e)

    context = {'employee': employee, 'laptop': laptop, 'num_of_laptops':num_of_laptops}
    return render(request, 'partials/search-result-replace.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def search_results_for_laptop_return(request):

    lk_emp_id = request.POST.get('lk_emp_id')
    request.session['assign_new'] = request.POST.get('assign_new')

    try:
        employee = Employee.objects.get(lk_emp_id=lk_emp_id)
        laptop = Laptop.objects.filter(emp_id=employee)
        num_of_laptops = laptop.count()       
    except Employee.DoesNotExist:
        return HttpResponse("<div><br><p style='color: red;'>Invalid Employee ID! Please enter a valid employee ID</p></div>")
    except Exception as e:
        return HttpResponse(e)

    context = {'employee': employee, 'laptop': laptop, 'num_of_laptops':num_of_laptops}
    return render(request, 'partials/search-result-return.html', context)
