import rules

# Predicates for Chapter Permissions


@rules.predicate
def is_chapter_facilitator(user, chapter):
    if not user.is_authenticated:
        return False
    return user.is_chapter_facilitator(chapter)


@rules.predicate
def is_chapter_assistant(user, chapter):
    if not user.is_authenticated:
        return False
    return user.is_chapter_assistant(chapter)


@rules.predicate
def is_chapter_member(user, chapter):
    if not user.is_authenticated:
        return False
    return user.is_chapter_member(chapter)


rules.add_perm('chapters.view_chapter', is_chapter_member)
rules.add_perm('chapters.change_chapter', is_chapter_facilitator)


@rules.predicate
def can_access_contact(user, contact):
    if not user.is_authenticated:
        return False
    return user.is_chapter_member(contact.chapter)


rules.add_perm('contacts.view_contact', can_access_contact)
rules.add_perm('contacts.add_contact', is_chapter_member)
rules.add_perm('contacts.change_contact', can_access_contact)
rules.add_perm('contacts.delete_contact', is_chapter_facilitator)
