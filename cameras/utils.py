# cameras/utils.py
def is_administrator(user):
    return user.is_authenticated and user.groups.filter(name='Administrators').exists()