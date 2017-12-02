from django.test import TestCase, Client
from bestat.models import City
from django.contrib.gis.geos import Point


class BestatModelsTest(TestCase):
    def test_city_add(self):  # Tests database connection
        self.assertTrue(City.objects.all().count() == 0)
        new_city = City(name='test city',
                        point=Point(0,0),
                        activate=1,
                        population=1000)
        new_city.save()
        self.assertTrue(City.objects.all().count() == 1)
        self.assertTrue(City.objects.get(name='test city'))


class BestatTest(TestCase):
    def test_home_page(self):  # Tests that a GET request to home page
        client = Client()  # results in an HTTP 200 (OK) response.
        response = client.get('/bestat/')
        self.assertEqual(response.status_code, 200)

    def test_city_page(self):  # Tests that a GET request to map
        client = Client()  # results in an HTTP 200 (OK) response.
        response = client.get('/bestat/map/?name=Pittsburgh')
        self.assertEqual(response.status_code, 200)