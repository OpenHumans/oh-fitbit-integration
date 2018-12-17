from django.db import models
from django.conf import settings
from open_humans.models import OpenHumansMember
from datetime import timedelta
import requests
import arrow


class GoogleFitMember(models.Model):
    """
    Store OAuth2 data for a GoogleFit Member.
    This is a one to one relationship with a OpenHumansMember object.
    """
    user = models.OneToOneField(OpenHumansMember, related_name="googlefit_member", on_delete=models.CASCADE)
    userid = models.CharField(max_length=255, unique=True, null=True)
    access_token = models.CharField(max_length=512)
    refresh_token = models.CharField(max_length=512)
    expires_in = models.CharField(max_length=512)
    scope = models.CharField(max_length=512)
    token_type = models.CharField(max_length=512)
    last_updated = models.DateTimeField(
                            default=(arrow.now() - timedelta(days=7)).format())
    last_submitted = models.DateTimeField(
                            default=(arrow.now() - timedelta(days=7)).format())

    @staticmethod
    def get_expiration(expires_in):
        return (arrow.now() + timedelta(seconds=expires_in)).format()

    def get_access_token(self,
                         client_id=settings.FITBIT_CLIENT_ID,
                         client_secret=settings.FITBIT_CLIENT_SECRET):
        """
        Return access token. Refresh first if necessary.
        """
        # Also refresh if nearly expired (less than 60s remaining).
        delta = timedelta(seconds=60)
        if arrow.get(self.expires_in) - delta < arrow.now():
            self._refresh_tokens()
        return self.access_token

    def _refresh_tokens(self):
        """
        Refresh access token.
        """
        print("calling refresh token method in class")
        response = requests.post(
            'https://api.googlefit.com/oauth2/token',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token},
            auth=requests.auth.HTTPBasicAuth(
                settings.FITBIT_CLIENT_ID, settings.FITBIT_CLIENT_SECRET))
        print(response.text)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']
            self.token_expires = self.get_expiration(data['expires_in'])
            self.scope = data['scope']
            self.userid = data['user_id']
            self.save()
            return True
        return False
