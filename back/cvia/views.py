import os
import time
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return JsonResponse({'message': 'Hello, world! ResumEnhancAI✨ is running.'})


def is_pdf(file_path: str) -> bool:
    with open(file_path, 'rb') as f:
        header = f.read(4)
        return header == b'%PDF'


def extract_text_from_pdf(file_path: str) -> str:
    text = ''
    return text


def analyze_cv(text: str) -> int:
    score = 100
    return score


def generate_recommendations(text: str) -> str:
    recommendations = "You should add more information about your experience."
    return recommendations

@csrf_exempt
def upload_cv(request):
    if request.method == 'POST':
        file = request.FILES['cv']
        timestamp = int(time.time())
        file_name = f"cv_{timestamp}_{file.name}"
        file_path = default_storage.save(file_name, file)
        try:
            if not is_pdf(file_path):
                if os.path.exists(file_path):
                    os.remove(file_path)
                return JsonResponse(
                    data={'error': 'The file is not a PDF.'},
                    status=400)

            text = extract_text_from_pdf(file_path)
            score = analyze_cv(text)
            recommendations = generate_recommendations(text)

            if os.path.exists(file_path):
                os.remove(file_path)

            return JsonResponse(
                {'score': score, 'recommendations': recommendations})
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
