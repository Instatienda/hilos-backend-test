from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_on = models.DateTimeField(
        verbose_name='Creado el',
        default=timezone.now,
        db_index=True)
    last_updated_on = models.DateTimeField(
        verbose_name='Última actualización el',
        auto_now=True)

    class Meta():
        abstract = True
