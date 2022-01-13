from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import flow_execution


urlpatterns = format_suffix_patterns([
    path('flow-execution/<uuid:pk>/download',
         flow_execution.FlowExecutionResultDownload.as_view(),
         name='flow-execution-result-download'),
])
