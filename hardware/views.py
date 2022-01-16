from django.shortcuts import render, redirect
from .models import *
from .forms import EmployeeForm

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

    context = {'active_emps': active_emps, 'inactive_emps': inactive_emps, 'employees': employees}

    return render(request, 'hardware/dash_employees.html', context)

def employee(request, pk):
    employee_info = Employee.objects.get(emp_id=pk)

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

    context = {'employee_info': employee_info, 'changes':changes, 'edit_history':edit_history}
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
    return render(request, 'hardware/dash_laptops.html')