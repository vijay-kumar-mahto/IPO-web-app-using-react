from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Broker


class BrokerModelTest(TestCase):
    def setUp(self):
        Broker.objects.create(
            broker_name="Test Broker",
            website_url="https://testbroker.com",
            min_account_size=10000.00
        )

    def test_broker_creation(self):
        broker = Broker.objects.get(broker_name="Test Broker")
        self.assertEqual(broker.broker_name, "Test Broker")
        self.assertEqual(broker.website_url, "https://testbroker.com")
        self.assertEqual(float(broker.min_account_size), 10000.00)


class BrokerAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.broker = Broker.objects.create(
            broker_name="API Test Broker",
            website_url="https://apitestbroker.com",
            min_account_size=5000.00
        )

    def test_get_brokers(self):
        url = reverse('broker-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)