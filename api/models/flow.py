from django.db import models

from uuid import uuid4

from api.models.base import BaseModel


class Comparison(models.TextChoices):
    EXACT = 'exact'
    DIFFERENT = '!exact'
    GTE = 'gte'
    GT = 'gt'
    LTE = 'lte'
    LT = 'lt'
    IS_NULL = 'isnull'
    NOT_NULL = '!isnull'
    CONTAINS = 'icontains'
    NOT_CONTAINS = '!icontains'


class Flow(BaseModel):
    class FlowEndAction(models.TextChoices):
        WEBHOOK = 'WEBHOOK', 'Webhook'
        NO_ACTION = 'NO_ACTION', 'No action'

    class ExecutionType(models.TextChoices):
        INBOUND = 'INBOUND', 'Inbound'
        OUTBOUND = 'OUTBOUND', 'Outbound'

    id = models.UUIDField(default=uuid4, primary_key=True)
    team = models.ForeignKey('api.Team',
                             on_delete=models.CASCADE,
                             related_name='flows')
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey('auth.User',
                                   on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    # Execution
    execution_type = models.CharField(max_length=20,
                                      choices=ExecutionType.choices)

    first_step = models.ForeignKey('api.FlowStep',
                                   on_delete=models.CASCADE,
                                   blank=True, null=True,
                                   related_name='ffs')

    class Meta():
        ordering = ['team']

    def __str__(self):
        return self.name
