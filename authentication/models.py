from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

# Create your models here.

class Company(AbstractBaseUser, PermissionsMixin):
    username=None
    email = models.EmailField(_("email address"), unique=True)
    name=models.CharField(max_length=100,null=False)
    profilePicture= models.ImageField(upload_to="users/",null=True, blank=True, default='profile_default.png')
    address=models.CharField(max_length=100,null=False)
    city=models.CharField(max_length=100,null=False)
    website=models.CharField(max_length=255,null=False)
    identification=models.CharField(max_length=30,null=False)
    typecompany = models.CharField(max_length=30,null=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login= models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    contact = models.CharField(max_length=15)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
   
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email
     
    def has_module_perms(self, app_label):
       return self.is_superuser
    def has_perm(self, perm, obj=None):
       return self.is_superuser
    
    class Meta:
        verbose_name_plural = 'Companies'


class Employee(models.Model):
    name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    date_birth = models.DateField(null=False)
    address = models.CharField(max_length=300)
    position = models.CharField(max_length=300)
    salary = models.BigIntegerField()
    work_days = models.IntegerField()
    clasopt = (('MOI','MOI'),
                ('MOD','MOD'))
    clasification = models.CharField(max_length=30,choices=clasopt,null=False)
    state = models.CharField(max_length=300)
    salarydev = models.BigIntegerField(default=0)
    deduction = models.BigIntegerField(default=0)
    totalpaysalary = models.BigIntegerField(default=0)
    transport_aux = models.BigIntegerField(default=0)
    totalsalary = models.BigIntegerField(default=0)
    severance = models.BigIntegerField(default=0)
    bonus = models.BigIntegerField(default=0)
    severance_pay = models.BigIntegerField(default=0)
    vacations = models.BigIntegerField(default=0)
    totalbenefits = models.BigIntegerField(default=0)
    health = models.BigIntegerField(default=0)
    pension = models.BigIntegerField(default=0)
    ateb = models.BigIntegerField(default=0)
    totalsecurity = models.BigIntegerField(default=0)
    box = models.BigIntegerField(default=0)
    sena = models.BigIntegerField(default=0)
    icbf = models.BigIntegerField(default=0)
    totalparafiscal = models.BigIntegerField(default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False)

class Payroll(models.Model):
    salary_dl = models.BigIntegerField(default=0)
    salary_il = models.BigIntegerField(default=0) 
    benefits_dl = models.BigIntegerField(default=0)
    benefits_il = models.BigIntegerField(default=0)
    security_dl = models.BigIntegerField(default=0)
    security_il = models.BigIntegerField(default=0)
    parafiscal_dl = models.BigIntegerField(default=0)
    parafiscal_il = models.BigIntegerField(default=0)
    totalsalary = models.BigIntegerField(default=0)
    totalbenefits = models.BigIntegerField(default=0)
    totalsecurity = models.BigIntegerField(default=0)
    totalparafiscal = models.BigIntegerField(default=0)
    datepayroll = models.DateField(auto_now_add=True)
    employees = models.ManyToManyField(Employee)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False)

