from django.utils.text import camel_case_to_spaces


class BaseRole:
    key = None
    label = None

    def __init__(self, chapter=None):
        self.chapter = chapter
        super().__init__()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.key = camel_case_to_spaces(cls.__name__).replace(' ', '_')

    def has_perm(self, perm, obj=None):
        try:
            app_name, perm_name = perm.split('.')
        except ValueError:
            return False
        method_name = f'{app_name}_can_{perm_name}'
        return getattr(self, method_name, lambda obj: False)(obj=obj)

    def chapters_can_view_chapter(self, obj=None):
        return True

    def chapters_can_view_chapterrole(self, obj=None):
        return True

    def chapters_can_add_chapterrole(self):
        return False

    def chapters_can_change_chapterrole(self, obj=None):
        return False

    def chapters_can_delete_chapterrole(self, obj=None):
        return False

    def members_can_view_member(self, obj=None):
        return True

    def members_can_view_email(self, obj=None):
        return False

    def members_can_view_phone(self, obj=None):
        return False

    def members_can_change_member(self, obj=None):
        return False

    def chapters_can_add_owner(self, obj=None):
        return False

    def get_permitted_member_fields(self, obj=None):
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

    def members_can_view_email(self, obj=None):
        return True


class ReporterPhone(BaseRole):
    label = 'Reporter (Phone Only)'

    def members_can_view_phone(self, obj=None):
        return True


class Reporter(ReporterEmail, ReporterPhone):
    label = 'Reporter'


class Manager(Reporter):
    label = 'Manager'

    def members_can_change_member(self, member=None):
        return self.chapter == member.chapter

    def chapters_can_change_chapterrole(self, obj=None):
        return True

    def chapters_can_add_chapterrole(self, obj=None):
        return True


class Owner(Manager):
    label = 'Owner'

    def chapters_can_add_owner(self, obj=None):
        return True

    def chapters_can_delete_chapterrole(self, obj=None):
        return True


_ROLE_CLASSES = [ReporterEmail, ReporterPhone, Reporter, Manager, Owner]

ROLE_CLASSES = {cls.key: cls for cls in _ROLE_CLASSES}

ROLE_CHOICES = [(None, '---')] + [(cls.key, cls.label) for cls in _ROLE_CLASSES]


def get_role_instance(chapter_role):
    return ROLE_CLASSES.get(chapter_role.role_key)(chapter_role)
