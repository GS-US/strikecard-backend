import rules


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

rules.add_perm('contacts.view_contact', is_chapter_member)
rules.add_perm('contacts.add_contact', is_chapter_member)
rules.add_perm('contacts.change_contact', is_chapter_facilitator)
rules.add_perm('contacts.delete_contact', is_chapter_facilitator)
