from firebase_admin import credentials, initialize_app

from app.core.config import settings


class Firebase:
    db = None


cred = credentials.Certificate(settings.CERTIFICATE.dict())
initialize_app(cred)
firebase = Firebase()
