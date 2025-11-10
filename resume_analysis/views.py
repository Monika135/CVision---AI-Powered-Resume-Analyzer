from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ResumeAnalysis
from .serializers import ResumeAnalysisSerializer
from .utils import analyze_resume, extract_text_from_pdf, extract_text_from_docx
from .tasks import analyze_resume_task


class AnalyzeResumeAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResumeAnalysisSerializer

    def post(self, request):
        resume_text = request.data.get("resume_text", "").strip()
        job_description = request.data.get("job_description", "").strip()

        file_obj = request.FILES.get("file")
        if file_obj:
            content_type = file_obj.content_type
            if content_type == "application/pdf" or file_obj.name.lower().endswith(".pdf"):
                file_bytes = file_obj.read()
                resume_text = extract_text_from_pdf(file_bytes)
            elif file_obj.name.lower().endswith((".docx", ".doc")):
                file_bytes = file_obj.read()
                resume_text = extract_text_from_docx(file_bytes)
            else:
                return Response({"error": "Unsupported file type."}, status=400)

        if not resume_text or not job_description:
            return Response({"error": "Provide both resume text (or file) and job_description."}, status=400)

        analysis = ResumeAnalysis.objects.create(
            user=request.user,
            resume_text=resume_text,
            job_description=job_description
            )

        # Try to call Celery (if running). If Celery not configured or raises error, run synchronously.
        try:
            task = analyze_resume_task.delay(str(analysis.id), resume_text, job_description)
            return Response({"message": "Analysis started", "analysis_id": analysis.id, "task_id": task.id} , status=202)
        except Exception:
            result = analyze_resume(resume_text, job_description)
            analysis.ats_score = result["score"]
            analysis.matched_keywords = result["matched_keywords"]
            analysis.missing_keywords = result["missing_keywords"]
            analysis.suggestions = result["suggestions"]
            analysis.save()

            return Response(ResumeAnalysisSerializer(analysis).data, status=201)


class AnalysisHistoryAPI(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResumeAnalysisSerializer
    
    def get_queryset(self):
        return ResumeAnalysis.objects.filter(
            user=self.request.user,
            ats_score__isnull=False
        ).order_by("-created_at")
    
class AnalysisDetailAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResumeAnalysisSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return ResumeAnalysis.objects.filter(user=self.request.user)



@login_required
def resume_analysis_view(request):
    return render(request, "analyser/result.html")
