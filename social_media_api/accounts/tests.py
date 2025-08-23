from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()


class AuthTests(APITestCase):
	def test_register_and_login(self):
		register_url = reverse('register')
		payload = {
			'username': 'tester',
			'email': 'tester@example.com',
			'password': 'StrongPass123!',
			'password2': 'StrongPass123!',
		}
		r = self.client.post(register_url, payload, format='json')
		self.assertEqual(r.status_code, status.HTTP_201_CREATED)
		self.assertIn('token', r.data)

		login_url = reverse('login')
		r2 = self.client.post(login_url, {'username': 'tester', 'password': 'StrongPass123!'}, format='json')
		self.assertEqual(r2.status_code, status.HTTP_200_OK)
		self.assertIn('token', r2.data)

		# profile
		token = r2.data['token']
		self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
		profile_url = reverse('profile')
		r3 = self.client.get(profile_url)
		self.assertEqual(r3.status_code, status.HTTP_200_OK)
from django.test import TestCase

# Create your tests here.
