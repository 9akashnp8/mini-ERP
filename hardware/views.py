from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.core import serializers
from django.urls import is_valid_path
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import *
from .filters import EmployeeFilter, ExitEmployeeFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
import datetime

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
    return render(request, 'hardware/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    return render(request, 'hardware/dashboard.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def onboading(request):
    return render(request, 'hardware/onboard.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def replace(request):
    return render(request, 'hardware/replace.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def exit_return(request):
    return render(request, 'hardware/exit.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employees(request):
    employees = Employee.objects.all()
    active_emps = Employee.objects.filter(emp_status = 'Active').count()
    inactive_emps = Employee.objects.filter(emp_status = 'InActive').count()

    myFilter = EmployeeFilter(request.GET, queryset=employees)
    employees = myFilter.qs

    context = {'active_emps': active_emps, 'inactive_emps': inactive_emps, 'employees': employees,
    'myFilter':myFilter}

    return render(request, 'hardware/dash_employees.html', context)

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
    return render(request, 'hardware/employee.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee_add(request):
    form = EmployeeForm()
    if request.method == "POST":
        #print(request.POST)
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dash_employees')

    context = {'form':form}
    return render(request, 'hardware/employee_add.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee_edit(request, pk):
    employee = Employee.objects.get(emp_id=pk)
    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('/dash_employees')

    context = {'form':form}
    return render(request, 'hardware/employee_add.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employee_del(request, pk):
    employee = Employee.objects.get(emp_id=pk)
    if request.method == "POST":
        employee.delete()
        return redirect('/dash_employees')

    context = {'employee':employee}
    return render(request, 'hardware/employee_del.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def laptops(request):
    available_laps = Laptop.objects.filter(hardware=None)
    assignable_laps = available_laps.filter(laptop_status='Working')
    repairable_laps = available_laps.filter(laptop_status='Repair')
    replaceable_laps = available_laps.filter(laptop_status='Replace')
    laps_in_use = Laptop.objects.filter(hardware__isnull=False)
    laps_for_repair = Laptop.objects.all().filter(laptop_status='Repair').count()
    laps_for_replace = Laptop.objects.all().filter(laptop_status='Replace').count()
    working_laps = Laptop.objects.all().filter(laptop_status='Working').count()

    context = {'laps_for_repair':laps_for_repair, 'laps_for_replace':laps_for_replace, 
    'working_laps':working_laps, 'available_laps':available_laps, 'laps_in_use':laps_in_use,
    'assignable_laps':assignable_laps, 'repairable_laps':repairable_laps, 'replaceable_laps':replaceable_laps }
    return render(request, 'hardware/dash_laptops.html', context)

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
    return render(request, 'hardware/laptop.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def laptop_add(request):
    form = LaptopForm()

    if request.method == 'POST':
        form = LaptopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dash_laptops')
    
    context = {'form' : form}
    return render(request, 'hardware/laptop_add.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def laptop_edit(request, pk):
    laptop = Laptop.objects.get(id=pk)
    form = LaptopForm(instance=laptop)

    if request.method == 'POST':
        form = LaptopForm(request.POST, instance=laptop)
        if form.is_valid():
            form.save()
            return redirect('/dash_laptops')

    context = {'form':form}
    return render(request, 'hardware/laptop_add.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def laptop_del(request, pk):
    laptop = Laptop.objects.get(id=pk)
    if request.method == 'POST':
        laptop.delete()
        return redirect('/dash_laptops')
    
    context = {'laptop':laptop}
    return render(request, 'hardware/laptop_del.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def onbrd_emp_add(request):
    form = OnboardEmployeeAddForm()
    if request.method == "POST":
        form = OnboardEmployeeAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added New Employee")
            return redirect('onbrd_hw_assign')
    context = {'form':form}
    return render(request, 'hardware/onbrd_emp_add.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def onbrd_hw_assign(request):
    
    latest_emp = Employee.objects.last()
    free_laptops = Laptop.objects.filter(laptop_location=latest_emp.loc_id, laptop_status='Working', emp_id=None)
    
    context = {'latest_emp':latest_emp, 'free_laptops':free_laptops}
    return render(request, 'hardware/onbrd_hw_assign.html', context)

def onbrd_complete(request, pk):
    laptop_assigned = Laptop.objects.get(id=pk)
    employee_to_assign = Employee.objects.last()
    print(employee_to_assign.emp_id)
    laptop_assigned.emp_id = employee_to_assign
    laptop_assigned.save()
    messages.success(request, f"{employee_to_assign} succesfully onboarded!")

    return redirect('employee', employee_to_assign.emp_id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee', 'admin'])
def employeeProfile(request):
    '''
    An 'employee self service' page where the employee can view all the hardware
    that have been assigned to him/her.
    '''
    laptop_assigned = Laptop.objects.get(emp_id=request.user.employee)
    print(laptop_assigned)
    hardwareType = Hardware._meta.get_field('hardware_id').remote_field.model.__name__
    context = {'laptop_assigned':laptop_assigned, 'hardwareType':hardwareType}
    return render(request, 'hardware/empprofile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee',])
def empSettingsPage(request):
    employee = request.user.employee
    form = EmployeeForm(instance=employee)

    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'hardware/empSettingsPage.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def emp_exit(request):
    employees = Employee.objects.filter(emp_status='Active')
    myExitFilter = ExitEmployeeFilter(request.GET, queryset=employees)
    employees = myExitFilter.qs

    context = {'myExitFilter':myExitFilter, 'employees':employees}
    return render(request, 'hardware/emp_exit.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def emp_exit_confirm(request, pk):
    employee_info = Employee.objects.get(emp_id=pk)
    laptop_assigned = Laptop.objects.get(emp_id=pk)
    hardware_type = Hardware._meta.get_field('hardware_id').remote_field.model.__name__

    laptop_exit_form = EmployeeExitFormLaptop(initial={'laptop_date_returned':'YYYY-DD-MM', 'laptop_return_remarks':''})
    laptop_exit_media_form = EmployeeExitFormLaptopImage(instance=laptop_assigned)

    if request.method == "POST":
        laptop_exit_form = EmployeeExitFormLaptop(request.POST, initial={'laptop_date_returned':datetime.date.today(), 'laptop_return_remarks':'Enter Any Remarks here'}, instance=laptop_assigned)
        laptop_exit_media_form = EmployeeExitFormLaptopImage(request.POST, request.FILES)
        if laptop_exit_form.is_valid() and laptop_exit_media_form.is_valid():
            laptop_assigned.media = laptop_exit_media_form.save()
            laptop_exit_form.save()
            laptop_exit_media_form.save()
            
            return redirect('emp_exit_complete', employee_info.emp_id)

    context = {'employee_info':employee_info, 'hardware_type':hardware_type,
    'laptop_assigned':laptop_assigned, 'laptop_exit_form':laptop_exit_form,
    'laptop_exit_media_form':laptop_exit_media_form}
    return render(request, 'hardware/emp_exit_confirm.html', context)

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
