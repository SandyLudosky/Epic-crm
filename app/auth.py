from sqlalchemy.orm.exc import NoResultFound
from app.models import User
import pickle
import os

SESSION_FILE = "sessions.pkl"


class Authentication:
    def __init__(self, session):
        self.session = session


def authenticate_user(session, name, password):
    print("authenticate_user", name, password, session)
    try:
        # Récupérer l' ser par son nom d'utilisateur
        user = session.query(User).filter_by(name=name).one()

        # Vérifier le mot de passe
        if user.check_password(password):
            return user  # Authentification réussie
    except NoResultFound:
        pass  # L'user n'existe pas

    return None  # Authentification échouée


def get_current_user(session):
    try:
        file = recuperer_session()
        if file:
            user_id = file.split("_")[0]
            user = session.query(User).filter_by(name=user_id).one()
            return user
    except NoResultFound:
        pass


def sauvegarder_session(session_id, user_id):
    # Fonction pour sauvegarder la session
    with open(SESSION_FILE, "wb") as file:
        pickle.dump(session_id, file)
        pickle.dump(user_id, file)


def recuperer_session():
    # Fonction pour récupérer la session
    try:
        with open(SESSION_FILE, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None


def authentification_initiale(session, name, password):
    # Authentification initiale
    user = authenticate_user(session, name, password)
    if user:
        session_id = f"{name}_{user.id}"  # Créer un ID de session unique
        user_id = user.id
        sauvegarder_session(session_id, user_id)
        print("Authentification réussie.")
        return user.id
    else:
        print("Authentification échouée.")
        return None


def auto_login(session):
    # Vérification de l'authentification au lancement suivant
    session_id = recuperer_session()
    if session_id:
        return session_id.split("_")[1]
    else:
        print("Aucune session trouvée. Veuillez vous authentifier.")
        return None


def is_admin(session, user_id):
    user = session.query(User).filter_by(id=user_id).one()
    if user:
        return user.role
    else:
        return None


def logout_user():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    print("User successfully logged out!")
    exit()


def admin_required(session):
    return auto_login(session) and is_admin(session, auto_login(session)) == "admin"
