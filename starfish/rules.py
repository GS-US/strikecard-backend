import rules
from chapters.models import ChapterRole

# Predicates for Chapter Permissions


@rules.predicate
def is_chapter_facilitator(user, chapter):
    if not user.is_authenticated:
        return False
    return ChapterRole.objects.filter(
        user=user, chapter=chapter, role='facilitator'
    ).exists()


@rules.predicate
def is_chapter_assistant(user, chapter):
    return ChapterRole.objects.filter(
        user=user, chapter=chapter, role='assistant'
    ).exists()


@rules.predicate
def is_chapter_member(user, chapter):
    return is_chapter_leader(user, chapter) or is_chapter_assistant(user, chapter)


# Permissions for Chapters
rules.add_perm('chapters.view_chapter', is_chapter_member)
rules.add_perm('chapters.change_chapter', is_chapter_facilitator)


@rules.predicate
def can_access_contact(user, contact):
    return ChapterRole.objects.filter(user=user, chapter=contact.chapter).exists()


# Permissions for Contacts
rules.add_perm('contacts.view_contact', can_access_contact)
rules.add_perm('contacts.add_contact', is_chapter_member)
rules.add_perm('contacts.change_contact', can_access_contact)
rules.add_perm('contacts.delete_contact', is_chapter_facilitator)
