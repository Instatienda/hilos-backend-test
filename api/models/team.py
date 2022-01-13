from django.db import models

from api.models.base import BaseModel


class Team(BaseModel):
    name = models.CharField(max_length=100)

    class Meta():
        ordering = ['-id']

    def __str__(self):
        return self.name


class TeamMember(BaseModel):
    user = models.OneToOneField('auth.User',
                                on_delete=models.CASCADE,
                                related_name='team_membership')
    team = models.ForeignKey('api.Team',
                             on_delete=models.CASCADE,
                             related_name='team_members')

    def __str__(self):
        return f'{self.team.name} - {self.user.email}'
