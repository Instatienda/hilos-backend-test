from django.utils import timezone
from rest_framework import generics
from rest_framework_csv import renderers as r
from rest_framework.response import Response

from api.models import FlowExecution


class FlowExecutionResultDownload(generics.RetrieveAPIView):
    renderer_classes = (r.CSVRenderer, )

    def get_queryset(self):
        return FlowExecution.objects.filter(
            flow__team__team_members__user=self.request.user).prefetch_related(
                'contact_executions', 'contact_executions__execution_steps')

    def get(self, request, *args, **kwargs):
        from api.models.flow_step import StepType
        instance = self.get_object()
        keys = [s.name for s in instance.flow.steps.order_by(
            'created_on').all()]
        data = []
        for contact in instance.contact_executions.all():  # noqa
            step_data = {}
            for execution_step in contact.execution_steps.all():  # noqa
                if execution_step.execution_result:
                    if execution_step.step.step_type == StepType.CONDITIONAL:
                        step_data[execution_step.step.name
                                  ] = execution_step.execution_result.get('conditional')  # noqa

                    if execution_step.step.step_type == StepType.QUESTION:
                        step_data[execution_step.step.name
                        ] = execution_step.execution_result.get('answer')  # noqa
            data.append(step_data)

        # Now properly format data. For CSV renderer to work well, data must be
        # as a dict with headers as keys. For keys wo value, set an empty str
        for sd in data:
            for key in keys:
                sd[key] = sd.get(key) if sd.get(key) is not None else ''

        download_time = timezone.now().strftime('d/M/Y HH:mm:ss')
        filename = f'{instance.flow.name} Results {download_time}'
        response = Response(
            data,
            content_type='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'})
        return response
