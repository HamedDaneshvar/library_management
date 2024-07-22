from app.crud.base import CRUDBase
from app.models.borrow import Status
from app.schemas.borrow import StatusCreate, StatusUpdate


class CRUDStatus(CRUDBase[Status, StatusCreate, StatusUpdate]):
    pass


status = CRUDStatus(Status)
