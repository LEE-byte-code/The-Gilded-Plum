from django.test import TestCase
from django.urls import reverse


class MenuAPITest(TestCase):
    def test_menu_list(self):
        resp = self.client.get(reverse('api-menu'))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreater(len(data['data']), 0)

    def test_gallery_list(self):
        resp = self.client.get(reverse('api-gallery'))
        self.assertEqual(resp.status_code, 200)

    def test_chef_table(self):
        resp = self.client.get(reverse('api-chef-table'))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('availableSeats', data)
