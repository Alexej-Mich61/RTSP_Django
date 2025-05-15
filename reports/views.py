# reports/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_administrator(user):
    return user.is_authenticated and user.groups.filter(name='Administrators').exists()

@user_passes_test(is_administrator, login_url='/accounts/login/')
def reports(request):
    return render(request, 'reports/reports.html', {})
