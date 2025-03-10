from django.db import models
from django.conf import settings


class LarkProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar_url = models.URLField(blank=True, null=True)
    open_id = models.CharField(max_length=255, unique=True)
    access_token = models.CharField(max_length=255)

    class Meta:
        db_table = 'lark_profile'

    def __str__(self):
        return f"Profile for {self.user.username}"
