from app.crud.base import CRUDBase
from app.models.cognitive_profile import CognitiveProfile
from app.schemas.cognitive_profile import CognitiveProfileUpdate

class CRUDCognitiveProfile(CRUDBase[CognitiveProfile, None, CognitiveProfileUpdate]):
    """
    CRUD operations for the CognitiveProfile model.
    """
    pass

profile = CRUDCognitiveProfile(CognitiveProfile)