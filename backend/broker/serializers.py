from rest_framework import serializers
from .models import Broker


class BrokerSerializer(serializers.ModelSerializer):
    """Serializer for the Broker model."""
    class Meta:
        model = Broker
        fields = [
            'broker_id', 'broker_name', 'broker_logo', 'website_url',
            'description', 'min_account_size', 'account_opening_link',
            'created_at', 'updated_at'
        ]