from pydantic.main import BaseModel, Extra


class OrdersAssign(BaseModel, extra=Extra.forbid):
    courier_id: int
