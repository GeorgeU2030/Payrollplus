from django import forms
from django.views.generic.edit import CreateView
from django.views import View
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm , CustomAuthenticationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date
from .models import Company,Payroll,Employee

# Create your views here.

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("authentication:signin")
    template_name = 'signup.html'

    def form_valid(self, form):
        # Obtener la instancia del usuario y establecer el archivo cargado en el campo adecuado
        user = form.save(commit=False)
        user.profilePicture = self.request.FILES['profilePicture']  # Obtener el archivo cargado

        # Guardar el usuario con el archivo cargado
        user.save()

        return super().form_valid(form)

class SignIn(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'

class Menu(CreateView):
    def get(self,request):
        
        try:
            company = request.user.id
            last_payroll = Payroll.objects.filter(company=company).latest('id')
            employees = last_payroll.employees
        except:
            last_payroll = None

        if last_payroll != None and employees!=None:
            totalpayroll = last_payroll.totalsalary+ last_payroll.totalbenefits+last_payroll.totalsecurity+last_payroll.totalparafiscal
            data = {'payroll':last_payroll, 'totalpayroll':totalpayroll}
            return render(request,'menu.html',data)
        
        return render(request,'menu.html')
    
class PayrollView(CreateView):
    def get(self, request):
        try:
            company = request.user.id
            last_payroll = Payroll.objects.filter(company=company).latest('id')
        except:
            last_payroll = None

        if last_payroll == None:    
            idcompany = request.user.id
            company = Company.objects.get(id=idcompany)
            payroll = Payroll(company=company)
            payroll.save()
            data = {'payroll':payroll}
            return render(request,'menu.html',data)
        elif last_payroll != None:
            totalpayroll = last_payroll.totalsalary+ last_payroll.totalbenefits+last_payroll.totalsecurity+last_payroll.totalparafiscal
            data = {'payroll':last_payroll, 'totalpayroll':totalpayroll}
            return render(request,'menu.html',data)
        
        return render(request,'menu.html')


class EmployeesView(CreateView):
    def get(self, request):
        idcompany = request.user.id
        employees = Employee.objects.filter(company=idcompany,state='Activo').order_by('last_name')
        data = {'employees': employees}
        return render(request, 'lookEmployees.html',data)
    

class AddEmployeeView(CreateView):
    def get(self, request):
        return render(request, 'addEmployee.html')
    

class LookPayrollView(CreateView):
    def get(self, request):
        try:
            company = request.user.id
            last_payroll = Payroll.objects.filter(company=company).latest('id')
            employees = last_payroll.employees.order_by('last_name')
            data = {'payroll':last_payroll, 'employees':employees}
            return render(request,'lookPayroll.html',data)
        except:
            last_payroll = None
        
        return render(request, 'lookPayroll.html')


class NewEmployeeView(View):
    def post(self, request):
        if request.method == 'POST':     
            nameemployee = request.POST.get('namein')
            lastname = request.POST.get('lastnamein')
            email = request.POST.get('emailin')
            phone = request.POST.get('phonein')
            datebirth = request.POST.get('datein')
            address = request.POST.get('addressin')
            position = request.POST.get('positionin')
            salary = request.POST.get('salaryin')
            workdays = request.POST.get('workdaysin')
            clasify = request.POST.get('clasificationin')
            clasification=''
            if clasify == 'Mano de Obra Directa':
                clasification='MOD'
            elif clasify == 'Mano de Obra Indirecta':
                clasification='MOI'

            workdays = int(workdays)
            salary = int(salary)
            op1 = salary*(workdays/30)
            opax=0
            if (salary<=1160000*2):
                opax = int(140606*(workdays/30))

            ts=op1+opax
            opd = int(op1*0.08)
            optts = ts-opd
            ops = int(ts*0.0833)
            opsp = int(ts*0.01)
            opv = int(op1*0.0417)
            optb = ops+ops+opsp+opv
            oph = 0
            if salary>=1160000*10:
                oph = int(op1*0.085)

            opp = int(op1*0.12)
            opa = int(op1*0.02436)
            opts = oph+opp+opa
            opbox = int(op1*0.04)
            opsena =0
            opicbf =0
            if salary >=1160000*10:
                opsena=int(op1*0.02)
                opicbf=int(op1*0.03)
            optp = opbox+opsena+opicbf

            idcompany = request.user.id
            company = Company.objects.get(id=idcompany)
            employee = Employee(name=nameemployee, last_name=lastname, email=email,phone=phone,date_birth=datebirth,
                                address=address,position=position,salary=salary,work_days=workdays, clasification=clasification,
                                company=company,salarydev=op1,transport_aux=opax,totalsalary=ts,
                                deduction=opd,totalpaysalary=optts,severance=ops,bonus=ops,
                                severance_pay=opsp,vacations=opv,totalbenefits=optb,health=oph,pension=opp,
                                ateb=opa,totalsecurity=opts,box=opbox,sena=opsena,icbf=opicbf,totalparafiscal=optp,state='Activo')
            employee.save()
            last_payroll = Payroll.objects.filter(company=company).latest('id')
            last_payroll.employees.add(employee)
            if employee.clasification =='MOD':
                last_payroll.salary_dl += employee.totalsalary
                last_payroll.benefits_dl += employee.totalbenefits
                last_payroll.security_dl += employee.totalsecurity
                last_payroll.parafiscal_dl += employee.totalparafiscal
            elif employee.clasification =='MOI':
                last_payroll.salary_il += employee.totalsalary
                last_payroll.benefits_il += employee.totalbenefits
                last_payroll.security_il += employee.totalsecurity
                last_payroll.parafiscal_il += employee.totalparafiscal

            last_payroll.totalsalary += employee.totalsalary
            last_payroll.totalbenefits += employee.totalbenefits
            last_payroll.totalsecurity += employee.totalsecurity
            last_payroll.totalparafiscal += employee.totalparafiscal
            last_payroll.save()
            data = {'response':'El Usuario se ha creado con exito'}
            return render(request,'addEmployee.html',data)
            
class SearchEmployeeView(View):
    def post(self, request):
        idcompany = request.user.id
        value = request.POST.get('searchem')
        employees = Employee.objects.filter(
            Q(name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value) |
            Q(phone__icontains=value) |
            Q(position__icontains=value) ,
            company = idcompany
        ).order_by('last_name')

        if employees:
            data = {'employees': employees}
            return render(request, 'lookEmployees.html', data)

        info = 'No tienes empleados con el criterio de búsqueda ingresado'
        return render(request, 'lookEmployees.html', {'info': info})


class EditEmployeeView(View):
    def get(self, request,id):
        employees = Employee.objects.filter(id=id).first()
        data = {'e':employees}
        return render(request,'editEmployee.html',data)


class FiredEmployeeView(View):
    def get(self,request,id):
        employee = Employee.objects.get(id=id)
        employee.state = 'Fired'
        employee.save()
        data = {'response':'El Usuario ha sido despedido'}
        return render(request,'addEmployee.html',data)


class UpdateEmployeeView(View):
    def post(self, request,id):
        if request.method == 'POST': 
            idcompany = request.user.id
            company = Company.objects.get(id=idcompany)
            last_payroll = Payroll.objects.filter(company=company).latest('id')
            employee = Employee.objects.get(id=id)  
           
            if employee.clasification =='MOD':
                last_payroll.salary_dl -= employee.totalsalary
                last_payroll.benefits_dl -= employee.totalbenefits
                last_payroll.security_dl -= employee.totalsecurity
                last_payroll.parafiscal_dl -= employee.totalparafiscal
            elif employee.clasification =='MOI':
                last_payroll.salary_il -= employee.totalsalary
                last_payroll.benefits_il -= employee.totalbenefits
                last_payroll.security_il -= employee.totalsecurity
                last_payroll.parafiscal_il -= employee.totalparafiscal

            last_payroll.totalsalary -= employee.totalsalary
            last_payroll.totalbenefits -= employee.totalbenefits
            last_payroll.totalsecurity -= employee.totalsecurity
            last_payroll.totalparafiscal -= employee.totalparafiscal
            last_payroll.save()
              
            employee.name = request.POST.get('namein')
            employee.last_name = request.POST.get('lastnamein')
            employee.email = request.POST.get('emailin')
            employee.phone = request.POST.get('phonein')
            employee.date_birth = request.POST.get('datein')
            employee.address = request.POST.get('addressin')
            employee.position = request.POST.get('positionin')
            employee.salary = request.POST.get('salaryin')
            employee.work_days = request.POST.get('workdaysin')
            clasify = request.POST.get('clasificationin')
            clasification=''
            if clasify == 'Mano de Obra Directa':
                employee.clasification='MOD'
            elif clasify == 'Mano de Obra Indirecta':
                employee.clasification='MOI'

            salary = request.POST.get('salaryin')
            workdays = request.POST.get('workdaysin')
            workdays = int(workdays)
            salary = int(salary)
            op1 = salary*(workdays/30)
            opax=0
            if (salary<=1160000*2):
                opax = int(140606*(workdays/30))

            ts=op1+opax
            opd = int(op1*0.08)
            optts = ts-opd
            ops = int(ts*0.0833)
            opsp = int(ts*0.01)
            opv = int(op1*0.0417)
            optb = ops+ops+opsp+opv
            oph = 0
            if salary>=1160000*10:
                oph = int(op1*0.085)

            opp = int(op1*0.12)
            opa = int(op1*0.02436)
            opts = oph+opp+opa
            opbox = int(op1*0.04)
            opsena =0
            opicbf =0
            if salary >=1160000*10:
                opsena=int(op1*0.02)
                opicbf=int(op1*0.03)
            optp = opbox+opsena+opicbf

            
            employee.salarydev=op1
            employee.transport_aux=opax
            employee.totalsalary=ts
            employee.deduction=opd
            employee.totalpaysalary=optts
            employee.severance=ops
            employee.bonus=ops
            employee.severance_pay=opsp
            employee.vacations=opv
            employee.totalbenefits=optb
            employee.health=oph
            employee.pension=opp
            employee.ateb=opa
            employee.totalsecurity=opts
            employee.box=opbox
            employee.sena=opsena
            employee.icbf=opicbf
            employee.totalparafiscal=optp
            employee.save()
            
            if employee.clasification =='MOD':
                last_payroll.salary_dl += employee.totalsalary
                last_payroll.benefits_dl += employee.totalbenefits
                last_payroll.security_dl += employee.totalsecurity
                last_payroll.parafiscal_dl += employee.totalparafiscal
            elif employee.clasification =='MOI':
                last_payroll.salary_il += employee.totalsalary
                last_payroll.benefits_il += employee.totalbenefits
                last_payroll.security_il += employee.totalsecurity
                last_payroll.parafiscal_il += employee.totalparafiscal

            last_payroll.totalsalary += employee.totalsalary
            last_payroll.totalbenefits += employee.totalbenefits
            last_payroll.totalsecurity += employee.totalsecurity
            last_payroll.totalparafiscal += employee.totalparafiscal
            last_payroll.save()
            data = {'response':'El Usuario se ha actualizado con exito'}
            return render(request,'addEmployee.html',data)

class SearchEmployee2View(View):
    def post(self, request):
        idcompany = request.user.id
        value = request.POST.get('searchem')
        employees = Employee.objects.filter(
            Q(name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(position__icontains=value),
            company = idcompany
        ).order_by('last_name')

        if employees:
            data = {'employees': employees}
            return render(request, 'lookPayroll.html', data)

        info = 'No tienes empleados con el criterio de búsqueda ingresado'
        return render(request, 'lookPayroll.html', {'info': info})
    

class OrderpayrollView(View):
    def get(self,request):
        company = request.user.id
        last_payroll = Payroll.objects.filter(company=company).latest('id')
        employees = last_payroll.employees.filter(state='Activo').order_by('-salary')
        data = {'payroll':last_payroll, 'employees':employees}
        return render(request,'lookPayroll.html',data)

class SendpayrollView(View):
    def get(self,request):
        idcompany = request.user.id
        company = Company.objects.get(id=idcompany)
        laspayroll = Payroll.objects.filter(company=company).latest('id')
        current_date = date.today()
        laspayroll.datepayroll = current_date
        laspayroll.save()
        payroll = Payroll(company=company)
        payroll.save()
        last_payroll = Payroll.objects.filter(company=company).latest('id')
        employees = laspayroll.employees.filter(state='Activo')

        for e in employees:
            if e.clasification =='MOD':
                last_payroll.salary_dl += e.totalsalary
                last_payroll.benefits_dl += e.totalbenefits
                last_payroll.security_dl += e.totalsecurity
                last_payroll.parafiscal_dl += e.totalparafiscal
            elif e.clasification =='MOI':
                last_payroll.salary_il += e.totalsalary
                last_payroll.benefits_il += e.totalbenefits
                last_payroll.security_il += e.totalsecurity
                last_payroll.parafiscal_il += e.totalparafiscal

            last_payroll.totalsalary += e.totalsalary
            last_payroll.totalbenefits += e.totalbenefits
            last_payroll.totalsecurity += e.totalsecurity
            last_payroll.totalparafiscal += e.totalparafiscal
            last_payroll.employees.add(e)
            last_payroll.save()

        
        totalpayroll = last_payroll.totalsalary+ last_payroll.totalbenefits+last_payroll.totalsecurity+last_payroll.totalparafiscal
        data = {'payroll':last_payroll, 'totalpayroll':totalpayroll}
        return render(request,'menu.html',data)
