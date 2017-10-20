from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from learn.models import Student


class StudentApiTestCase(APITestCase):
    def create_authenticated_student(self):
        user = User.objects.create(username='ada')
        self.client.force_authenticate(user=user)
        return user.student

    def test_watch_instruction_adds_seen_instruction(self):
        student = self.create_authenticated_student()
        url = reverse('student-watch-instruction', kwargs={'pk': student.pk})
        data = {'instruction': 'block.fly'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(
            student.seen_instructions.all(),
            ['<Instruction: block.fly>'])
