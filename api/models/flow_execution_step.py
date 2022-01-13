from django.db import models

from uuid import uuid4

from api.models.base import BaseModel


class FlowExecutionStep(BaseModel):
    class Status(models.TextChoices):
        WAITING_TO_START = 'WAITING_TO_START'
        NOT_EXECUTED = 'NOT_EXECUTED'
        RUNNING = 'RUNNING'
        COMPLETED = 'COMPLETED'
        CANCELED = 'CANCELED'

    id = models.UUIDField(default=uuid4, primary_key=True)
    flow_execution_contact = models.ForeignKey('api.FlowExecutionContact',
                                               on_delete=models.CASCADE,
                                               related_name='execution_steps')
    step = models.ForeignKey('api.FlowStep',
                             on_delete=models.CASCADE,
                             related_name='execution_steps')
    status = models.CharField(max_length=20,
                              choices=Status.choices,
                              default=Status.WAITING_TO_START)

    execution_result = models.JSONField(blank=True, null=True)

    class Meta():
        ordering = ['flow_execution_contact', 'created_on']

    def __str__(self):
        return f'{self.flow_execution_contact} - {self.step}'

    def get_next_step(self):
        from api.models.flow_step import StepType
        if self.step.step_type == StepType.CONDITIONAL:
            if not self.execution_result['conditional']:
                return self.step.next_step_alternate
        return self.step.next_step_default
