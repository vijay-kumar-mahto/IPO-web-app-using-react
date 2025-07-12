from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ipo_app.models import IPO
from ipo_app.serializers import IPOSerializer


class HomeAPIView(APIView):
    """
    API view for the home page.
    Returns a summary of IPOs in different categories.
    """
    def get(self, request, format=None):
        upcoming_ipos = IPO.objects.filter(status='Upcoming').select_related('company')[:5]
        open_ipos = IPO.objects.filter(status='Open').select_related('company')[:5]
        listed_ipos = IPO.objects.filter(status='Listed').select_related('company').order_by('-listing_date')[:5]
        
        return Response({
            'upcoming_ipos': IPOSerializer(upcoming_ipos, many=True).data,
            'open_ipos': IPOSerializer(open_ipos, many=True).data,
            'listed_ipos': IPOSerializer(listed_ipos, many=True).data,
        }, status=status.HTTP_200_OK)