from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import *
from .filters import EmployeeFilter, ExitEmployeeFilter, LaptopFilter

from datetime import date

def load_designations(request):
    dept_id = request.GET.get('dept_id')
    designations = Designation.objects.filter(dept_id=dept_id).order_by('designation')
    context = {'designations': designations}
    return render(request, 'partials/designation_dropdown_list.html', context)

@unauthenticated_user
def register(request):
    '''
    Register a new user. This view uses a custom UserCreationForm where in an additional
    email field is added and all other decorators are removed.
    '''
    form1 = CreateUserForm()
    if request.method == "POST":
        form1 = CreateUserForm(request.POST)
        if form1.is_valid():
            user = form1.save()
            username = form1.cleaned_data.get('username')
            messages.success(request, "Account was created for " + username)
            return redirect('login')
            
    context = {'form1':form1}
    return render(request, 'hardware/register.html', context)

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
@admin_only
def home(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def onboading(request):
    return render(request, 'onboard/onboard.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def replace(request):
    employees = Employee.objects.filter(laptop__emp_id__isnull=False)
    
    myExitFilter = ExitEmployeeFilter(request.GET, queryset=employees)
    employees = myExitFilter.qs

    context = {'myExitFilter':myExitFilter, 'employees':employees,}
    return render(request, 'replace/replace.html', context)

def replace_confirm(request, pk):
    employee_info = Employee.objects.get(emp_id=pk)
    laptop_assigned = Laptop.objects.get(emp_id=pk)
    hardware_type = Hardware._meta.get_field('hardware_id').remote_field.model.__name__

    today = date.today()

    laptop_exit_form = EmployeeExitFormLaptop(initial={'laptop_date_returned':today.strftime("%b %d, %Y"), 'laptop_return_remarks':''})
    # laptop_exit_media_form = EmployeeExitFormLaptopImage(instance=laptop_assigned)

    if request.method == "POST":
        laptop_exit_form = EmployeeExitFormLaptop(request.POST, initial={'laptop_date_returned':today.strftime("%b %d, %Y"), 'laptop_return_remarks':'Enter Any Remarks here'}, instance=laptop_assigned)
        # laptop_exit_media_form = EmployeeExitFormLaptopImage(request.POST, request.FILES)
        if laptop_exit_form.is_valid():
            # laptop_assigned.media = laptop_exit_media_form.save()
            laptop_exit_form.save()
            # laptop_exit_media_form.save()

            laptop_assigned.emp_id=None
            laptop_assigned.save()
            
            return redirect('replace_assign_new', employee_info.emp_id)

    context = {'employee_info':employee_info, 'hardware_type':hardware_type,
    'laptop_assigned':laptop_assigned, 'laptop_exit_form':laptop_exit_form}

    return render(request, 'replace/replace_confirm.html', context)

def replace_assign_new(request, pk):
    employee = Employee.objects.get(emp_id=pk)
    free_laptops = Laptop.objects.filter(laptop_branch=employee.loc_id, laptop_status='Working', emp_id=None)
    request.session['employee'] = employee.emp_id

    context={'employee':employee, 'free_laptops':free_laptops}
    return render(request, 'replace/replace_assign_new.html', context)

def replace_complete(request, pk):
    laptop_assigned = Laptop.objects.get(id=pk)
    laptop_assigned.emp_id = Employee.objects.get(emp_id=request.session['employee'])
    laptop_assigned.save()
    del request.session['employee']

    return redirect('laptop', laptop_assigned.id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee_list_view(request):
    employees = Employee.objects.all()
    active_emps = Employee.objects.filter(emp_status = 'Active').count()
    inactive_emps = Employee.objects.filter(emp_status = 'InActive').count()

    myFilter = EmployeeFilter(request.GET, queryset=employees)
    employees = myFilter.qs

    context = {'active_emps': active_emps, 'inactive_emps': inactive_emps, 'employees': employees,
    'myFilter':myFilter}

    return render(request, 'employees/employees.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee(request, pk):
    employee_info = Employee.objects.get(emp_id=pk)
    laptop_assigned = None
    try:
        laptop_assigned = Laptop.objects.get(emp_id=pk)
    except:
        pass
    hardware_type = Hardware._meta.get_field('hardware_id').remote_field.model.__name__
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

    context = {'employee_info': employee_info, 'laptop_assigned': laptop_assigned,
    'hardware_type':hardware_type, 'changes':changes,}
    return render(request, 'employees/employee.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee_add_view(request):
    form = EmployeeForm()
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(employee_list_view)
        else:
            print(form.errors)

    context = {'form':form}
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
            messages.success(request, f'Successfully Edited {employee}', extra_tags='successful_edit')
            return redirect('employee', employee.emp_id)
    else:
        messages.success(request, f'Cancelled Editing of {employee}', extra_tags='cancel_edit')

    context = {'form':form, 'employee':employee}
    return render(request, 'employees/add_new_employee.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee_delete_view(request, pk):
    employee = Employee.objects.get(emp_id=pk)
    messages.success(request, f'Cancelled deletion of {employee}', extra_tags='cancel_delete')
    if request.method == "POST":
        employee.delete()
        messages.success(request, f'Successfully Deleted {employee}', extra_tags='successful_delete')
        return redirect(employee_list_view)
        

    context = {'employee':employee}
    return render(request, 'employees/employee_delete_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def laptops_list_view(request):
    laptops = Laptop.objects.all()

    myFilter = LaptopFilter(request.GET, queryset=laptops)
    laptops = myFilter.qs

    context = {'myFilter':myFilter, 'laptops': laptops}
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
            form.save()
            return redirect(laptops_list_view)

    context = {'form' : form}
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
            messages.success(request, f'Successfully Edited {laptop}', extra_tags='successful_edit')
            return redirect('laptop', laptop.id)
    else:
        messages.success(request, f'Cancelled Editing of {laptop}', extra_tags='cancel_edit')

    context = {'form':form, 'laptop':laptop}
    return render(request, 'laptops/add_new_laptop.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def laptop_delete_view(request, pk):
    laptop = Laptop.objects.get(id=pk)
    if request.method == 'POST':
        laptop.delete()
        messages.success(request, f"Succesfully deleted {laptop}", extra_tags="successful_delete")
        return redirect(laptops_list_view)
    
    context = {'laptop':laptop}
    return render(request, 'laptops/laptop_delete_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def onbrd_emp_add(request):
    form = EmployeeForm()
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added New Employee")
            return redirect('onbrd_hw_assign')
    context = {'form':form}
    return render(request, 'onboard/onbrd_emp_add.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def onbrd_hw_assign(request):
    
    latest_emp = Employee.objects.last()
    free_laptops = Laptop.objects.filter(laptop_branch=latest_emp.loc_id, laptop_status='Working', emp_id=None)
    
    context = {'latest_emp':latest_emp, 'free_laptops':free_laptops}
    return render(request, 'onboard/onbrd_hw_assign.html', context)

def onbrd_complete(request, pk):
    laptop_assigned = Laptop.objects.get(id=pk)
    employee_to_assign = Employee.objects.last()
    print(employee_to_assign.emp_id)
    laptop_assigned.emp_id = employee_to_assign
    laptop_assigned.save()
    messages.success(request, f"{employee_to_assign} succesfully onboarded!", extra_tags="onbrd_complete")

    return redirect('employee', employee_to_assign.emp_id)

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
    laptop_assigned = Laptop.objects.get(emp_id=pk)
    hardware_type = Hardware._meta.get_field('hardware_id').remote_field.model.__name__

    today = date.today()

    laptop_exit_form = EmployeeExitFormLaptop(initial={'laptop_date_returned':today.strftime('%b %d, %Y'), 'laptop_return_remarks':''})
    # laptop_exit_media_form = EmployeeExitFormLaptopImage(instance=laptop_assigned)

    if request.method == "POST":
        laptop_exit_form = EmployeeExitFormLaptop(request.POST, initial={'laptop_date_returned':today.strftime('%b %d, %Y'), 'laptop_return_remarks':'Enter Any Remarks here'}, instance=laptop_assigned)
        # laptop_exit_media_form = EmployeeExitFormLaptopImage(request.POST, request.FILES)
        if laptop_exit_form.is_valid():
            # laptop_assigned.media = laptop_exit_media_form.save()
            laptop_exit_form.save()
            # laptop_exit_media_form.save()
            messages.success(request, f"{employee_info.emp_name}'s Exit succesfully processed", extra_tags="exit_confirm")
            return redirect('emp_exit_complete', employee_info.emp_id)

    context = {'employee_info':employee_info, 'hardware_type':hardware_type,
    'laptop_assigned':laptop_assigned, 'laptop_exit_form':laptop_exit_form}
    return render(request, 'exit/emp_exit_confirm.html', context)

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

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def lap_image_history(request, pk):
#     laptop = Laptop.objects.get(id=pk)
#     images = laptop.laptopmedia_set.all()

#     context = {'images':images}
#     return render(request, 'laptops/laptop_image_history.html', context)
