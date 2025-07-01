from django.utils.text import camel_case_to_spaces


class BaseRole:
    key = None
    label = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.key = camel_case_to_spaces(cls.__name__).replace(' ', '_')

    def can_view_email(self):
        return False

    def can_view_phone(self):
        return False

    def can_edit(self):
        return False

    def can_delete(self):
        return False

    def get_permitted_fields(self):
        fields = []
        if self.can_view_email():
            fields.append('email')
        if self.can_view_phone():
            fields.append('phone')
        return fields

    def __str__(self):
        return self.label


class ReporterEmail(BaseRole):
    label = 'Reporter (Email Only)'

    def can_view_email(self):
        return True


class ReporterPhone(BaseRole):
    label = 'Reporter (Phone Only)'

    def can_view_phone(self):
        return True


class Reporter(ReporterEmail, ReporterPhone):
    label = 'Reporter'


class Manager(Reporter):
    label = 'Manager'

    def can_edit(self):
        return True


class Owner(Manager):
    label = 'Owner'

    def can_delete(self):
        return True


ALL_ROLE_CLASSES = [ReporterEmail, ReporterPhone, Reporter, Manager, Owner]

ROLE_CLASSES = {cls.key: cls() for cls in ALL_ROLE_CLASSES}

ROLE_CHOICES = [(None, '---')] + [(cls.key, cls.label) for cls in ALL_ROLE_CLASSES]
print(ROLE_CHOICES)


def get_role_instance(role_key):
    return ROLE_CLASSES.get(role_key)


def get_user_chapter_role(user, chapter):
    from .models import ChapterRole

    if user.is_superuser:
        return Owner()
    try:
        return ChapterRole.objects.get(user=user, chapter=chapter).get_role_object()
    except ChapterRole.DoesNotExist:
        return None
