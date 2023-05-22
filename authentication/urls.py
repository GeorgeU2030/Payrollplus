from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [ path("signin/", views.SignIn.as_view(),name="signin"), 
                path("signup/", views.SignUp.as_view(),name="signup"),
                path("menu/", views.Menu.as_view(),name="menu"),
                path("createpayroll/", views.PayrollView.as_view(),name="createpayroll"),
                path("lookemployees/", views.EmployeesView.as_view(),name="lookemployees"),
                path("addEmployee/", views.AddEmployeeView.as_view(),name="addemployee"),
                path("newEmployee/", views.NewEmployeeView.as_view(),name="newemployee"),
                path("lookpayroll/", views.LookPayrollView.as_view(),name="lookpayroll"),
                path("searchemployee/", views.SearchEmployeeView.as_view(),name="searchemployee"),
                path("searchemployee2/", views.SearchEmployee2View.as_view(),name="searchemployee2"),
                path("orderpayroll/", views.OrderpayrollView.as_view(),name="orderpayroll"),
                path("editemployee/<int:id>/", views.EditEmployeeView.as_view(),name="editemployee"),
                path("updateemployee/<int:id>/", views.UpdateEmployeeView.as_view(),name="updateemployee"),
                path("sendpayroll/", views.SendpayrollView.as_view(),name="sendpayroll"),
                path("firedemployee/<int:id>/", views.FiredEmployeeView.as_view(),name="firedemployee"),
                ]