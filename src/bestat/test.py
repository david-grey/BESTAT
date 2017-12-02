from django.test import TestCase, Client
from bestat.models import Neighbor


class TodoListTest(TestCase):
    # Seeds the test database with data we obtained
    # fixtures = ['sample-data']  # from python manage.py dumpdata

    def test_home_page(self):  # Tests that a GET request to home page
        client = Client()  # results in an HTTP 200 (OK) response.
        response = client.get('/bestat/')
        self.assertEqual(response.status_code, 200)

    # def test_city_page(self):  # Tests that a GET request to map
    #     client = Client()  # results in an HTTP 200 (OK) response.
    #     response = client.get('/bestat/map?name=Pittsburgh')
    #     self.assertEqual(response.status_code, 200)