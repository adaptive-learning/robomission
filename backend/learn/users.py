from lazysignup.models import LazyUser
from lazysignup.utils import is_lazy_user


def convert_lazy_user(lazy_user, new_user):
    assert is_lazy_user(lazy_user)
    rewire_student(lazy_user, new_user)
    delete_lazy_user(lazy_user)


def rewire_student(old_user, new_user):
    if hasattr(old_user, 'student'):
        student = old_user.student
        if hasattr(new_user, 'student'):
            new_user.student.delete()
        student.user = new_user
        student.save()


def delete_lazy_user(user):
    assert is_lazy_user(user)
    LazyUser.objects.filter(user=user).delete()
    user.delete()
