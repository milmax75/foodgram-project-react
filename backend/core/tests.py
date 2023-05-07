from http import HTTPStatus

from django.test import Client, TestCase


class StaticPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        'Project pages availability tests'
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.guest_client.get('/admin/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.guest_client.get('/recipes/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.guest_client.get('/favorite/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
