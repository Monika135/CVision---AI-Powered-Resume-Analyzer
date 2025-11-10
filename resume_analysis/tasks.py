from celery import shared_task
from .utils import analyze_resume
from .models import ResumeAnalysis

@shared_task(bind=True)
def analyze_resume_task(self, analysis_id, resume_text, job_description):
    result = analyze_resume(resume_text, job_description)
    try:
        analysis = ResumeAnalysis.objects.get(pk=analysis_id)
        analysis.analysis_id = analysis_id
        analysis.ats_score = result["score"]
        analysis.matched_keywords = result["matched_keywords"]
        analysis.missing_keywords = result["missing_keywords"]
        analysis.suggestions = result["suggestions"]
        analysis.save()
        return {"status": "success", "result": result}
    except ResumeAnalysis.DoesNotExist:
        return {"status": "failed", "error": "Analysis record not found"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
