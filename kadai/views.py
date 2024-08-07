from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee,Tabyouin,Patient,Medicine,Treatment
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.db import DataError
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from transformers import pipeline
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
    return render(request, 'index.html')


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
        if Employee.objects.filter(empid=id).exists():
            error_message = 'そのidはすでに登録されています'
            return render(request, 'ztouroku.html', {'error_message': error_message})
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
    newtels = request.POST.get('newtel')
    char_remove = "()-（）ー"
    table = str.maketrans('', '', char_remove)
    newtel = newtels.translate(table)
    if len(newtel) < 10:
        tabyouin = Tabyouin.objects.all()
        context = {
            'error_message':'正しく入力してください',
            'hospitals': tabyouin
        }
        return render(request, 'hospitalList.html', context)
    try:
        a = int(newtel)
    except ValueError:
        tabyouin = Tabyouin.objects.all()
        context = {
            'error_message': '正しく入力してください',
            'hospitals': tabyouin
        }
        return render(request, 'hospitalList.html', context)

    request.session['hospital_id'] = hospital_id
    request.session['newtel'] = newtels
    tabyouin = Tabyouin.objects.filter(tabyouinid=hospital_id)
    if not tabyouin.exists():
        tabyouin = Tabyouin.objects.all()
        context = {
            'error_message': 'idの入力に誤りがあります',
            'hospitals': tabyouin
        }
        return render(request, 'hospitalList.html', context)

    tabyou = Tabyouin.objects.get(tabyouinid=hospital_id)
    context = {
        'tabyouin': tabyou,
        'newtel': newtels
    }

    return render(request,'telLastCheck.html', context)


def telcomit(request):
    hospital_id = request.session['hospital_id']
    newtel = request.session['newtel']
    try:
        new_hospital = Tabyouin.objects.get(tabyouinid=hospital_id)
    except Employee.DoesNotExist:
        return render(request, 'hospitalList.html', {'error_message': '正しい他病院idを指定してください'})

    try:
        new_hospital.tabyouintel = newtel
        new_hospital.save()
        tabyouin = Tabyouin.objects.all()
        return render(request, 'hospitalList.html',{'hospitals':tabyouin})
    except DataError:
        tabyouin = Tabyouin.objects.all()
        context = {
            'error_message': '電話番号を入力してください',
            'hospitals': tabyouin
        }
        return render(request, 'hospitalList.html', context)


def CSearch(request):
    return render(request, 'capitalSearch.html')


def CSearch2(request):
    if request.method == 'POST':
        clower = request.POST.get('clower')
        char_remove = ",，￥"
        table = str.maketrans('', '', char_remove)
        newclower = clower.translate(table)
        if int(clower) < 0:
            return render(request, 'capitalSearch.html', {'error_message': '自然数を入力してください'})
        try:
            newclower = int(newclower)
        except ValueError:
            return render(request, 'capitalSearch.html',{'error_message': '数値を入力してください'})

        hospitals = Tabyouin.objects.filter(tabyouinshihonkin__gte=newclower)
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
    if not npass or not npass2:
        return render(request, 'kpassch.html', {'error_message': '入力もれがあります'})

    if npass == npass2:
        hashpass = make_password(npass)
    else:
        return render(request, 'kpassch.html',{'error_message': 'パスワードが一致しません'})

    try:
        emp = Employee.objects.get(empid=user_id)
        emp.emppasswd = hashpass
        emp.save()
        return render(request, 'chenge.html')
    except Employee.DoesNotExist:
        return render(request, 'error.html')


def uke_pass(request):
    user_id = request.session['user_id']
    npass = request.POST.get('npass')
    npass2 = request.POST.get('npass2')
    if not npass or not npass2:
        return render(request, 'upassch.html', {'error_message': '入力もれがあります'})
    if npass == npass2:
        hashpass = make_password(npass)
    else:
        return render(request, 'upassch.html', {'error_message': 'パスワードが一致しません'})
    try:
        emp = Employee.objects.get(empid=user_id)
        emp.emppasswd = hashpass
        emp.save()
        return render(request, 'ukechange.html')
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
        today = datetime.now().strftime('%Y-%m-%d')
        if not pid or not fname or not lname or not icn or not date:
            return render(request, 'patient.html', {'error_message': '入力もれがあります'})

        if Patient.objects.filter(patid=pid).exists():
            error_message = 'そのidはすでに登録されています'
            return render(request, 'patient.html', {'error_message': error_message})

        dates = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = dates.strftime('%Y-%m-%d')

        if formatted_date <= today:
            return render(request, 'patient.html', {'error_message': '過去の日にちは登録できません'})

        try:
            a = int(icn)
            if not len(icn) == 10:
                return render(request, 'patient.html', {'error_message': '保険番号は１０桁で入力してください'})
        except ValueError:
            return render(request, 'patient.html', {'error_message': '保険番号は数値で入力してください'})

        patient = Patient(patid=pid, patfname=fname, patlname=lname, hokenmei=icn, hokenexp=date)
        patient.save()
        return render(request, 'patilast.html')


def patich(request):
    patient = Patient.objects.all()
    return render(request, 'patiinfo.html',{'patients':patient})


def patich2(request,patid):
    patient = Patient.objects.get(patid=patid)
    request.session['patientid'] = patid
    return render(request,'patich.html',{'patient':patient})


def patient_ch(request):
    if request.method == 'POST':
        pid = request.session['patientid']
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
    try:
        a = int(icn)
        if not len(icn) == 10:
            pid = request.session['patientid']
            patient = Patient.objects.get(patid=pid)
            context = {
                'error_message': '保険証番号は１０桁でお願いします',
                'patient': patient
            }
            return render(request, 'patich.html', context)
    except ValueError:
        pid = request.session['patientid']
        patient = Patient.objects.get(patid=pid)
        context = {
            'error_message': '保険証番号をきちんと入力してください',
            'patient': patient
        }
        return render(request, 'patich.html', context)
    if icn != nowmei:
        if date == nowdate:
            pid = request.session['patientid']
            patient = Patient.objects.get(patid=pid)
            context = {
                'error_message': '保険証番号を変更する場合は期限も変更してください',
                'patient':patient
            }
            return render(request,'patich.html',context)
        else:
            if date <= nowdate:
                pid = request.session['patientid']
                patient = Patient.objects.get(patid=pid)
                context = {
                    'error_message': '現在の期限より前の日つけは登録できません',
                    'patient': patient
                }
                return render(request, 'patich.html', context)
            patient.hokenexp = date
            patient.hokenmei = icn
            patient.save()
            return render(request,'patilast.html')
    else:
        if date <= nowdate:
            pid = request.session['patientid']
            patient = Patient.objects.get(patid=pid)
            context = {
                'error_message': '現在の期限より前の日つけは登録できません',
                'patient': patient
            }
            return render(request, 'patich.html', context)
        patient.hokenexp = date
        patient.save()
        return render(request, 'patilast.html')


def patient_top(request):
    return render(request, 'uketukeTop.html')


def patserch(request):
    today = datetime.now().strftime('%Y-%m-%d')
    patients = Patient.objects.filter(hokenexp__lt=today)
    return render(request, 'patiserch.html', {'patients': patients})


def zpats(request):
    if request.method == 'POST':
        sei = request.POST.get('sei')
        mei = request.POST.get('mei')
        if sei and mei:
            sei = Patient.objects.filter(patfname__icontains=sei)
            mei = Patient.objects.filter(patlname__icontains=mei)
            if not sei.exists() and not mei.exists():
                return render(request, 'patizenken.html', {'error_message': '結果が見つかりません'})
            elif sei.exists():
                return render(request, 'patizenken.html', {'error_message': '結果が見つかりません'})
            elif mei.exists():
                return render(request, 'patizenken.html', {'error_message': '結果が見つかりません'})
            else:
                hul = Patient.objects.filter(patfname__icontains=sei, patlname__icontains=mei)
                return render(request, 'patizenken.html', {'patients': hul})
        elif not sei:
            mei = Patient.objects.filter(patlname__icontains=mei)
            if not mei.exists():
                return render(request, 'patizenken.html', {'error_message': '結果が見つかりません'})
            return render(request, 'patizenken.html', {'patients': mei})
        else:
            sei = Patient.objects.filter(patfname__icontains=sei)
            if not sei.exists():
                return render(request, 'patizenken.html', {'error_message': '結果が見つかりません'})
            return render(request, 'patizenken.html', {'patients': sei})

    else:
        return render(request, 'patizenken.html')


def patiidse(request):
    if request.method == 'POST':
        patient = request.POST.get('patient')
        pid = Patient.objects.filter(patid=patient)
        if not pid.exists():
            return render(request, 'patiidse.html', {'error_message': '結果が見つかりません'})
        return render(request, 'patiidse.html', {'patients': pid})
    else:
        return render(request, 'patiidse.html')


def zenken(request):
    patient = Patient.objects.all()
    return render(request, 'zenken.html',{'patients': patient})


def isi_top(request):
    return render(request, 'isiTop.html')


def drug(request,pid):
    request.session['dpatid'] = pid
    medicine = Medicine.objects.all()
    return render(request,'drug.html',{'medicines': medicine})


def drug_check(request):
    if request.method == 'POST':
        # if 'item_quantities' not in request.session:
        medicines_id = request.POST.getlist('select_medicine')
        item_quantities = {}
        sitem_quantities = {}

        try:
            for medicine_id in medicines_id:
                medicine = Medicine.objects.get(medicineid=medicine_id)
                quantity = request.POST.get(f'quan_{medicine_id}')
                if int(quantity) < 0:
                    medicine = Medicine.objects.all()
                    context = {
                        'medicines': medicine,
                        'error_message': '不正な数値です'
                    }
                    return render(request, 'drug.html', context)

                item_quantities[medicine] = int(quantity)
                sitem_quantities[medicine_id] = int(quantity)
            request.session['item_quantities'] = sitem_quantities
            return render(request,'drug_check.html',{'item_quantities': item_quantities})
        except ValueError:
            medicine = Medicine.objects.all()
            context = {
                'medicines':medicine,
                'error_message':'数量を入力してください'
            }
            return render(request, 'drug.html',context)
        # else:
        #     medicines_id = request.POST.getlist('select_medicine')
        #     item_quantities = {}
        #     sitem_quantities = {}
        #     ses = request.session.get('item_quantities',{})
        #     for medicine_id in medicines_id:
        #         quantity = request.POST.get(f'quan_{medicine_id}')
        #         sitem_quantities[medicine_id] = int(quantity)
        #     result = {key: ses[key] for key in ses if key not in sitem_quantities[key] }
        #     for key, value in result.items():
        #         sitem_quantities[key] = int(value)
        #
        #     request.session['item_quantities'] = sitem_quantities
        #     for item, quantity in sitem_quantities.items():
        #         medicine = Medicine.objects.get(medicineid=item)
        #         item_quantities[medicine] = quantity
        #     return render(request,'drug_check.html',{'item_quantities': item_quantities})
        #


def del_medicine(request,delid):
    del_quantities = {}
    after_quantity = {}
    item_quantities = request.session.get('item_quantities',{})
    del item_quantities[delid]
    for item, quantity in item_quantities.items():
        medicine = Medicine.objects.get(medicineid=item)
        del_quantities[medicine] = quantity
        after_quantity[item] = quantity
    request.session['item_quantities'] = after_quantity
    return render(request, 'drug_check.html', {'item_quantities': del_quantities})


def drug_top(request):
    medicine = Medicine.objects.all()
    return render(request,'drug.html',{'medicines': medicine})


def treatment(request):
    pid = request.session['dpatid']
    item_quantities = request.session.get('item_quantities', {})
    for key, value in item_quantities.items():
        medicine = Medicine.objects.get(medicineid=key)
        patient = Patient.objects.get(patid=pid)
        i = Treatment(patid=pid, patfname=patient.patfname, patlname=patient.patlname, medicineid=medicine.medicineid,
                      medicinename=medicine.medicinename,unit=medicine.unit , quantity=value)
        i.save()
    return render(request, 'isiTop.html')


def history(request):
    return render(request, 'history.html')


def treatment_history(request):
    patid = request.POST.get('pat_id')
    try:
        treatment = Treatment.objects.filter(patid=patid)
        if treatment:
            return render(request, 'pat_history.html', {'treatments': treatment})
        else:
            return render(request, 'history.html', {'error_message': 'その患者idの処置履歴はありません'})

    except Employee.DoesNotExist:
        return render(request, 'history.html', {'error_message': 'その患者idの処置履歴はありません'})


def sizengengo(request):
    if request.method == 'POST':
        pron = request.POST.get('pron')
        generator = pipeline('text-generation', model='gpt2')
        generated_text = generator(pron, max_length=50, num_return_sequences=1, truncation=True)
        generated_text = generated_text[0]
        generated_text = ''.join(str(value) for value in generated_text.values())
        char_remove = "{}n'￥"
        table = str.maketrans('', '', char_remove)
        generated_text = generated_text.translate(table)
        return render(request, 'sizengengo.html',{'message':generated_text})
    else:
        return render(request, 'sizengengo.html')










    






