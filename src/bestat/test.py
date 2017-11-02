from django.test import TestCase, Client
from bestat.models import Neighbor

class TodoListModelsTest(TestCase):
    def test_simple_add(self):
        self.assertTrue(Neighbor.objects.all().count() == 0)

