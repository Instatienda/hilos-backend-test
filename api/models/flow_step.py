from django.db import models

from api.models.base import BaseModel
from api.models.flow import Comparison


class StepType(models.TextChoices):
    CONDITIONAL = 'CONDITIONAL'
    MESSAGE = 'MESSAGE'
    QUESTION = 'QUESTION'
    ACTION = 'ACTION'
    DELAY = 'DELAY'


class FlowStep(BaseModel):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PENDING = 'PENDING', 'Pending'
        RUNNING = 'RUNNING', 'En curso'
        COMPLETED = 'COMPLETED', 'Completado'
        CANCELED = 'CANCELED', 'Cancelado'

    class AnswerType(models.TextChoices):
        FREE_TEXT = 'FREE_TEXT'
        SINGLE_OPTION = 'SINGLE_OPTION'
        MULTIPLE_OPTIONS = 'MULTIPLE_OPTIONS'
        NUMBER = 'NUMBER'
        URL = 'URL'
        EMAIL = 'EMAIL'
        FILE = 'FILE'
        IMAGE = 'IMAGE'
        PHONE = 'PHONE'
        DATE = 'DATE'
        TIME = 'TIME'
        DATETIME = 'DATETIME'
        BOOL = 'BOOL'

    class BodyType(models.TextChoices):
        TEXT = 'TEXT'
        IMAGE = 'IMAGE'
        FILE = 'FILE'
        LOCATION = 'LOCATION'

    flow = models.ForeignKey('api.Flow',
                             on_delete=models.CASCADE,
                             related_name='steps')
    name = models.CharField(max_length=100)
    step_type = models.CharField(max_length=100)
    next_step_default = models.OneToOneField('api.FlowStep',
                                             on_delete=models.CASCADE,
                                             blank=True, null=True,
                                             related_name='previous_step')
    # Conditional
    next_step_alternate = models.OneToOneField('api.FlowStep',
                                               on_delete=models.CASCADE,
                                               blank=True, null=True,
                                               related_name='previous_step_alt')

    # Question / Message
    body = models.TextField(blank=True, null=True)
    body_type = models.CharField(max_length=20,
                                 blank=True, null=True,
                                 choices=BodyType.choices)
    answer_type = models.CharField(max_length=30,
                                   blank=True, null=True,
                                   choices=AnswerType.choices)
    answer_validation_message = models.TextField(blank=True, null=True)
    answer_options = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta():
        ordering = ['flow', 'id']

    def __str__(self):
        return self.name


class StepConditionalCondition(models.Model):
    step = models.ForeignKey('api.FlowStep',
                             on_delete=models.CASCADE,
                             related_name='conditions')
    field = models.CharField(max_length=255)
    comparison = models.CharField(max_length=30,
                                  choices=Comparison.choices)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.step.pk} - {self.field} {self.comparison} {self.value}'
