from django.db import models

from api.models.base import BaseModel


class StepType(models.TextChoices):
    CONDITIONAL = 'CONDITIONAL'
    MESSAGE = 'MESSAGE'
    QUESTION = 'QUESTION'


class FlowStep(BaseModel):
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

    flow = models.ForeignKey('api.Flow',
                             on_delete=models.CASCADE,
                             related_name='steps')
    name = models.CharField(max_length=100)
    step_type = models.CharField(max_length=100,
                                 choices=StepType.choices)
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
    answer_type = models.CharField(max_length=30,
                                   blank=True, null=True,
                                   choices=AnswerType.choices)
    is_deleted = models.BooleanField(default=False)

    class Meta():
        ordering = ['flow', 'id']

    def __str__(self):
        return self.name
