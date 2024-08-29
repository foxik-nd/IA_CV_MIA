import os
import time
import PyPDF2
from mistralai import Mistral
from dotenv import load_dotenv
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt


def index():
    return JsonResponse({'message': 'Hello, world! ResumEnhancAI✨ is running.'})


def is_pdf(file_path: str) -> bool:
    with open(file_path, 'rb') as f:
        header = f.read(4)
        return header == b'%PDF'


def extract_text_from_pdf(pdf_path: str) -> str:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text


def ask_mistral(prompt: str, model: str = 'open-mixtral-8x22b') -> str:
    load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set MISTRAL_API_KEY in the .env file.")

    client = Mistral(api_key=api_key)
    try:
        response = client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        if response and response.choices:
            return response.choices[0].message.content.strip()
        else:
            return "No recommendation available."

    except ValueError as e:
        return f"Requests rate limit exceeded. Details: {str(e)}"


def score_cv(text: str) -> int:
    prompt = f"""
    Vous allez évaluer le texte de CV suivant sur une échelle de 0 à 100, où 100 
    représente un CV parfait. 
    Veuillez attribuer une note basée uniquement sur les critères suivants :
    
    1. **Qualité du contenu** (jusqu'à 30 points) : 
    Évaluez la pertinence des informations, leur précision, et leur utilité 
    pour le poste visé.
    2. **Clarté de l'expression** (jusqu'à 25 points) : Les idées sont-elles 
    bien structurées et exprimées de manière claire ?
    3. **Concision** (jusqu'à 20 points) : Le CV est-il concis tout en 
    fournissant les informations nécessaires sans surcharger ?
    4. **Orthographe et grammaire** (jusqu'à 15 points) : Chaque faute 
    d'orthographe ou de grammaire retire 1 point.
    5. **Engagement** (jusqu'à 10 points) : Le texte est-il engageant, 
    captivant et convaincant pour un recruteur ?
    
    **Important :** Répondez uniquement par un nombre entier représentant 
    la note finale, sans aucun texte supplémentaire.
    
    Exemple de réponse correcte : 85
    
    Texte du CV :
    "{text}"
    """
    return int(ask_mistral(prompt, model='open-mixtral-8x22b'))


def recommendation_cv(text: str) -> str:
    prompt = f"""
    Étant donné le texte de CV suivant, fournissez une recommandation brève, 
    concise et professionnelle qui aborde directement les domaines à améliorer. 
    La recommandation doit être actionnable et aller droit au but, 
    en évitant tout détail superflu. Considérez le ton et le style appropriés.

    Texte du CV :
    "{text}"

    Recommandation :
    """
    try:
        return ask_mistral(prompt, model='mistral-large-latest')
    except Exception as e:
        return f"Error: Unable to generate a score. Details: {str(e)}"


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
            score = score_cv(text)
            recommendations = recommendation_cv(text)

            if os.path.exists(file_path):
                os.remove(file_path)

            return JsonResponse(
                {'score': score, 'recommendations': recommendations})
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
