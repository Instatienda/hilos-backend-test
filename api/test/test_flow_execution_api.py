from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from io import StringIO
import csv

from api import models


class FlowExecutionAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='test', email='test@instatienda.mx')
        self.team = models.Team.objects.create(
            name="Test")
        models.TeamMember.objects.create(user=self.user, team=self.team)

    def login(self):
        self.client.force_authenticate(user=self.user)

    def test_download_results_csv(self):
        # Create flow
        flow = models.Flow.objects.create(
            name='Inbound test',
            team=self.team,
            execution_type=models.Flow.ExecutionType.INBOUND,
            is_active=True,
            created_by=self.user)

        # Add steps, joined through next_step_default
        step_q_2 = models.FlowStep.objects.create(
            flow=flow,
            name="Question 2: B",
            step_type=models.flow_step.StepType.QUESTION,
            body_type=models.FlowStep.BodyType.TEXT,
            answer_type=models.FlowStep.AnswerType.FREE_TEXT,
            body="Another question")
        step_c = models.FlowStep.objects.create(
            flow=flow,
            name="Conditional",
            step_type=models.flow_step.StepType.CONDITIONAL,
            next_step_default=step_q_2)
        step_q = models.FlowStep.objects.create(
            flow=flow,
            name="Question 1: A",
            step_type=models.flow_step.StepType.QUESTION,
            body_type=models.FlowStep.BodyType.TEXT,
            answer_type=models.FlowStep.AnswerType.SINGLE_OPTION,
            answer_options='Óption 1, Option 2',
            body="Hey wassup grl, which option do ya want",
            next_step_default=step_c)

        # Set flow first step
        flow.first_step = step_q
        flow.save()

        # Create contact
        contact = models.Contact.objects.create(
            phone='+525576565090',
            team=self.team)

        # Create flow execution
        flow_execution = models.FlowExecution.objects.create(
            flow=flow,
            created_by=self.user,
            execution_type=models.FlowExecution.ExecutionType.INBOUND,
            execute_for=models.FlowExecution.ExecutionFor.ALL,
            inbound_start_message='Hi!')

        # Create flow execution for contact
        flow_execution_contact = models.FlowExecutionContact.objects.create(
            flow_execution=flow_execution,
            contact=contact)

        # Create flow execution steps for contact
        flow_execution_step_q = models.FlowExecutionStep.objects.create(
            flow_execution_contact=flow_execution_contact,
            step=step_q,
            status=models.FlowExecutionStep.Status.COMPLETED,
            execution_result={'answer': 'Option 1'})
        flow_execution_step_c = models.FlowExecutionStep.objects.create(
            flow_execution_contact=flow_execution_contact,
            step=step_c,
            status=models.FlowExecutionStep.Status.COMPLETED,
            execution_result={'conditional': True})

        self.login()
        response = self.client.get(
            reverse('api:flow-execution-result-download',
                    kwargs={'pk': flow_execution.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = StringIO(response.content.decode(encoding='utf-8'))
        reader = csv.reader(result)

        # We expect to get a csv with the following
        expected_rows = [
            [step_q.name, step_c.name, step_q_2.name],
            [flow_execution_step_q.execution_result['answer'],
             str(flow_execution_step_c.execution_result['conditional']),
             '']
        ]
        for idx, row in enumerate(reader):
            self.assertEqual(expected_rows[idx], row)
