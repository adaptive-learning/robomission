from learn.models import Block, Toolbox, Student
from learn.serializers import BlockSerializer
from learn.serializers import ToolboxSerializer
from learn.serializers import StudentSerializer
from rest_framework import generics


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


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

