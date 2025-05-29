from django.apps import AppConfig

class ContactsConfig(AppConfig):
    name = 'contacts'

    def ready(self):
        import contacts.signals
