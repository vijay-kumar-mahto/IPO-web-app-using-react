from rest_framework import viewsets, permissions, filters
from .models import Broker
from .serializers import BrokerSerializer


class BrokerViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Broker instances."""
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['broker_name', 'description']
    ordering_fields = ['broker_name', 'min_account_size', 'created_at']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]