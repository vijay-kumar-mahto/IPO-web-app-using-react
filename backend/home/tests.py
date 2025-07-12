from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ipo_app.models import Company, IPO


class HomeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create test companies
        self.company1 = Company.objects.create(company_name="Upcoming IPO Company")
        self.company2 = Company.objects.create(company_name="Open IPO Company")
        self.company3 = Company.objects.create(company_name="Listed IPO Company")
        
        # Create test IPOs
        self.upcoming_ipo = IPO.objects.create(
            company=self.company1,
            price_band="₹100-₹120",
            issue_size="₹500 Cr",
            status="Upcoming"
        )
        
        self.open_ipo = IPO.objects.create(
            company=self.company2,
            price_band="₹200-₹220",
            issue_size="₹1000 Cr",
            status="Open"
        )
        
        self.listed_ipo = IPO.objects.create(
            company=self.company3,
            price_band="₹300-₹320",
            issue_size="₹1500 Cr",
            status="Listed",
            ipo_price=310,
            listing_price=350,
            listing_gain=12.90,
            current_market_price=400,
            current_return=29.03
        )

    def test_home_api(self):
        url = reverse('home-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if all three categories are in the response
        self.assertIn('upcoming_ipos', response.data)
        self.assertIn('open_ipos', response.data)
        self.assertIn('listed_ipos', response.data)
        
        # Check if each category has the correct number of IPOs
        self.assertEqual(len(response.data['upcoming_ipos']), 1)
        self.assertEqual(len(response.data['open_ipos']), 1)
        self.assertEqual(len(response.data['listed_ipos']), 1)