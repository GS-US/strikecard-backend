from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import ExpungedMember, Member


@receiver([post_save, post_delete], sender=Member)
def update_chapter_total_on_member_change(sender, instance, **kwargs):
    if instance.chapter:
        instance.chapter.update_total_members()


@receiver([post_save, post_delete], sender=ExpungedMember)
def update_chapter_total_on_expunged_member_change(sender, instance, **kwargs):
    if instance.chapter:
        instance.chapter.update_total_members()
