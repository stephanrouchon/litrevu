# LitRevu

Application web de publication de d'échange de critiques de livres ou d'articles

# Prérequis
- Python 3.13.1

application développé sous Django

### 1. Clonez le dépôt GIT :
https://github.com/stephanrouchon/litrevu.git</br>
cd litrevu

### 2. creez un environnement virtuel :
python -m venv env

### 3. activez l'environnement virtuel
- a. sur macOS/Linux : 
  
source env/bin/activate
    
- b. sur windows
  
 env\Scripts\activate

### 4. Installez les dépendances

pip install -r requirements.txt

Configuration

### 5. Créer un fichier env à la racine du projet avec les élements suivants

- SECRET_KEY=your_secret_key
-  DEBUG=True
- ALLOWED_HOSTS= [localhost,127.0.0.1]

### 6. Appliquez les migrations de la base de données :
python manage.py migrate

### 7. Créez un superutilisateur pour accéder à l'interface d'administration :
python manage.py createsuperuser

Utilisation
### 8. Lancez le serveur de développement 

python manage.py runserver

Accedez à l'application dans votre navigateur à l'adresse suivante

http://127.0.0.1:8000

### Fonctionnalités
- Publication de critiques de livres ou d'articles
- Échange de critiques entre utilisateurs
- Gestion des abonnements et des abonnés
- Blocage et déblocage des utilisateurs


Licence
Ce projet est sous licence MIT.
