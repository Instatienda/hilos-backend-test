from typing import OrderedDict
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

    def test_can_order_results(self):
        # Create flow
        flow = models.Flow.objects.create(
            name='Test',
            team=self.team)

        # Add steps, joined through next_step_default
        step_q_2 = models.FlowStep.objects.create(
            flow=flow,
            name="Another Question S3",
            step_type=models.flow_step.StepType.QUESTION,
            answer_type=models.FlowStep.AnswerType.FREE_TEXT,
            body="Another question")
        step_c = models.FlowStep.objects.create(
            flow=flow,
            name="Conditional S2",
            step_type=models.flow_step.StepType.CONDITIONAL,
            next_step_default=step_q_2)
        step_q = models.FlowStep.objects.create(
            flow=flow,
            name="Question S1",
            step_type=models.flow_step.StepType.QUESTION,
            answer_type=models.FlowStep.AnswerType.SINGLE_OPTION,
            body="Hey, which option do ya want?",
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
            flow=flow)

        # Create flow execution for contact
        flow_execution_contact = models.FlowExecutionContact.objects.create(
            flow_execution=flow_execution,
            contact=contact)

        # Create flow execution steps for contact
        # (only 2 steps have been completed)
        flow_execution_step_q = models.FlowExecutionStep.objects.create(
            flow_execution_contact=flow_execution_contact,
            step=step_q,
            execution_result={'answer': 'Option 1'})
        flow_execution_step_c = models.FlowExecutionStep.objects.create(
            flow_execution_contact=flow_execution_contact,
            step=step_c,
            execution_result={'conditional': True})

        # We expect a list with ordered result dicts like
        # [
        #   {Phone: 123, Step1: Result1, Step2: Result2, ...},
        #   {Phone: 123, Step1: Result1, Step2: Result2, ...}
        # ]
        # If a step does not have a result, return an empty string
        expected_dict = OrderedDict()
        expected_dict.update({
            'Phone': contact.phone})
        expected_dict.update({
            step_q.name: flow_execution_step_q.execution_result['answer']})
        expected_dict.update({
            step_c.name: flow_execution_step_c.execution_result['conditional']})
        expected_dict.update({
            step_q_2.name: ''})

        result_list = flow_execution.get_results_list()
        self.assertEqual([expected_dict, ], result_list)

    def test_download_results_csv(self):
        # Create flow
        flow = models.Flow.objects.create(
            name='Test',
            team=self.team)

        # Add steps, joined through next_step_default
        step_q_2 = models.FlowStep.objects.create(
            flow=flow,
            name="Question 2",
            step_type=models.flow_step.StepType.QUESTION,
            answer_type=models.FlowStep.AnswerType.FREE_TEXT,
            body="Another question")
        step_c = models.FlowStep.objects.create(
            flow=flow,
            name="Conditional",
            step_type=models.flow_step.StepType.CONDITIONAL,
            next_step_default=step_q_2)
        step_q = models.FlowStep.objects.create(
            flow=flow,
            name="Question 1",
            step_type=models.flow_step.StepType.QUESTION,
            answer_type=models.FlowStep.AnswerType.SINGLE_OPTION,
            body="Hey, which option do ya want",
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
            flow=flow)

        # Create flow execution for contact
        flow_execution_contact = models.FlowExecutionContact.objects.create(
            flow_execution=flow_execution,
            contact=contact)

        # Create flow execution steps for contact
        # (only 2 steps have been completed)
        flow_execution_step_q = models.FlowExecutionStep.objects.create(
            flow_execution_contact=flow_execution_contact,
            step=step_q,
            execution_result={'answer': 'Option 1'})
        flow_execution_step_c = models.FlowExecutionStep.objects.create(
            flow_execution_contact=flow_execution_contact,
            step=step_c,
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
