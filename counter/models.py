import json
from datetime import datetime
from math import sqrt

import uuid as uuid
from django.db import models
from django.db.models import DateTimeField


# class Point(models.Model):
#     x = models.FloatField()
#     y = models.FloatField()
#
#     #calculate distance between two points according to the formula
#     def calculate_distance(self, point):
#         return sqrt(pow(self.x - point.x, 2) + pow(self.y - point.y, 2))


class Profile(models.Model):
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    user_name = models.CharField(unique=True, max_length=120, blank=True, null=True)
    password = models.CharField(max_length=120, blank=True, null=True)
    phone_number = models.CharField(max_length=120, blank=True, null=True)

    def save(self, *args, **kwargs):
        fields = kwargs.pop('update_fields', [])
        if fields != ['last_login']:
            return super(Profile, self).save(*args, **kwargs)
class Message(models.Model):
    content = models.TextField(help_text='Message text', null=False, blank=True)
    subject = models.TextField(help_text='Message text', null=False, blank=True)
    creation_time = DateTimeField(default=datetime.now)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    read = models.BooleanField(default=False, null=True, blank=True)
    receiver = models.TextField(help_text='Phone numbers', null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['receiver', 'creation_time']),
        ]

    def sender_name(self):
        return self.sender.first_name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
