from import_export import resources
from members.models import Member


class MemberResource(resources.ModelResource):
    zip_code = resources.Field(attribute='zip_code', column_name='ZIP')
    chapter__title = resources.Field(attribute='chapter__title', column_name='Chapter')
    partner_campaign__name = resources.Field(
        attribute='partner_campaign__name', column_name='Partner'
    )

    class Meta:
        model = Member
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
