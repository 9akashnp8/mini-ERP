from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .decorators import  allowed_users
from .models import Laptop, Hardware
from .forms import LaptopForm, LaptopReturnForm
from .filters import LaptopFilter
from employee.models import Employee

from datetime import date
from environs import Env

env = Env()
env.read_env()

#Views
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
