from django.db import models

from uuid import uuid4

from api.models.base import BaseModel


class FlowExecution(BaseModel):
    class ExecutionFor(models.TextChoices):
        FILTERS = 'FILTERS'
        LIST = 'LIST'
        ALL = 'ALL'

    class Status(models.TextChoices):
        READY = 'READY'
        RUNNING = 'RUNNING'
        COMPLETED = 'COMPLETED'
        CANCELED = 'CANCELED'
        STOPPED = 'STOPPED'

    class ExecutionType(models.TextChoices):
        INBOUND = 'INBOUND'
        OUTBOUND = 'OUTBOUND'
        API = 'API'

    id = models.UUIDField(default=uuid4, primary_key=True)
    flow = models.ForeignKey('api.Flow',
                             on_delete=models.CASCADE,
                             related_name='executions')
    created_by = models.ForeignKey('auth.User',
                                   on_delete=models.CASCADE)
    start_on = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50,
                              choices=Status.choices,
                              default=Status.READY)
    execute_for = models.CharField(max_length=20,
                                   choices=ExecutionFor.choices)
    execution_type = models.CharField(max_length=20,
                                      choices=ExecutionType.choices)
    inbound_start_message = models.TextField(blank=True, null=True)
    inbound_start_message_match_exact = models.BooleanField(default=True)

    class Meta():
        ordering = ['flow', '-created_on']

    def __str__(self):
        return f'{self.flow} - {self.execution_type} - {self.status}'
