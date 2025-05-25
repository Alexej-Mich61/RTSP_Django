#users/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

def is_administrator(user):
    return user.is_authenticated and user.groups.filter(name='Administrators').exists()

@login_required
@user_passes_test(is_administrator, login_url='/users/login/')
def users(request):
    return render(request, 'users/users.html', {})