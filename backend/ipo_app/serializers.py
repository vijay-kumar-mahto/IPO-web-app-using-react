from rest_framework import serializers
from .models import Company, IPO, Document


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for the Company model."""
    class Meta:
        model = Company
        fields = ['company_id', 'company_name', 'company_logo', 'created_at', 'updated_at']


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for the Document model."""
    class Meta:
        model = Document
        fields = ['document_id', 'ipo', 'rhp_pdf', 'drhp_pdf', 'created_at', 'updated_at']


class IPOSerializer(serializers.ModelSerializer):
    """Serializer for the IPO model."""
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(source='company', read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = IPO
        fields = [
            'ipo_id', 'company', 'company_id',
            'price_band', 'open_date', 'close_date', 'issue_size',
            'issue_type', 'listing_date', 'status', 'ipo_price',
            'listing_price', 'listing_gain', 'current_market_price',
            'current_return', 'documents', 'created_at', 'updated_at'
        ]


class IPODetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for the IPO model with nested company and document data."""
    company = CompanySerializer(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = IPO
        fields = [
            'ipo_id', 'company', 'price_band', 'open_date', 'close_date',
            'issue_size', 'issue_type', 'listing_date', 'status', 'ipo_price',
            'listing_price', 'listing_gain', 'current_market_price',
            'current_return', 'documents', 'created_at', 'updated_at'
        ]


class IPOCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating IPO records."""
    class Meta:
        model = IPO
        fields = [
            'ipo_id', 'company', 'price_band', 'open_date', 'close_date',
            'issue_size', 'issue_type', 'listing_date', 'status', 'ipo_price',
            'listing_price', 'listing_gain', 'current_market_price',
            'current_return', 'created_at', 'updated_at'
        ]
        read_only_fields = ['ipo_id', 'created_at', 'updated_at']
