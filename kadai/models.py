from django.db import models
# 他病院テーブル
class Tabyouin(models.Model):
    tabyouinid = models.CharField(max_length=8, primary_key=True)
    tabyouinmei = models.CharField(max_length=64)
    tabyouinaddress = models.CharField(max_length=64)
    tabyouintel = models.CharField(max_length=15)
    tabyouinshihonkin = models.IntegerField()
    kyukyu = models.IntegerField(choices=((1, '救急対応'), (2, '非救急')))

# 仕入れ先テーブル
class Shiiregyosha(models.Model):
    shiireid = models.CharField(max_length=8, primary_key=True)
    shiiremei = models.CharField(max_length=64)
    shiireaddress = models.CharField(max_length=64)
    shiiretel = models.CharField(max_length=15)
    shihonkin = models.IntegerField()
    nouki = models.IntegerField()

# 従業員テーブル
class Employee(models.Model):
    empid = models.CharField(max_length=8, primary_key=True)
    empfname = models.CharField(max_length=64)
    emplname = models.CharField(max_length=64)
    emppasswd = models.CharField(max_length=256)  # パスワードのハッシュ化は別途処理が必要
    emprole = models.IntegerField(choices=((1, '受付'), (2, '医師')))

# 患者テーブル
class Patient(models.Model):
    patid = models.CharField(max_length=8, primary_key=True)
    patfname = models.CharField(max_length=64)
    patlname = models.CharField(max_length=64)
    hokenmei = models.CharField(max_length=64)
    hokenexp = models.DateField()

# 薬剤テーブル
class Medicine(models.Model):
    medicineid = models.CharField(max_length=8, primary_key=True)
    medicinename = models.CharField(max_length=64)
    unit = models.CharField(max_length=8)

class Treatment(models.Model):
    patid = models.CharField(max_length=8)
    patfname = models.CharField(max_length=64)
    patlname = models.CharField(max_length=64)
    medicineid = models.CharField(max_length=8)
    medicinename = models.CharField(max_length=64)
    unit = models.CharField(max_length=8)
    quantity = models.IntegerField()

