from django.db import models

from uuid import uuid4
from api.models.base import BaseModel


class Contact(BaseModel):
    id = models.UUIDField(default=uuid4, primary_key=True)
    team = models.ForeignKey('api.Team',
                             on_delete=models.CASCADE,
                             related_name='contacts')
    phone = models.CharField(max_length=30)

    class Meta():
        ordering = ['team']

    def __str__(self):
        return f'{self.id} - {self.phone}'
