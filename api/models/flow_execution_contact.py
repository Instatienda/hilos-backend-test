from django.db import models

from uuid import uuid4

from api.models.base import BaseModel


class FlowExecutionContact(BaseModel):
    class Status(models.TextChoices):
        READY = 'READY'
        RUNNING = 'RUNNING'
        COMPLETED = 'COMPLETED'
        CANCELED = 'CANCELED'
        STOPPED = 'STOPPED'
        EXPIRED = 'EXPIRED'

    id = models.UUIDField(default=uuid4, primary_key=True)
    flow_execution = models.ForeignKey('api.FlowExecution',
                                       on_delete=models.CASCADE,
                                       related_name='contact_executions')
    contact = models.ForeignKey('api.Contact',
                                on_delete=models.CASCADE,
                                related_name='flow_executions')

    status = models.CharField(max_length=50,
                              choices=Status.choices,
                              default=Status.READY)

    class Meta():
        ordering = ['flow_execution', 'created_on']

    def __str__(self):
        return f'{self.flow_execution} - {self.contact}'
