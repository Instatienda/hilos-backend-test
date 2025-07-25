from django.db import models

from uuid import uuid4

from api.models.base import BaseModel


class FlowExecution(BaseModel):
    id = models.UUIDField(default=uuid4, primary_key=True)
    flow = models.ForeignKey('api.Flow',
                             on_delete=models.CASCADE,
                             related_name='executions')

    class Meta():
        ordering = ['flow', '-created_on']

    def __str__(self):
        return f'Execution for {self.flow}'

    def get_results_list(self):
        raise NotImplementedError('finish me!')
