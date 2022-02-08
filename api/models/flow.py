from django.db import models

from uuid import uuid4

from api.models.base import BaseModel


class Flow(BaseModel):
    id = models.UUIDField(default=uuid4, primary_key=True)
    team = models.ForeignKey('api.Team',
                             on_delete=models.CASCADE,
                             related_name='flows')
    name = models.CharField(max_length=100)
    first_step = models.ForeignKey('api.FlowStep',
                                   on_delete=models.CASCADE,
                                   blank=True, null=True,
                                   related_name='ffs')

    class Meta():
        ordering = ['team']

    def __str__(self):
        return self.name
