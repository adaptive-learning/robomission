from django.contrib.auth.models import User
from lazysignup.decorators import allow_lazy_user
from lazysignup.models import LazyUser
from lazysignup.utils import is_lazy_user


@allow_lazy_user
def get_or_create_user(request):
    """Return a current user and create one if it doesn't exist

    Lazy user is generally created already when loading the frontend app.
    However, there are at least two cases when the frontend-app view is not
    loaded: one scenario is a manual testing through the browsable api, and
    second is FE development, when the home page is served from the FE server.
    """
    return request.user


def is_initial_user(user):
    return user.username == 'initial'


def get_initial_user():
    return User.objects.get(username='initial')


def get_or_fake_user(request):
    user = request.user
    if user.is_anonymous():
        return get_initial_user()
        #user.student = Student(pk='initial')
        #user.teacher = None
    return user


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
