#
from django.urls import path
from employee.views import EmployeeView,HomeView, SalaryView, LoginView
app_name = 'employee'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('salary/', SalaryView.as_view(), name='salary'),
    path('employee/', EmployeeView.as_view(), name='employee'),
    path('login/', LoginView.as_view(), name='login')
]