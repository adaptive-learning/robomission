from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from learn.models import Student


# TODO: Replace this test (instructions not used anymore) by tests for the
# current student API (start task, solve task, etc.)
#class StudentApiTestCase(APITestCase):
#    def create_authenticated_student(self):
#        user = User.objects.create(username='ada')
#        self.client.force_authenticate(user=user)
#        return user.student
#
#    def test_watch_instruction_adds_seen_instruction(self):
#        student = self.create_authenticated_student()
#        url = reverse('student-watch-instruction', kwargs={'pk': student.pk})
#        data = {'instruction': 'block.fly'}
#        response = self.client.post(url, data, format='json')
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        self.assertQuerysetEqual(
#            student.seen_instructions.all(),
#            ['<Instruction: block.fly>'])


class UserApiTestCase(APITestCase):
    def test_succesful_registration(self):
        data = {
            'username': 'a@b.com',
            'email': 'a@b.com',
            'password1': 'robomise',
            'password2': 'robomise'}
        response = self.client.post(
            '/rest-auth/registration/',
            data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='a@b.com')
        self.assertEqual(user.email, 'a@b.com')

    def test_succesful_login(self):
        user = User.objects.create_user('a@b.com', 'a@b.com', 'robomise')
        data = {
            'username': 'a@b.com',
            'email': 'a@b.com',
            'password': 'robomise'}
        response = self.client.post(
            '/rest-auth/login/',
            data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.data)

    def test_unsuccesful_login(self):
        data = {
            'username': 'a@b.com',
            'email': 'a@b.com',
            'password': 'robomise'}
        response = self.client.post(
            '/rest-auth/login/',
            data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
