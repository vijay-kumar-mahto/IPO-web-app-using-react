from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Company, IPO, Document


class CompanyModelTest(TestCase):
    def setUp(self):
        Company.objects.create(company_name="Test Company")

    def test_company_creation(self):
        company = Company.objects.get(company_name="Test Company")
        self.assertEqual(company.company_name, "Test Company")


class IPOModelTest(TestCase):
    def setUp(self):
        company = Company.objects.create(company_name="Test Company")
        IPO.objects.create(
            company=company,
            price_band="₹100-₹120",
            issue_size="₹500 Cr",
            status="Upcoming"
        )

    def test_ipo_creation(self):
        ipo = IPO.objects.get(company__company_name="Test Company")
        self.assertEqual(ipo.price_band, "₹100-₹120")
        self.assertEqual(ipo.status, "Upcoming")


class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(company_name="API Test Company")
        self.ipo = IPO.objects.create(
            company=self.company,
            price_band="₹200-₹220",
            issue_size="₹1000 Cr",
            status="Open"
        )

    def test_get_companies(self):
        url = reverse('company-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_ipos(self):
        url = reverse('ipo-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)