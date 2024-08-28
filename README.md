# ResumEnhancAI✨

**ResumEnhancAI✨** est un outil basé sur Django qui permet aux utilisateurs d'améliorer leurs CV en attribuant un score et en générant des recommandations personnalisées grâce à l'intelligence artificielle. 
L'application traite les fichiers de manière éphémère, sans stocker de données, afin de garantir la confidentialité des utilisateurs.

## Fonctionnalités

- **Upload de CV en PDF** : Les utilisateurs peuvent télécharger leur CV au format PDF.
- **Analyse IA** : L'outil attribue un score au CV et propose des recommandations d'amélioration basées sur un modèle d'intelligence artificielle.
- **Traitement éphémère** : Les fichiers sont supprimés immédiatement après traitement pour assurer la confidentialité.

## Prérequis

- Python 3.x
- Django 3.x ou supérieur


## Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/votre-utilisateur/resumenhancai.git
   cd IA_CV_MIA
   ```

2. Créez un environnement virtuel et activez-le :

   ```bash
   python -m venv env
   source env/bin/activate 
   ```

3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

4. Lancez le serveur de développement :

   ```bash
   python manage.py runserver
   ```

## Utilisation

- **Endpoints** :
   - **POST `/upload/`** : Téléversez un fichier PDF pour analyse. Le backend renverra un score et des recommandations en JSON.
   
   Exemple de réponse JSON :
   ```json
   {
     "score": 85,
     "recommendations": "Ajoutez une section 'Projets' pour mettre en avant vos réalisations."
   }
   ```

## Auteurs
- Nassim YAZI
- Nicolas DESFORGES