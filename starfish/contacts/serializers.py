from partners.models import PartnerCampaign
from regions.models import Zip
from rest_framework import serializers

from .models import PendingContact, get_by_email


class PendingContactSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    zip_code = serializers.CharField(max_length=5)
    partner_slug = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = PendingContact
        fields = ['name', 'email', 'phone', 'zip_code', 'partner_slug']

    def validate_zip_code(self, value):
        try:
            return Zip.objects.get(code=value)
        except Zip.DoesNotExist:
            raise serializers.ValidationError('Please enter a valid 5-digit ZIP Code.')

    def validate_email(self, value):
        contact = get_by_email(value.strip())
        if contact:
            if isinstance(contact, PendingContact):
                contact.delete()
            else:
                raise serializers.ValidationError(
                    'The email address entered is already registered.'
                )
        return value

    def create(self, validated_data):
        partner_slug = validated_data.pop('partner_slug', None)
        if partner_slug:
            try:
                validated_data['partner_campaign'] = PartnerCampaign.objects.get(
                    slug=partner_slug
                )
            except PartnerCampaign.DoesNotExist:
                pass

        return PendingContact.objects.create(**validated_data)
