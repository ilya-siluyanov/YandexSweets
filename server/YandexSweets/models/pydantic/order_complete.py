from pydantic.main import BaseModel, Extra


class OrderComplete(BaseModel, extra=Extra.forbid):
    courier_id: int
    order_id: int
    complete_time: str
