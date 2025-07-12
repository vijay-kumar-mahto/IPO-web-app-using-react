from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Company, IPO, Document
from .serializers import (
    CompanySerializer,
    IPOSerializer,
    IPODetailSerializer,
    IPOCreateUpdateSerializer,
    DocumentSerializer
)


class CompanyViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Company instances."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company_name']
    ordering_fields = ['company_name', 'created_at']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class IPOViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing IPO instances."""
    queryset = IPO.objects.all().select_related('company')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'company__company_name']
    search_fields = ['company__company_name', 'issue_type']
    ordering_fields = ['open_date', 'close_date', 'listing_date', 'ipo_price', 'listing_gain', 'current_return']
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'retrieve':
            return IPODetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return IPOCreateUpdateSerializer
        return IPOSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False)
    def upcoming(self, request):
        """Return upcoming IPOs."""
        upcoming_ipos = IPO.objects.filter(status='Upcoming').select_related('company')
        serializer = self.get_serializer(upcoming_ipos, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def open(self, request):
        """Return open IPOs."""
        open_ipos = IPO.objects.filter(status='Open').select_related('company')
        serializer = self.get_serializer(open_ipos, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def listed(self, request):
        """Return listed IPOs."""
        listed_ipos = IPO.objects.filter(status='Listed').select_related('company')
        serializer = self.get_serializer(listed_ipos, many=True)
        return Response(serializer.data)


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Document instances."""
    queryset = Document.objects.all().select_related('ipo', 'ipo__company')
    serializer_class = DocumentSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]