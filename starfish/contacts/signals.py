from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Contact, ExpungedContact


@receiver([post_save, post_delete], sender=Contact)
def update_chapter_total_on_contact_change(sender, instance, **kwargs):
    if instance.chapter:
        instance.chapter.update_total_contacts()


@receiver([post_save, post_delete], sender=ExpungedContact)
def update_chapter_total_on_expunged_contact_change(sender, instance, **kwargs):
    if instance.chapter:
        instance.chapter.update_total_contacts()
