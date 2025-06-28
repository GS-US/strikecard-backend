from rest_framework import serializers
from .models import PendingContact, get_by_email
from regions.models import Zip
from partners.models import PartnerCampaign


class PendingContactSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    zip_code = serializers.CharField(max_length=5)
    partner_slug = serializers.CharField(max_length=255, required=False, write_only=True)

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
        zip_code = validated_data.pop('zip_code')
        validated_data['zip_code'] = Zip.objects.get(code=zip_code)
        pending_contact = PendingContact.objects.create(**validated_data)
        return pending_contact
