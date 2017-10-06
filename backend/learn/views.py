from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from learn.models import Block, Toolbox, Student
from learn.permissions import IsOwnerOrStaff
from learn.serializers import BlockSerializer
from learn.serializers import StudentSerializer
from learn.serializers import ToolboxSerializer
from learn.serializers import UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'students': reverse('student-list', request=request, format=format)
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BlockList(generics.ListCreateAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class BlockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class ToolboxList(generics.ListCreateAPIView):
    queryset = Toolbox.objects.all()
    serializer_class = ToolboxSerializer


class ToolboxDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Toolbox.objects.all()
    serializer_class = ToolboxSerializer


class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrStaff)


class PracticeOverview(generics.GenericAPIView):
    queryset = Student.objects.all()

    def get(self, request, *args, **kwargs):
        student = self.get_object()
        return Response(
            'there will be a practice overview for student {s}'.format(s=student))
