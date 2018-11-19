from django.test import TestCase
from .models import Bucketlist
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

# Create your tests here.

class ModelTestCase(TestCase):
    def setUp(self):
        self.bucketlist_name="Write world class code"
        self.bucketlist = Bucketlist(name=self.bucketlist_name)

    def test_model_can_create_bucketlist(self):
        old_count = Bucketlist.objects.count()
        Bucketlist.objects.create()
        new_count = Bucketlist.objects.count()
        self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.bucketlist_data = {'name': 'Go to Ibiza'}
        self.response = self.client.post(
            reverse('create'),
            self.bucketlist_data,
            format="json")

    def test_api_can_create_a_bucketlist(self):
        """Test the api has bucket creation capability."""

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bucketlist.objects.count(), 1)

    def test_api_can_get_bucketlist(self):
        bucketlist = Bucketlist.objects.get()
        response=self.client.get(reverse('details', kwargs={'pk': bucketlist.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bucketlist)

    def test_api_can_update(self):
        bucketlist = Bucketlist.objects.get()
        change_bucketlist={'name':'somethingelse'}
        res = self.client.put(
            reverse('details', kwargs={'pk': bucketlist.id}),
            change_bucketlist, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_bucketlist(self):
        """Test the api can delete a bucketlist."""
        bucketlist = Bucketlist.objects.get()
        response = self.client.delete(
            reverse('details',
                kwargs={'pk': bucketlist.id}),
                format='json',
            follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bucketlist.objects.count(), 0)

