from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter that disables regular signup forms
    but allows OAuth signup through social accounts.
    """

    def is_open_for_signup(self, request):
        """
        Disable regular signup forms - only allow OAuth signup.
        """
        return False


class DevAccountAdapter(DefaultAccountAdapter):
    """
    Development account adapter that allows both regular signup forms
    and OAuth signup through social accounts.
    """

    def is_open_for_signup(self, request):
        """
        Allow regular signup forms in development.
        """
        return True


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter that handles OAuth signup.
    """

    def is_open_for_signup(self, request, sociallogin):
        """
        Allow OAuth signup for new users.
        """
        return True

    def pre_social_login(self, request, sociallogin):
        """
        Handle pre-social login logic.
        """
        # This method is called before the social login is processed
        # You can add custom logic here if needed
        pass

    def populate_user(self, request, sociallogin, data):
        """
        Populate user data from social login.
        """
        user = super().populate_user(request, sociallogin, data)

        # Set username from social account if not provided
        if not user.username:
            if sociallogin.account.provider == 'google':
                # Use email as username for Google
                user.username = data.get('email', '').split('@')[0]
            elif sociallogin.account.provider == 'discord':
                # Use Discord username
                user.username = data.get('username', '')

        return user
