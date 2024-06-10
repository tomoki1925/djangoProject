from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee,Tabyouin,Patient
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def loginTop(request):
    if request.method == 'POST':
        key = request.POST.get('user_id')
        password = request.POST.get('password')

        if not key or not password:
            return render(request, 'index.html', {'error_message': '入力してください'})

        try:
            employee = Employee.objects.get(empid=key)

        except Employee.DoesNotExist:
            return render(request, 'index.html', {'error_message': 'Invalid user ID or password.'})

        if password == employee.emppasswd:
            if employee.emprole == 3:
                request.session['user_id'] = employee.empid
                request.session['user_pass'] = employee.emppasswd
                request.session['user_role'] = employee.emprole
                return render(request, 'kanrisyaTop.html')

        if check_password(password, employee.emppasswd):

            if employee.emprole == 1:
                request.session['user_id'] = employee.empid
                request.session['user_pass'] = employee.emppasswd
                request.session['user_role'] = employee.emprole
                return render(request, 'uketukeTop.html')
            elif employee.emprole == 2:
                request.session['user_id'] = employee.empid
                request.session['user_pass'] = employee.emppasswd
                request.session['user_role'] = employee.emprole
                return render(request, 'isiTop.html')
            else:
                return render(request, 'index.html', {'error_message': 'Access denied.'})
        else:
            return render(request, 'index.html', {'error_message': 'パスワードもしくはIDが違います'})
    else:
        return render(request, 'index.html')


def logout(request):
    # Clear session data
    request.session.flush()
    return redirect('index')


def employee(request):
    return render(request, 'ztouroku.html')


def employee_check(request):
    if request.method == 'POST':
        uid = request.POST.get('userid')
        fname = request.POST.get('farstname')
        lname = request.POST.get('lastname')
        passwd = request.POST.get('passwd')
        passwd2 = request.POST.get('passwd2')
        role = request.POST.get('role')
        if passwd != passwd2:
            return render(request, 'ztouroku.html', {'error_pass_message': '入力したパスワードが一致しません'})

        request.session['uid'] = uid
        request.session['fname'] = fname
        request.session['lnamee'] = lname
        request.session['passwd'] = passwd
        request.session['role'] = role
        if role == 2:
            role = '医師'
        else:
            role = '受付'
        if not uid or not fname or not lname or not passwd or not role:
            return render(request, 'ztouroku.html', {'error_message': '入力してください'})
        context = {
            'uid': uid,
            'fname': fname,
            'lname': lname,
            'passwd': passwd,
            'role': role
        }

        return render(request, 'tourokucheck.html', context)

    else:
        id = request.session['uid']
        fname = request.session['fname']
        lname = request.session['lnamee']
        passwd = request.session['passwd']
        role = request.session['role']
        hashed_password = make_password(passwd)
        try:
            employee_form = Employee(empid=id, empfname=fname, emplname=lname, emppasswd=hashed_password, emprole=role)
            employee_form.save()
            return render(request, 'tourokufinish.html')
        except IntegrityError:
            return render(request,'error.html')


def employee_back(request):
    return render(request, 'kanrisyaTop.html')


def hospital_list(request):
    tabyouin  = Tabyouin.objects.all()
    return render(request, 'hospitalList.html',{'hospitals':tabyouin})


def telcheck(request):
    hospital_id = request.POST.get('hospital_id')
    newtel = request.POST.get('newtel')
    request.session['hospital_id'] = hospital_id
    request.session['newtel'] = newtel
    tabyouin = Tabyouin.objects.get(tabyouinid=hospital_id)
    context = {
        'tabyouin': tabyouin,
        'newtel': newtel
    }
    return render(request,'telLastCheck.html',context)


def telcomit(request):
    hospital_id = request.session['hospital_id']
    newtel = request.session['newtel']
    try:
        new_hospital = Tabyouin.objects.get(tabyouinid=hospital_id)
    except Employee.DoesNotExist:
        return render(request, 'hospitalList.html', {'error_message': '正しい他病院idを指定してください'})
    new_hospital.tabyouintel = newtel
    new_hospital.save()
    tabyouin = Tabyouin.objects.all()
    return render(request, 'hospitalList.html',{'hospitals':tabyouin})


def CSearch(request):
    return render(request, 'capitalSearch.html')


def CSearch2(request):
    if request.method == 'POST':
        clower = request.POST.get('clower')
        hospitals = Tabyouin.objects.filter(tabyouinshihonkin__gte=clower)
        return render(request, 'capitalSearch.html', {'hospitals':hospitals})


def emppass(request):
    a = request.session['user_role']
    if a == 3:
        return render(request, 'kpassch.html')
    else:
        return render(request,'upassch.html')


def manager_pass(request):
    user_id = request.POST.get('user_id')
    npass = request.POST.get('npass')
    npass2 = request.POST.get('npass2')
    if npass == npass2:
        hashpass = make_password(npass)
    else:
        return render(request, 'kpassch.html',{'error_message': 'パスワードが一致しません'})

    try:
        emp = Employee.objects.get(empid=user_id)
        emp.emppasswd = hashpass
        emp.save()
        return render(request, 'kanrisyaTop.html')
    except Employee.DoesNotExist:
        return render(request, 'error.html')


def uke_pass(request):
    user_id = request.session['user_id']
    npass = request.POST.get('npass')
    npass2 = request.POST.get('npass2')
    if npass == npass2:
        hashpass = make_password(npass)
    else:
        return render(request, 'upassch.html', {'error_message': 'パスワードが一致しません'})
    try:
        emp = Employee.objects.get(empid=user_id)
        emp.emppasswd = hashpass
        emp.save()
        return render(request, 'uketukeTop.html')
    except Employee.DoesNotExist:
        return render(request, 'error.html')


def patiReg(request):
    return render(request, 'patient.html')


def patient_reg(request):
    if request.method == 'POST':
        pid = request.POST.get('pati_id')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        icn = request.POST.get('icn')
        date = request.POST.get('date')
        patient = Patient(patid=pid, patfname=fname, patlname=lname, hokenmei=icn, hokenexp=date)
        patient.save()
        return render(request, 'uketukeTop.html')


def patich(request):
    patient = Patient.objects.all()
    return render(request, 'patiinfo.html',{'patients':patient})


def patich2(request,patid):
    patient = Patient.objects.get(patid=patid)
    return render(request,'patich.html',{'patient':patient})


def patient_ch(request):
    if request.method == 'POST':
        pid = request.POST.get('pati_id')
        icn = request.POST.get('icn')
        date = request.POST.get('date')
        context={
            'icn':icn,
            'date':date,
            'pid':pid
        }
        return render(request,'paticheck.html',context)


def patient_dec(request):
    pid = request.POST.get('pid')
    icn = request.POST.get('icn')
    date = request.POST.get('date')
    patient = Patient.objects.get(patid=pid)
    nowdate = patient.hokenexp.strftime('%Y-%m-%d')
    nowmei = patient.hokenmei
    if icn != nowmei:
        if date == nowdate:
            return render(request,'patich.html',{'error_message':'保険証番号を変更する場合は期限も変更してください'})
        else:
            patient.hokenexp = date
            patient.hokenmei = icn
            patient.save()
            return render(request,'patilast.html')
    else:
        patient.hokenexp = date
        patient.save()
        return render(request, 'patilast.html')


def patient_top(request):
    return render(request, 'uketukeTop.html')


















