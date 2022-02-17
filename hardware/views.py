from django.shortcuts import render, redirect
from .models import *
from .forms import EmployeeForm, HardwareAssignmentForm, LaptopForm
from .filters import EmployeeFilter

def home(request):
    return render(request, 'hardware/dashboard.html')

def onboading(request):
    return render(request, 'hardware/onboard.html')

def replace(request):
    return render(request, 'hardware/replace.html')

def exit_return(request):
    return render(request, 'hardware/exit.html')

def employees(request):
    employees = Employee.objects.all()
    active_emps = Employee.objects.filter(emp_status = 'Active').count()
    inactive_emps = Employee.objects.filter(emp_status = 'InActive').count()

    myFilter = EmployeeFilter(request.GET, queryset=employees)
    employees = myFilter.qs

    context = {'active_emps': active_emps, 'inactive_emps': inactive_emps, 'employees': employees,
    'myFilter':myFilter}

    return render(request, 'hardware/dash_employees.html', context)

def employee(request, pk):
    employee_info = Employee.objects.get(emp_id=pk)
    hardwares_assigned = Hardware.objects.filter(emp_id=pk)
    hardware_type = Hardware._meta.get_field('hardware_id').remote_field.model.__name__
    qry = employee_info.history.all()

    def historical_changes(qry):
        changes = []
        if qry is not None:
            latest_edit= qry.first()
            for all_changes in range(qry.count()):
                new_record, old_record = latest_edit, latest_edit.prev_record
                if old_record is not None:
                    delta = new_record.diff_against(old_record)
                    changes.append(delta)
                latest_edit = new_record
                return changes

    edit_history = employee_info.history.all()

    changes = historical_changes(qry)

    context = {'employee_info': employee_info, 'hardwares_assigned':hardwares_assigned, 'hardware_type':hardware_type, 'changes':changes, 'edit_history':edit_history}
    return render(request, 'hardware/employee.html', context)

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

def employee_del(request, pk):
    employee = Employee.objects.get(emp_id=pk)
    if request.method == "POST":
        employee.delete()
        return redirect('/dash_employees')

    context = {'employee':employee}
    return render(request, 'hardware/employee_del.html', context)

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

def laptop(request, pk):
    laptop_info = Laptop.objects.get(id=pk)

    context = {'laptop_info': laptop_info}
    return render(request, 'hardware/laptop.html', context)

def laptop_add(request):
    form = LaptopForm()

    if request.method == 'POST':
        form = LaptopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dash_laptops')
    
    context = {'form' : form}
    return render(request, 'hardware/laptop_add.html', context)

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

def laptop_del(request, pk):
    laptop = Laptop.objects.get(id=pk)
    if request.method == 'POST':
        laptop.delete()
        return redirect('/dash_laptops')
    
    context = {'laptop':laptop}
    return render(request, 'hardware/laptop_del.html', context)

def onbrd_emp_add(request):
    form = EmployeeForm()
    if request.method == "POST":
        #print(request.POST)
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/onbrd_hw_assign')
    context = {'form':form}
    return render(request, 'hardware/onbrd_emp_add.html', context)

def onbrd_hw_assign(request, pk):
    employee = Employee.objects.get(emp_id=pk)
    form = HardwareAssignmentForm(initial={'emp_id':employee})
    if request.method == "POST":
        form = HardwareAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dash_employees')
    
    context = {'form':form}
    return render(request, 'hardware/onbrd_hw_assign.html', context)