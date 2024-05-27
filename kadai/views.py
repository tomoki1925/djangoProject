from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from django.http import HttpResponse

def index(request):
    return render(request, 'static/../templates/index.html')

def loginTop(request):
    if request.method == 'POST':
        key = request.POST.get('user_id')
        password = request.POST.get('password')

        if not key or not password:
            return render(request, 'static/../templates/index.html', {'error_message': '入力してください'})

        try:
            employee = Employee.objects.get(empid=key)

        except Employee.DoesNotExist:
            return render(request, 'static/../templates/index.html', {'error_message': 'Invalid user ID or password.'})

        if password == employee.emppasswd:
            if employee.emprole == 1:
                request.session['user_id'] = employee.empid
                request.session['user_pass'] = employee.emppasswd
                return render(request, 'kanrisyaTop.html')
            elif employee.emprole == 2:
                request.session['user_id'] = employee.empid
                request.session['user_pass'] = employee.emppasswd
                return render(request, 'uketukeTop.html')
            elif employee.emprole == 1:
                request.session['user_id'] = employee.empid
                request.session['user_pass'] = employee.emppasswd
                return render(request, 'isiTop.html')
            else:
                return render(request, 'static/../templates/index.html', {'error_message': 'Access denied.'})
        else:
            return render(request, 'static/../templates/index.html', {'error_message': 'パスワードもしくはIDが違います'})
    else:
        return render(request, 'static/../templates/index.html')

def logout(request):
    # Clear session data
    request.session.flush()
    return redirect('index')