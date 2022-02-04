from django.db import models

from uuid import uuid4

from api.models.base import BaseModel


class FlowExecution(BaseModel):
    class Status(models.TextChoices):
        READY = 'READY'
        RUNNING = 'RUNNING'
        COMPLETED = 'COMPLETED'
        CANCELED = 'CANCELED'
        STOPPED = 'STOPPED'

    id = models.UUIDField(default=uuid4, primary_key=True)
    flow = models.ForeignKey('api.Flow',
                             on_delete=models.CASCADE,
                             related_name='executions')
    status = models.CharField(max_length=50,
                              choices=Status.choices,
                              default=Status.READY)

    class Meta():
        ordering = ['flow', '-created_on']

    def __str__(self):
        return f'{self.flow} - {self.execution_type} - {self.status}'

    def get_results_list(self):
        raise NotImplementedError('finish me!')
