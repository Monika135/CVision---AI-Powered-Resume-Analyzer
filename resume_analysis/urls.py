from django.urls import path
from .views import AnalyzeResumeAPI, AnalysisHistoryAPI, AnalysisDetailAPI, resume_analysis_view

app_name = 'resume_analysis'


urlpatterns = [
    path("api/analyze_resume/", AnalyzeResumeAPI.as_view(), name="api_analyze"),
    path("api/analyses_history/", AnalysisHistoryAPI.as_view(), name="api_analyses"),
    path("api/analyses_detail/<uuid:id>/", AnalysisDetailAPI.as_view(), name="api_analysis_detail"),
    path("resume_analysis_view/", resume_analysis_view, name = "resume_analysis_view"),
]
