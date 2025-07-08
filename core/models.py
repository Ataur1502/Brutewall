from django.db import models
from django.utils import timezone
from datetime import timedelta

class IPAttempt(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)
    blocked = models.BooleanField(default=False)
    blocked_until = models.DateTimeField(null=True, blank=True)

    def is_temporarily_blocked(self):
        if self.blocked and self.blocked_until:
            return timezone.now() < self.blocked_until
        return False

    def unblock_if_expired(self):
        if self.blocked and self.blocked_until and timezone.now() >= self.blocked_until:
            self.blocked = False
            self.attempts = 0
            self.blocked_until = None
            self.save()

    def __str__(self):
        return f"{self.ip_address} | Attempts: {self.attempts} | Blocked: {self.blocked}"
