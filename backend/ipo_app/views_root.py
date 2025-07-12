from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root view that provides links to all available endpoints.
    """
    return Response({
        'companies': reverse('company-list', request=request, format=format),
        'ipos': reverse('ipo-list', request=request, format=format),
        'upcoming_ipos': reverse('ipo-upcoming', request=request, format=format),
        'open_ipos': reverse('ipo-open', request=request, format=format),
        'listed_ipos': reverse('ipo-listed', request=request, format=format),
        'documents': reverse('document-list', request=request, format=format),
        'brokers': reverse('broker-list', request=request, format=format),
        'home': reverse('home-api', request=request, format=format),
        'admin': '/admin/',
    })