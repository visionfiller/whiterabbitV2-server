
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import date as date_filter

class Message(models.Model):
    """Message Model
        
    """
    sender = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="messagesent")
    receiver = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, related_name="messagereceived")
    body = models.CharField(max_length=150)
    date = models.DateTimeField(default=timezone.now)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.date = timezone.now()
        return super(Message, self).save(*args, **kwargs)
    @property
    def formatted_date(self):
        return date_filter(self.date, "Y-m-d h:i A")