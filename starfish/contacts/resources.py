from import_export import resources

from contacts.models import Contact


class ContactResource(resources.ModelResource):

    class Meta:
        model = Contact
        fields = (
            'name',
            'email',
            'phone',
            'zip_code',
            'chapter__title',
            'partner_campaign__name',
            'validated',
        )

    def get_import_fields(self):
        return (self.fields[f] for f in ['name', 'email', 'phone', 'zip_code'])
