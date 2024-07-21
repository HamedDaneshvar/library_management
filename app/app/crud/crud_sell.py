from app.crud.base import CRUDBase
from app.models.sell import Sell
from app.schemas.sell import SellCreate, SellUpdate


class CRUDSell(CRUDBase[Sell, SellCreate, SellUpdate]):
    pass

sell = CRUDSell(Sell)
