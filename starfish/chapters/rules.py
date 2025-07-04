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

rules.add_perm('members.view_member', is_chapter_member)
rules.add_perm('members.add_member', is_chapter_member)
rules.add_perm('members.change_member', is_chapter_facilitator)
rules.add_perm('members.delete_member', is_chapter_facilitator)
